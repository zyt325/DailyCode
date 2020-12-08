from ldap3 import Server, Connection, ALL, NTLM

LDAP_CONFIG={}
LDAP_CONFIG['DOMAIN']='ad'
LDAP_CONFIG['HOST']='dc09.base-fx.com'
LDAP_CONFIG['BASE_DN']='ou=Basers,dc=ad,dc=base-fx,dc=com'
LDAP_CONFIG['USERNAME']='zhangyt'
LDAP_CONFIG['PASSWORD']='b@onpJ32'


class LDAPBackend(object):
    """
    Authenticates with ldap.
    """
    def authenticate_user(self, username, passwd):
        try:
            if self._bind_as(username, passwd):
                return True
        except Exception as e:
            return False

    def _bind(self):
        self._bind_as(LDAP_CONFIG['USERNAME'], LDAP_CONFIG['PASSWORD'])

    def _bind_as(self, bind_dn, bind_password):
        try:
            self._connection = Server(LDAP_CONFIG['HOST'], get_info=ALL)
            bind_dn = '%s\\%s' % (LDAP_CONFIG['DOMAIN'], bind_dn)
            self.c=Connection(self._connection, user=bind_dn, password=bind_password,authentication=NTLM,auto_bind=True)
            print(self.c)
            return True
        except Exception as e:
            return False


# print(LDAPBackend().authenticate_user('zhangyt','7my_9rJg'))

