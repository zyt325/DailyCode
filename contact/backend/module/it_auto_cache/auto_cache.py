# -*- coding: utf-8 -*-
import os
import inspect
import time

try:
    import cPickle as pickle
except ImportError:
        import pickle
from .cache import Cache

__all__ = [
    'get_auto_cache',
    'auto_cache_decorator',
    'DoNotCacheException',
]


class DoNotCacheException(Exception):
    """
    Tells the cache mechanism to not store the result in the cache.

    Instead of a regular return call, a function that's being cached
    can raise a DoNotCacheException (which is given the return value),
    signalling to the cache framework that the return value should not
    be cached. Subsequent calls to the function will still miss the
    cache, and a new value can be computed and returned (and possibly
    cached).
    """

    def __init__(self, return_value):
        """
        Populates the DoNotCacheException with the given return_value.
        """
        super(DoNotCacheException, self).__init__()

        self.return_value = return_value


class CacheMiss(Exception):
    """
    Raised whenever we tried to find a key that's not in the cache.
    """

    def __init__(self, func, args, kwargs):
        super(CacheMiss, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs


class MG(object):
    """MG is a Module Global class used just for namespacing our module globals"""

    # _cache_dict is a global dict that is used to keep track of the AutoCache
    # objects that have been returned by the get_auto_cache function.
    _cache_dict = dict()


with open(os.path.join(os.path.dirname(__file__), 'scripts', 'set.lua')) as lua_set_file:
    lua_set = lua_set_file.read()


class AutoCache(Cache):
    """
    Gives us a convenient way to use a decorator to cache any function-call.

    It is a subclass of Cache, which implements the namespaced caching."""
    time_cost_suffix = 'time_cost'

    def __init__(self, namespace='', expire_time=None, host='cache.base-fx.com', only_read=False, force_update=False,alternate_hosts=None):
        """
        Sets up our redis cache with the given namespace.

        :param basestring namespace: Namespace to apply to our caches.
                                     None means use 'Default'.
        :param int expire_time: Specific expiry time, in seconds.
                                None means use redis' default.
        """
        namespace = 'ITD:%s' % namespace
        self._only_read = only_read
        self._force_update = force_update

        super(AutoCache, self).__init__(
            namespace=namespace,
            expire_time=expire_time,
            host=host,
            alternate_hosts=alternate_hosts,
        )
        self._lua_set = self._redis.register_script(lua_set)
        self._time_cost_keys_pattern = '{prefix}{sep}{ns}*{sep}{suffix}'.format(
            sep=self.sep, prefix=self.monitoring_prefix, ns=self._namespace, suffix=self.time_cost_suffix)

        # wrappers_map is used to keep track of what real functions were mapped
        # to what wrappers in the decorator
        self._wrappers_map = {}

    def decorator(self, func):
        """
        A function decorator to wrap any other function in boilerplate code.

        It will cache the results of that function call (or read from cache, if
        available).

        To use it, do something like this:
        @<decorator>
        def function_name(...):
           ...

        Just use the function as usual after that, and it will be optimised with
        the cache.
        Note: you can call your function like this:
           function_name(..., update_auto_cache=True)
        to force it to evaluate the underlying function, and to update the
        cache again regardless of what is already in the cache.
        """

        def wrapper(*args, **kwargs):
            # We allow users to force the wrapper to ignore any pre-existing
            # cache entry if they pass in the arg update_auto_cache=True as an
            # argument
            try:
                if kwargs.pop('update_auto_cache', False):
                    raise CacheMiss(func, args, kwargs)  # pretend we there was a cache miss
                if not self._only_read and self._force_update:
                    raise CacheMiss(func, args, kwargs)
                return self._read_cache(func, args, kwargs)
            except CacheMiss as e:
                if not self._only_read:
                    return self._update_cache(e.func, e.args, e.kwargs)

        # When this decorator is applied to a function, we keep track of it so
        # we can access the original function later.
        self._wrappers_map[wrapper] = func
        return wrapper

    def set(self, key, value, expire_seconds=None, expire_milliseconds=None,
            only_if_new=False, only_if_old=False, time_cost=0):
        """
        Set value in the cache corresponding to the given key.

        depending on how redis behaves given all the optional parameters.
        Maybe we should remove the expire_milliseconds option. It only adds
        confusion and isn't needed yet.

        :param basestring key: the key for the cached value
        :param basestring value: the value (must be a string) to be cached
        :param int expire_seconds: combined with expire_milliseconds
        :param int expire_milliseconds: combined with expire_seconds
        :param bool only_if_new: the set only happens if the key
                                 does NOT exist in the cache
        :param bool only_if_old: the set only happens if the key
                                 DOES exist in the cache
        :param float time_cost: how long when you calculate this value
        """
        pieces = []
        if expire_seconds:
            pieces.append('EX')
            pieces.append(expire_seconds)
        if expire_milliseconds:
            pieces.append('PX')
            pieces.append(expire_milliseconds)

        if only_if_new:
            pieces.append('NX')
        if only_if_old:
            pieces.append('XX')

        name = self._add_namespace_prefix(key)
        return self._lua_set([name, value] + pieces, ['{prefix}{sep}{name}{sep}{suffix}'.format(
            sep=self.sep, prefix=self.monitoring_prefix, name=name, suffix=self.time_cost_suffix), time_cost] + pieces)

    def time_cost_ave(self):
        raw_keys = self._redis.keys(self._time_cost_keys_pattern)
        if raw_keys:
            raw_values = self._redis.mget(raw_keys)
        else:
            raw_values = []
        return self._ave([float(value) for value in raw_values])

    def _get_source_func(self, wrapper):
        """
        Returns the raw function from the decorated one.

        Given the wrapper function that the decorator for this object has
        previously returned, this function returns the original function
        that was wrapped."""

        return self._wrappers_map[wrapper]

    def _get_cache_key(self, func, args, kwargs):
        """
        Compute the cache key to use for a function with its arguments.

        This is the function that's internally used to compute the key that's
        used to identify our cache location.  By default, it's combining the
        function name and a pickled version of the arguments, but you can
        override it in a sub-class if you can build a more efficient, but
        still unique, version.

        Its arguments are the original function that the decorator was applied
        to (available using _get_source_func) and the arguments that would be
        used in the call that is to be cached.

        The return type should be a unique string identifying that function
        call.

        :rtype: basestring
        """
        def _translate_args(self, *args, **kwargs):
            return args, kwargs
        args, kwargs = _translate_args(*args, **kwargs)
        return '{mn}{sep}{func}{sep}{args}'.format(
            sep=self.sep,
            mn=inspect.getmodule(func).__name__,
            func=func.__name__,
            args=pickle.dumps([args, kwargs]),
        )

    def _update_cache(self, func, args, kwargs):
        """
        Executes the given function with given args and caches the result.

        This is ignoring the current state of the cache, ie it will evaluate
        the function even if the cache already has a value for it.

        It returns the result of the function evaluation.
        """

        try:
            start_time = time.time()
            value = func(*args, **kwargs)  # evaluate the function
            end_time = time.time()
            self.set(
                self._get_cache_key(func, args, kwargs),
                pickle.dumps(value),
                self._expire_time,
                time_cost=end_time - start_time
            )  # cache the result
        except DoNotCacheException as e:
            # if the called function raised DoNotCacheException, then return
            # the value without caching
            return e.return_value
        return value

    def _read_cache(self, func, args, kwargs):
        """
        Strictly tries to get an already cached result.

        It returns None if the function call is not in the cache.
        """
        key = self._get_cache_key(func, args, kwargs)
        value_string = self.get(key)
        if value_string is None:
            raise CacheMiss(func, args, kwargs)  # pretend we there was a cache miss
        return pickle.loads(value_string)

    @classmethod
    def _ave(cls, iterable):
        return (1.0 * sum(iterable) / len(iterable)) if iterable else 0


def get_auto_cache(namespace='py_auto_cache', expire_time=None, host=None):
    """
    This returns an AutoCache object for the given parameters.

    There will be exactly one such object returned for all calls to this
    function in the current process.
    """
    if (namespace, expire_time, host) not in MG._cache_dict:
        MG._cache_dict[(namespace, expire_time, host)] = AutoCache(
            namespace=namespace,
            expire_time=expire_time,
            host=host,
        )
    return MG._cache_dict[(namespace, expire_time, host)]


def auto_cache_decorator(namespace='py_auto_cache',
                         expire_time=None, host=None):
    """
    This returns a function that can be used to decorate a function with caching

    The decorator will be caching the results of the given function in a cache
    that is specific to the function and the absolute path to the file the
    function is in.

    For example:

    @auto_cache_decorator(host='localhost')
    def foo():
        sleep(60) # wait for a minute
        return 42

    foo()   # the first time this is called in a given pipeline will take 1
            # minute, after that, it will be quick, as it gets the result from
            # the cache

    WARNING: it will not account for any differences in execution environment
             that may affect the results of the function call. For instance,
             any functions called within the root function will be greatly
             affected by the sys.path.
    """
    return get_auto_cache(namespace, expire_time, host).decorator
