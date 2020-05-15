# -*- coding: utf-8 -*-
import os
from redis import StrictRedis, ConnectionError, TimeoutError
from logging import getLogger, StreamHandler

logger = getLogger('py_auto_cache')
logger.addHandler(StreamHandler())

__all__ = ['Cache']


with open(os.path.join(os.path.dirname(__file__), 'scripts', 'get.lua')) as lua_get_file:
    lua_get = lua_get_file.read()


def _strip(str1, str2):
    if str1.startswith(str2):
        return str1[len(str2):]
    return str1


class Cache(object):
    """
    A wrapper class for redis to help support namespaces.

    The methods in this class will, unless otherwise stated,
    work within the namespace defined by this class.
    """
    sep = ':'
    global_ns = 'py_auto_cache'
    monitoring_prefix = 'monitoring'
    hits_suffix = 'hits'
    misses_suffix = 'misses'

    def __init__(self, namespace='default', expire_time=None, host='localhost', alternate_hosts=None):
        """
        Sets up our redis cache with the given namespace.

        :param basestring namespace: Namespace to apply to our interactions
                                     with redis. None means use 'Default'.
        :param int expire_time: Specific expiry time, in seconds.
                                if None, use the redis' default.
        """
        assert namespace != 'default'
        super(Cache, self).__init__()
        if alternate_hosts is None:
            alternate_hosts = []

        self._namespace = '{global_ns}{sep}{ns}{sep}'.format(sep=self.sep, global_ns=self.global_ns, ns=namespace)

        monitoring_key_formatting = '{prefix}{sep}{ns}{suffix}'
        self._hits_key = monitoring_key_formatting.format(
            sep=self.sep, prefix=self.monitoring_prefix, ns=self._namespace, suffix=self.hits_suffix)
        self._misses_key = monitoring_key_formatting.format(
            sep=self.sep, prefix=self.monitoring_prefix, ns=self._namespace, suffix=self.misses_suffix)

        self._expire_time = expire_time
        self._redis = StrictRedis(socket_timeout=60,**self._convert_host(host))
        self._lua_get = self._redis.register_script(lua_get)

        self._alternate_redises = []
        if isinstance(alternate_hosts, (list, tuple, set)):
            for alternate_host in set(alternate_hosts):
                if alternate_host != host:
                    self._alternate_redises.append(StrictRedis(socket_timeout=1, **self._convert_host(alternate_host)))
        else:
            raise TypeError('alternate_hosts must be a list, tuple, set or None')

    def get(self, key):
        """
        Get value corresponding to the given key, from the redis cache.

        Returns None if there is no match.

        :param basestring key: the key for the cached value
        :return: value saved in redis server.
        """
        value = self._lua_get([self._add_namespace_prefix(key),
                               self._hits_key,
                               self._misses_key])
        return value

    def set(self, key, value, expire_seconds=None, expire_milliseconds=None,
            only_if_new=False, only_if_old=False):
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
        """
        name = self._add_namespace_prefix(key)
        return self._redis.set(
            name, value,
            self._expire_time if expire_seconds is None else expire_seconds,
            expire_milliseconds, only_if_new, only_if_old)

    def hits(self):
        return int(self._redis.get(self._hits_key) or '0')

    def misses(self):
        return int(self._redis.get(self._misses_key) or '0')

    def hit_rate(self):
        hits = self.hits()
        misses = self.misses()
        count = hits + misses
        if count == 0:
            return 0
        return 1.0 * hits / (hits + misses)

    def memory_size(self):
        raw_keys = self._keys_with_namespace()
        if raw_keys:
            raw_values = self._redis.mget(raw_keys)
        else:
            raw_values = []

        return self._calculate_size(raw_keys) + self._calculate_size(raw_values)

    def get_keys(self, pattern='*'):
        """
        Get cleaned up keys (the namespace this class adds will be stripped)
        in the redis cache.

        It searches for keys by pattern
        (which will have the namespace implicitly added).

        - ? matches one character
        - * matches non or many characters
        - [] matches one specific characters like regexp
        - \ escapes special characters.

        :param basestring pattern: a pattern string,
               the namespace will be implicitly added.
        :return: a list of matched keys without namespace prefix.
        """
        return [self._strip_namespace_prefix(name)
                for name in self._keys_with_namespace(pattern)]

    def delete(self, *keys):
        """
        Delete all entries that match the given keys from the
        namespaced redis cache.

        This method will delete keys from all the alternate hosts, too.

        :param keys: a list of keys (not patterns)
        """
        if keys:
            raw_keys = [self._add_namespace_prefix(key) for key in keys]
            self._redis.delete(*raw_keys)
            for alternate_redis in self._alternate_redises:
                try:
                    alternate_redis.delete(*raw_keys)
                except (ConnectionError, TimeoutError) as e:
                    logger.debug(str(e))

    def clear(self):
        """
        Clear all the keys from all the servers in this namespace.

        This will match keys from all the server, then delete them.
        """
        for redis in [self._redis] + self._alternate_redises:
            raw_keys = redis.keys(self._add_namespace_prefix('*'))
            if raw_keys:
                redis.delete(*raw_keys)

    @classmethod
    def _calculate_size(cls, something):
        return sum(len(item) for item in something if isinstance(item, basestring))

    @classmethod
    def _convert_host(cls, host):
        l = host.split(':')
        if len(l) == 1:
            return {'host': l[0], 'port': 6379}
        elif len(l) == 2:
            return {'host': l[0], 'port': int(l[1])}
        else:
            raise ValueError('{} is not a normal host.'.format(host))

    def _add_namespace_prefix(self, key):
        """
        Add namespace to a simple key string as a prefix like {namespace}:{key}

        :param basestring key: a simple key string.
        """
        return '{ns}{key}'.format(ns=self._namespace, key=key)

    def _strip_namespace_prefix(self, key):
        """
        Strip namespace from a hard key string like {namespace}:{key}
        then only return {key}.

        :param str|unicode key: a hard key string.
        """
        return _strip(key, self._namespace)

    def _keys_with_namespace(self, pattern='*'):
        """
        Get raw redis keys (ie including the namespace that this class adds).

        Searching is done by pattern
        (which will have the namespace implicitly added).

        :param basestring pattern: a pattern string.
        :return: a list of matched keys, including the namespace
        """
        return self._redis.keys(self._add_namespace_prefix(pattern))
