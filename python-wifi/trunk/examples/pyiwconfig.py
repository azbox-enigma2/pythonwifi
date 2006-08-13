#!/usr/bin/env python
# -*- coding: latin1 -*-
# python-wifi -- a wireless library to access wireless cards via python
# Copyright (C) 2004-2005 Róman Joost
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public License
#    as published by the Free Software Foundation; either version 2.1 of
#    the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#    USA 
import sys
import types
from pythonwifi.iwlibs import Wireless, getNICnames


def iwconfig():
    """ get wireless information from the device driver """
    ifnames = getNICnames()
    if ifnames == []:
        print "no WLAN devices found"
        return 1
    
    for name in ifnames:
        wifi = Wireless(name)
        stat, qual, discard, missed_beacon = wifi.getStatistics()
        print """%s  %s  ESSID:"%s"
        Mode:%s  Frequency:%s  Access Point:%s
        Bit Rate:%s   Tx-Power:%s   Sensitivity:%s/65535
        Retry limit:%s  RTS thr:%s   Fragment thr:%s
        Encryption:%s
        Power Management:%s
        Link Quality:%s/100  Signal level:%sdBm  Noise level:%sdBm
        Rx invalid nwid:%s  Rx invalid crypt:%s  Rx invalid frag:%s
        Tx excessive retries:%s  Invalid misc:%s   Missed beacon: %s
        """ %(name, wifi.getWirelessName(), wifi.getEssid(),
        wifi.getMode(), wifi.getFrequency(), wifi.getAPaddr(),
        wifi.getBitrate(), wifi.getTXPower(), wifi.getSensitivity(), 
        wifi.getRetrylimit(), wifi.getRTS(), wifi.getFragmentation(), 
        wifi.getEncryption(),
        wifi.getPowermanagement(), 
        qual.quality, qual.signallevel, qual.noiselevel,
        discard['nwid'], discard['code'], discard['fragment'],
        discard['retries'], discard['misc'], missed_beacon)
        
def main():
    if len(sys.argv) > 1:
        try:
            ifname, option, value = sys.argv[1:]
        except ValueError:
            usage()
            sys.exit(2)
    else:
        iwconfig()
        sys.exit(1)
   
    ifnames = getNICnames()
    if ifnames == []:
        print "No wireless devices present or incompatible OS."
        sys.exit(0)
    # find out if the user passed a valid device
    try:
        ifnames.index(ifname)
    except IndexError:
        print "You passed an invalid interface name."
        sys.exit(0)
        
    wifi = Wireless(ifname)
    if option == 'mode':
        val = wifi.setMode(value)
    else:
        print "\nSorry, this is an invalid option you passed!\n"
        usage()
    
    #if type(val) is types.StringType:
    #        print "%s" %val
        
    
def usage():
    print """iwconfig.py - Copyright 2004-2005 Roman Joost
Configure a wireless network interface via Python. This programm is
a frontend tool, to the Wireless Library for Python.

usage: pyiwconfig IFNAME option value

    options:    value:
        mode    Auto, Ad-Hoc, Managed, Master, Repeater, Secondary,
                Montior"""

    

if __name__ == "__main__":
    main()
