import ldap
from django_auth_ldap.backend import LDAPBackend
from django_auth_ldap.config import GroupOfNamesType
from django_auth_ldap.config import LDAPGroupQuery
from django_auth_ldap.config import LDAPSearch

BASE_LDAP_CONFIG = dict(
    AUTH_LDAP_BJ_USER_DN_TEMPLATE='CN=%(user)s,OU=PRD,OU=BJ,OU=Basers,DC=ad,DC=base-fx,DC=com',
    AUTH_LDAP_XM_USER_DN_TEMPLATE='CN=%(user)s,OU=PRD,OU=XM,OU=Basers,DC=ad,DC=base-fx,DC=com',

    AUTH_LDAP_SERVER_URI='ldap://pdc.base-fx.com',
    AUTH_LDAP_USER_DN_TEMPLATE='CN=%(user)s,OU=Basers,DC=ad,DC=base-fx,DC=com',
    AUTH_LDAP_GROUP_SEARCH=LDAPSearch("CN=tech,OU=Basers,DC=ad,DC=base-fx,DC=com",
                                      ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)", ),
    AUTH_LDAP_GROUP_TYPE=GroupOfNamesType(name_attr="cn"),
    AUTH_LDAP_USER_ATTR_MAP={"first_name": "givenName", "last_name": "sn"},
    AUTH_LDAP_USER_FLAGS_BY_GROUP={
        "is_active": "CN=PLE,OU=Basers,DC=ad,DC=base-fx,DC=com",
        "is_staff": (LDAPGroupQuery("CN=PLE,OU=Basers,DC=ad,DC=base-fx,DC=com"),),
        "is_superuser": "CN=PLE,OU=Basers,DC=ad,DC=base-fx,DC=com"
    }
)


class BaseLDAPSettings(LDAPBackend):
    defaults = {
        'ALWAYS_UPDATE_USER': True,
        'AUTHORIZE_ALL_USERS': False,
        'BIND_AS_AUTHENTICATING_USER': False,
        'BIND_DN': '',
        'BIND_PASSWORD': '',
        'CACHE_GROUPS': False,
        'CONNECTION_OPTIONS': {},
        'DENY_GROUP': None,
        'FIND_GROUP_PERMS': False,
        'GROUP_CACHE_TIMEOUT': None,
        'GROUP_SEARCH': None,
        'GROUP_TYPE': None,
        'MIRROR_GROUPS': None,
        'MIRROR_GROUPS_EXCEPT': None,
        'PERMIT_EMPTY_PASSWORD': False,
        'PROFILE_ATTR_MAP': {},
        'PROFILE_FLAGS_BY_GROUP': {},
        'REQUIRE_GROUP': None,
        'SERVER_URI': 'ldap://localhost',
        'START_TLS': False,
        'USER_ATTRLIST': None,
        'USER_ATTR_MAP': {},
        'USER_DN_TEMPLATE': None,
        'USER_FLAGS_BY_GROUP': {},
        'USER_SEARCH': None,
    }

    def __init__(self, prefix='AUTH_LDAP_', location=None, defaults={}):
        self._prefix = prefix
        defaults = dict(self.defaults, **defaults)
        for name, default in defaults.items():
            if name == 'USER_DN_TEMPLATE':
                config_name = ''.join([prefix, location, '_', name])
            else:
                config_name = prefix + name
            value = BASE_LDAP_CONFIG.get(config_name, default)
            setattr(self, name, value)


class BaseLDAPBackend(LDAPBackend):
    """ To differentiate _USER_DN_TEMPLATE according to our own ldap"""

    def _set_settings(self, settings):
        self._settings = settings

    def _get_settings(self):
        if self._settings is None:
            self._settings = BaseLDAPSettings(self.settings_prefix,
                                              self.location,
                                              self.default_settings)
        return self._settings
    settings = property(_get_settings, _set_settings)


class LDAPBackendBJ(BaseLDAPBackend):
    """Make ldap search in 'CN=%(user)s,OU=PRD,OU=BJ,OU=Basers,DC=ad,DC=base-fx,DC=com' """
    location = 'BJ'


class LDAPBackendXM(BaseLDAPBackend):
    """Make ldap search in 'CN=%(user)s,OU=PRD,OU=XM,OU=Basers,DC=ad,DC=base-fx,DC=com' """
    location = 'XM'
