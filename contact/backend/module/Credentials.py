#!/usr/bin/python
# coding:utf-8

from Global import default


def _clear(number):
        result = []
        while number:
            result.append(chr(number % 128))
            number >>= 7
        return ''.join(reversed(result))


def Credentials(auth_type='db', city=default['city']):    
    credentials = {'BJ': {}, 'WX': {}, 'XM': {}, 'LA': {}, 'DC': {}, 'KL': {}}
    credentials['BJ']['linux-simple'] = ('root', _clear(55599684644640946))
    credentials['BJ']['ple-tools-db'] = ('ple', _clear(675655278160864618085))
    credentials['BJ']['ldap'] = ('uid=root,cn=users,dc=xserver,dc=base-fx,dc=com', _clear(142739024786090804172849))
    credentials['BJ']['ad'] = ('cn=Administrator,cn=users,dc=ad,dc=base-fx,dc=com', _clear(938724368017542699568))
    credentials['BJ']['snmp'] = ('basenet')
    credentials['BJ']['localhost'] = ('root', _clear(55599684644640946))
    credentials['XM']['localhost'] = ('root', _clear(55599684644640946))
    credentials['WX']['localhost'] = ('root', _clear(55599684644640946))
    credentials['BJ']['switches'] = ('basefx', _clear(55599684644640946))
    credentials['qubedb'] = ('qube_admin',_clear(65753674419924920))
    credentials['BJ']['qube.base-fx.com'] = credentials['qubedb']
    credentials['BJ']['qube.bj.base-fx.com'] = credentials['qubedb']
    credentials['WX']['qube.wx.base-fx.com'] = credentials['qubedb']
    credentials['XM']['qube.xm.base-fx.com'] = credentials['qubedb']
    credentials['XM']['qube.kl.base-fx.com'] = credentials['qubedb']
    credentials['XM']['qube.dc.base-fx.com'] = credentials['qubedb']
    credentials['BJ']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['WX']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['XM']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['LA']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['DC']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['KL']['xen-master.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['BJ']['xen22.base-fx.com'] = ('itd', _clear(434545571551329))
    credentials['db'] = ('itd',_clear(63840988175379178))
    credentials['BJ']['db.base-fx.com'] = credentials['db']
    credentials['KL']['db.base-fx.com'] = credentials['db']
    credentials['DC']['db.base-fx.com'] = credentials['db']
    credentials['WX']['db.base-fx.com'] = credentials['db']
    credentials['XM']['db.base-fx.com'] = credentials['db']
    credentials['BJ']['dbd.base-fx.com'] = credentials['db']
    credentials['KL']['dbd.base-fx.com'] = credentials['db']
    credentials['DC']['dbd.base-fx.com'] = credentials['db']
    credentials['WX']['dbd.base-fx.com'] = credentials['db']
    credentials['XM']['dbd.base-fx.com'] = credentials['db']

    try:
        return credentials[city.upper()][auth_type]
    except:
        return credentials['BJ']['linux-simple']


def DBCredentials(dbname=None):
    dbs = {}
    default = {
        'Host': 'db.base-fx.com',
        'Timeout': 30,
        'CharSet': 'utf8',
        'User': None,
        'Password': None,
        'Database': None,
    }

    dbs['root'] = default.copy()
    dbs['root']['User'] = 'root'
    dbs['root']['Password'] = 'basefx12'
    dbs['root']['Database'] = None

    dbs['switches_for_marc'] = default.copy()
    dbs['switches_for_marc']['Host'] = 'db01.base-fx.com'
    dbs['switches_for_marc']['User'] = 'test'
    dbs['switches_for_marc']['Password'] = 'test.123'
    dbs['switches_for_marc']['Database'] = 'switches_for_marc'

    dbs['switches'] = default.copy()
    dbs['switches']['User'] = 'networker'
    dbs['switches']['Password'] = 'goodgollymissmolly'
    dbs['switches']['Database'] = 'switches'

    dbs['switches_load'] = default.copy()
    dbs['switches_load']['Host'] = 'db01.base-fx.com'
    dbs['switches_load']['User'] = 'networker'
    dbs['switches_load']['Password'] = 'goodgollymissmolly'
    dbs['switches_load']['Database'] = 'switches'

    dbs['inventory_RO'] = default.copy()
    dbs['inventory_RO']['User'] = 'readonly'
    dbs['inventory_RO']['Password'] = 'readonly'
    dbs['inventory_RO']['Database'] = 'inventory_new'

    dbs['dns'] = default.copy()
    dbs['dns']['Host'] = 'db08.base-fx.com'
    dbs['dns']['User'] = 'dns'
    dbs['dns']['Password'] = '4bx#rv3H'
    dbs['dns']['Database'] = 'dns'

    if not dbname:
        return dbs.keys()

    try:
        return dbs[dbname]
    except KeyError:
        return None
