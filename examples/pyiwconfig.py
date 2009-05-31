#!/usr/bin/env python
# Copyright 2004, 2005 Roman Joost <roman@bromeco.de> - Rotterdam, Netherlands
# Copyright 2009 by Sean Robinson <seankrobinson@gmail.com>
#
# This file is part of Python WiFi
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
import sys
import types
from pythonwifi.iwlibs import Wireless, WirelessInfo, getNICnames

def getBitrate(wifi, wifi_details):
    """ Return formatted string with Bit Rate info. """
    try:
        bitrate = wifi_details.getBitrate()
    except IOError, (errno, strerror):
        return None
    else:
        if bitrate.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Bit Rate%c%s   " % (fixed, wifi.getBitrate())

def getTXPower(wifi, wifi_details):
    """ Return formatted string with TXPower info. """
    try:
        txpower = wifi_details.getTXPower()
    except IOError, (errno, strerror):
        return None
    else:
        if txpower.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Tx-Power%c%s   " % (fixed, wifi.getTXPower())

def getSensitivity(wifi, wifi_details):
    """ Return formatted string with Sensitivity info. """
    try:
        sensitivity = wifi_details.getSensitivity()
    except IOError, (errno, strerror):
        return None
    else:
        if sensitivity.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Sensitivity%c%d/65535" % (fixed, wifi.getSensitivity())

def getRetrylimit(wifi, wifi_details):
    """ Return formatted string with Retry info. """
    try:
        retry = wifi_details.getRetry()
    except IOError, (errno, strerror):
        return None
    else:
        return "Retry limit:%s  " % (wifi.getRetrylimit(), )

def iwconfig():
    """ get wireless information from the device driver """
    ifnames = getNICnames()
    if ifnames == []:
        print "no WLAN devices found"
        return 1

    for name in ifnames:
        wifi = Wireless(name)
        wifi_details = WirelessInfo(name)
        print """%-8.16s  %s  ESSID:"%s" """ % (name,
            wifi.getWirelessName(), wifi.getEssid())
        print """\t  Mode:%s  Frequency:%s  Access Point:%s""" % (wifi.getMode(),
            wifi.getFrequency(), wifi.getAPaddr())

        print "\t ",
        bitrate = getBitrate(wifi, wifi_details)
        if bitrate:
            print bitrate,
        txpower = getTXPower(wifi, wifi_details)
        if txpower:
            print txpower,
        sensitivity = getSensitivity(wifi, wifi_details)
        if sensitivity:
            print sensitivity,
        print

        # Retry, RTS, and Fragmentation line
        print "\t ",
        retry = getRetrylimit(wifi, wifi_details)
        if retry:
            print retry,
        print
        print """\t  Encryption key:%s""" % (wifi.getEncryption(), )

        pm = wifi.getPowermanagement()
        print """\t  Power Management:%s""" % (pm[0], )

        stat, qual, discard, missed_beacon = wifi.getStatistics()
        print """\t  Link Quality:%s/100  Signal level:%sdBm  Noise level:%sdBm""" % \
            (qual.quality, qual.signallevel, qual.noiselevel)
        print """\t  Rx invalid nwid:%s  Rx invalid crypt:%s  Rx invalid frag:%s""" % \
            (discard['nwid'], discard['code'], discard['fragment'],)
        print """\t  Tx excessive retries:%s  Invalid misc:%s   Missed beacon: %s""" % \
            (discard['retries'], discard['misc'], missed_beacon)


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
