#!/usr/bin/env python
import unittest
import types
from iwlibs import Wireless, getNICnames

class TestWireless(unittest.TestCase):

    def setUp(self):
        ifnames = getNICnames()
        self.wifi = Wireless(ifnames[0])
        
    def test_wirelessMethods(self):
        # test all wireless methods that they don't return an error
        # 'getBitrates' and 'getChannelInfo' are not tested here,
        # because they return tuples as a normal result
        methods = ['getAPaddr',
                   'getBitrate',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getWirelessName',
                   'getPowermanagement',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'getStatistics']

        # None of the methods should return something different then '0'
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is not types.TupleType,
                         '%s is a TupleType: %s' % (m, result))
        
        # the user is not allowed to run this method
        result = self.wifi.getEncryption()
        self.assert_(result[0] == 1)

    def test_wirelessWithNonWifiCard(self):
        self.wifi.ifname = 'eth0'
        methods = ['getAPaddr',
                   'getBitrate',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getWirelessName',
                   'getPowermanagement',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'getStatistics']
    
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is types.TupleType)
            self.assertEquals(result[0], 95)
        
    
    def test_wirelessWithNonExistantCard(self):
        self.wifi.ifname = 'eth5'
        methods = ['getAPaddr',
                   'getBitrate',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getWirelessName',
                   'getPowermanagement',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'getStatistics']
    
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is types.TupleType, 
                         "%s returns not a TupleType: %s" %(m, result))
            self.assertEquals(result[0], 19)
        
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestWireless))
unittest.TextTestRunner(verbosity=2).run(suite)
