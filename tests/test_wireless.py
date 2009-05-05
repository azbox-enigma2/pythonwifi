#!/usr/bin/env python
# Copyright 2004-2008 Roman Joost <roman@bromeco.de> - Rotterdam, Netherlands
# this file is part of the python-wifi package - a python wifi library
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import errno
import unittest
import types
from pythonwifi.iwlibs import Wireless, getNICnames
from pythonwifi.flags import modes

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
                   'getQualityMax',
                   'getQualityAvg',
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
        # test setMode
        old_mode = self.wifi.getMode()                   # save current mode for later restoration
        self.wifi.setMode('Monitor')
        self.assert_(self.wifi.getMode() == 'Monitor')
        self.wifi.setMode(old_mode)                      # restore mode
        
        # test setEssid
        old_mode = self.wifi.getEssid()                  # save current ESSID for later restoration
        self.wifi.setEssid('Joost')
        self.assert_(self.wifi.getEssid() == 'Joost')
        self.wifi.setEssid(old_mode)                     # restore ESSID


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
                   'getQualityMax',
                   'getQualityAvg',
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
                   'getQualityMax',
                   'getQualityAvg',
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
