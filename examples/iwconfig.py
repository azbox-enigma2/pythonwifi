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
import getopt
import sys
import types

import pythonwifi.flags
from pythonwifi.iwlibs import Wireless, WirelessInfo, getNICnames, getWNICnames

def getBitrate(wifi):
    """ Return formatted string with Bit Rate info. """
    try:
        bitrate = wifi.wireless_info.getBitrate()
    except IOError, (errno, strerror):
        return None
    else:
        if bitrate.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Bit Rate%c%s   " % (fixed, wifi.getBitrate())

def getTXPower(wifi):
    """ Return formatted string with TXPower info. """
    try:
        txpower = wifi.wireless_info.getTXPower()
    except IOError, (errno, strerror):
        return None
    else:
        if txpower.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Tx-Power%c%s   " % (fixed, wifi.getTXPower())

def getSensitivity(wifi):
    """ Return formatted string with Sensitivity info. """
    try:
        sensitivity = wifi.wireless_info.getSensitivity()
    except IOError, (errno, strerror):
        return None
    else:
        if sensitivity.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Sensitivity%c%d/65535" % (fixed, wifi.getSensitivity())

def getRetrylimit(wifi):
    """ Return formatted string with Retry info. """
    try:
        retry = wifi.wireless_info.getRetry()
    except IOError, (errno, strerror):
        return None
    else:
        return "Retry limit:%s   " % (wifi.getRetrylimit(), )

def getRTS(wifi, wifi_details):
    """ Return formatted string with RTS info. """
    try:
        rts = wifi_details.getRTS()
    except IOError, (errno, strerror):
        return None
    else:
        if rts.disabled:
            return "RTS thr:off   "
        if rts.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "RTS thr%c%d B   " % (fixed, wifi.getRTS())

def getFragmentation(wifi, wifi_details):
    """ Return formatted string with Fragmentation info. """
    try:
        frag = wifi_details.getFragmentation()
    except IOError, (errno, strerror):
        return None
    else:
        if frag.disabled:
            return "Fragment thr:off"
        if frag.fixed:
            fixed = "="
        else:
            fixed = ":"
        return "Fragment thr%c%d B   " % (fixed, wifi.getFragmentation())

def getEncryption(wifi, wifi_details):
    """ Return formatted string with Encryption info.

    As noted in iwconfig.c: we display only the "current" key, use iwlist
    to list all keys.

    """
    #try:
    enc = wifi_details.getEncryption()
    #except IOError, (errno, strerror):
        #print errno, strerror
        #return None
    #else:
    if (enc.flags & pythonwifi.flags.IW_ENCODE_DISABLED):
        key = "Encryption key:off"
    else:
        key = "Encryption key:%s" % (wifi.getKey(), )
    if ((enc.flags & pythonwifi.flags.IW_ENCODE_INDEX) > 1):
        index = " [%d]" % (enc.flags & pythonwifi.flags.IW_ENCODE_INDEX, )
    else:
        index = ""
    if ((enc.flags & pythonwifi.flags.IW_ENCODE_RESTRICTED) > 0):
        mode = "   Security mode:restricted"
    elif ((enc.flags & pythonwifi.flags.IW_ENCODE_OPEN) > 0):
        mode = "   Security mode:open"
    else:
        mode = ""
    return "%s%s%s" % (key, index, mode)

def iwconfig(interface):
    """ Get wireless information from the device driver. """
    if interface not in getWNICnames():
        print "%-8.16s  no wireless extensions." % (interface, )
    else:
        wifi = Wireless(interface)
        print """%-8.16s  %s  ESSID:"%s" """ % (interface,
            wifi.getWirelessName(), wifi.getEssid())
        print """\t  Mode:%s  Frequency:%s  Access Point:%s""" % (wifi.getMode(),
            wifi.getFrequency(), wifi.getAPaddr())

        # Bit Rate, TXPower, and Sensitivity line
        bitrate = getBitrate(wifi)
        print "\t ",
        if bitrate:
        txpower = getTXPower(wifi)
            print bitrate,
        if txpower:
        sensitivity = getSensitivity(wifi)
            print txpower,
        if sensitivity:
            print sensitivity,
        print

        # Retry, RTS, and Fragmentation line
        retry = getRetrylimit(wifi)
        print "\t ",
        if retry:
            print retry,
        rts = getRTS(wifi, wifi_details)
        if rts:
            print rts,
        fragment = getFragmentation(wifi, wifi_details)
        if fragment:
            print fragment,
        print

        print "\t ",
        print getEncryption(wifi, wifi_details),
        print

        pm = wifi.getPowermanagement()
        print """\t  Power Management:%s""" % (pm[0], )

        stat, qual, discard, missed_beacon = wifi.getStatistics()
        print """\t  Link Quality:%s/100  Signal level:%sdBm  Noise level:%sdBm""" % \
            (qual.quality, qual.signallevel, qual.noiselevel)
        print """\t  Rx invalid nwid:%s  Rx invalid crypt:%s  Rx invalid frag:%s""" % \
            (discard['nwid'], discard['code'], discard['fragment'],)
        print """\t  Tx excessive retries:%s  Invalid misc:%s   Missed beacon: %s""" % \
            (discard['retries'], discard['misc'], missed_beacon)

    print

def usage():
    """ Print info about using iwconfig.py. """
    print """Usage: iwconfig.py [interface]
                interface essid {NNN|any|on|off}
                interface mode {managed|ad-hoc|master|...}
                interface freq N.NNN[k|M|G]
                interface channel N
                interface bit {N[k|M|G]|auto|fixed}
                interface rate {N[k|M|G]|auto|fixed}
                interface enc {NNNN-NNNN|off}
                interface key {NNNN-NNNN|off}
                interface power {period N|timeout N|saving N|off}
                interface nickname NNN
                interface nwid {NN|on|off}
                interface ap {N|off|auto}
                interface txpower {NmW|NdBm|off|auto}
                interface sens N
                interface retry {limit N|lifetime N}
                interface rts {N|auto|fixed|off}
                interface frag {N|auto|fixed|off}
                interface modulation {11g|11a|CCK|OFDMg|...}
                interface commit 
       Check man pages for more details."""

def version_info():
    """ Print version info for iwconfig.py, Wireless Extensions compatibility,
        and Wireless Extensions version in the kernel.

    """
    pass

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"])
    except getopt.GetoptError, error_str:
        # invalid options will be taken to be interface name
        pass
    else:
        try:
            if opts[0][0] in ("-h", "--help"):
                usage()
        except:
            try:
                if opts[0][0] in ("-v", "--version"):
                    version_info()
            except:
                if len(args) == 0:
                    # no params given to iwconfig.py
                    for interface in getNICnames():
                        iwconfig(interface)
                if len(args) == 1:
                    # one param given to iwconfig.py, it should be a network device
                    if sys.argv[1] in getNICnames():
                        iwconfig(sys.argv[1])


if __name__ == "__main__":
    main()
