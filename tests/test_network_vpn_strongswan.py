#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

import accounts
import utils
import utils_dbus

from dbus_gen.com_deepin_daemon_Network import Network
from dbus_gen.com_deepin_daemon_Network_ConnectionSession import ConnectionSession

dbus_network = Network('com.deepin.daemon.Network', '/com/deepin/daemon/Network')

class TestNetworkVpnStrongswan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.run_make_cmd("start-service-vpn-strongswan")

    @classmethod
    def tearDownClass(cls):
        utils.run_make_cmd("stop-service-vpn-strongswan")

    def test_backend_strongswan_privatekey(self):
        session_path = utils_dbus.create_connection('vpn-strongswan', '/')
        dbus_session = ConnectionSession('com.deepin.daemon.Network', session_path)
        uuid = dbus_session.Uuid
        dbus_session.SetKey('alias-vpn-strongswan', 'address', json.dumps(utils.get_ansible_server_host()))
        dbus_session.SetKey('alias-vpn-strongswan', 'certificate', json.dumps(accounts.vpn_strongswan_cacert))
        dbus_session.SetKey('alias-vpn-strongswan', 'method', json.dumps('key'))
        dbus_session.SetKey('alias-vpn-strongswan', 'usercert', json.dumps(accounts.vpn_strongswan_clientcert))
        dbus_session.SetKey('alias-vpn-strongswan', 'userkey', json.dumps(accounts.vpn_strongswan_clientkey))
        dbus_session.SetKey('alias-vpn-strongswan', 'virtual', json.dumps(True)) # request an inner IP address
        self.assertTrue(dbus_session.Save())
        utils_dbus.test_active_connection(self, uuid, "/")

    @unittest.skip("could not define password for eap method so the password input dialog will be popup now")
    def test_backend_strongswan_eap(self):
        session_path = utils_dbus.create_connection('vpn-strongswan', '/')
        dbus_session = ConnectionSession('com.deepin.daemon.Network', session_path)
        uuid = dbus_session.Uuid
        dbus_session.SetKey('alias-vpn-strongswan', 'address', json.dumps(utils.get_ansible_server_host()))
        dbus_session.SetKey('alias-vpn-strongswan', 'certificate', json.dumps(accounts.vpn_strongswan_cacert))
        dbus_session.SetKey('alias-vpn-strongswan', 'method', json.dumps('eap'))
        dbus_session.SetKey('alias-vpn-strongswan', 'user', json.dumps(accounts.vpn_strongswan_username))
        # TODO
        # dbus_session.SetKey('alias-vpn-strongswan', 'password', json.dumps(accounts.vpn_strongswan_password))
        dbus_session.SetKey('alias-vpn-strongswan', 'virtual', json.dumps(True)) # request an inner IP address
        self.assertTrue(dbus_session.Save())
        utils_dbus.test_active_connection(self, uuid, "/")
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
