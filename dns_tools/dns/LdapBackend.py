from ldap3 import Server, Connection, ALL, NTLM, SUBTREE

LDAP_CONFIG = {'HOST': 'pdc.base-fx.com', 'SSL': False, 'base_dn': 'ou=Basers,dc=ad,dc=base-fx,dc=com', }


# user（如domain\Administrator）和passwod为登录域控服务器的账户密码

class LDAPBackend(object):
    """
    Authenticates with ldap.
    """

    def authenticate(self, username=None, passwd=None, **kwargs):
        if not username or not passwd:
            return None
        if self._authenticate_user(username, passwd):
            return username
        else:
            return None

    def _authenticate_user(self, username, passwd):
        try:
            conn = Connection(self._connection(), "ad\%s" % username, passwd, auto_bind=True, authentication=NTLM)
            if conn:
                dep = self._get_user_dep(conn, username)
                print(dep)
                if dep in ['ITD']:
                    return 1
            return 0
        except:
            return 0

    def _connection(self):
        server = Server(LDAP_CONFIG['HOST'], use_ssl=LDAP_CONFIG['SSL'], get_info=ALL)
        return server

    def _get_user_dep(self, conn, user):
        try:
            conn.search(search_base=LDAP_CONFIG['base_dn'], search_filter="(&(objectClass=user)(cn=%s))" % user,
                        search_scope=SUBTREE, attributes=['department'])
            return conn.response[0]['attributes']['department']
        except:
            return None

# print(LDAPBackend().authenticate('zhangyt', '7my_9rJg'))
