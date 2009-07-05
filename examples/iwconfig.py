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
from pythonwifi.iwlibs import Wireless, WirelessInfo, Iwrange, getNICnames, getWNICnames

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
        iwrange = Iwrange(wifi.ifname)
        return "Sensitivity%c%d/%d  " % (
            fixed, wifi.getSensitivity(), iwrange.sensitivity)

def getRetrylimit(wifi):
    """ Return formatted string with Retry info. """
    try:
        retry = wifi.wireless_info.getRetry()
    except IOError, (errno, strerror):
        return None
    else:
        modifier = ""
        if (retry.flags & pythonwifi.flags.IW_RETRY_MIN):
            modifier = " min"
        elif (retry.flags & pythonwifi.flags.IW_RETRY_MAX):
            modifier = " max"
        elif (retry.flags & pythonwifi.flags.IW_RETRY_SHORT):
            modifier = " short"
        elif (retry.flags & pythonwifi.flags.IW_RETRY_LONG):
            modifier = "  long"
        type = " limit"
        if (retry.flags & pythonwifi.flags.IW_RETRY_LIFETIME):
            type = " lifetime"
        return "Retry%s%s:%s   " % (modifier, type, wifi.getRetrylimit())

def getRTS(wifi):
    """ Return formatted string with RTS info. """
    try:
        rts = wifi.wireless_info.getRTS()
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

def getFragmentation(wifi):
    """ Return formatted string with Fragmentation info. """
    try:
        frag = wifi.wireless_info.getFragmentation()
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

def getEncryption(wifi):
    """ Return formatted string with Encryption info.

        As noted in iwconfig.c: we display only the "current" key, use iwlist
        to list all keys.

    """
    #try:
    enc = wifi.wireless_info.getEncryption()
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

def getPowerManagement(wifi):
    """ Return formatted string with Power Management info. """
    pm = wifi.getPowermanagement()
    return "Power Management:%s" % (pm[0], )

def iwconfig(interface):
    """ Get wireless information from the device driver. """
    if interface not in getWNICnames():
        print "%-8.16s  no wireless extensions." % (interface, )
    else:
        wifi = Wireless(interface)
        print """%-8.16s  %s  ESSID:"%s" """ % (interface,
            wifi.getWirelessName(), wifi.getEssid())
        if (wifi.wireless_info.getMode() == pythonwifi.flags.IW_MODE_ADHOC):
            ap_type = "Cell"
        else:
            ap_type = "Access Point"
        ap_addr = wifi.getAPaddr()
        if (ap_addr == "00:00:00:00:00:00"):
            ap_addr = "Not-Associated"
        print """          Mode:%s  Frequency:%s  %s: %s""" % (
            wifi.getMode(), wifi.getFrequency(), ap_type, ap_addr)

        # Bit Rate, TXPower, and Sensitivity line
        line = "          "
        bitrate = getBitrate(wifi)
        if bitrate:
            line = line + bitrate
        txpower = getTXPower(wifi)
        if txpower:
            line = line + txpower
        sensitivity = getSensitivity(wifi)
        if sensitivity:
            line = line + sensitivity
        print line

        # Retry, RTS, and Fragmentation line
        line = "          "
        retry = getRetrylimit(wifi)
        if retry:
            line = line + retry
        rts = getRTS(wifi)
        if rts:
            line = line + rts
        fragment = getFragmentation(wifi)
        if fragment:
            line = line + fragment
        print line

        # Encryption line
        line = "          "
        line = line + getEncryption(wifi)
        print line

        # Power Management line
        line = "          "
        line = line + getPowerManagement(wifi)
        print line

        stat, qual, discard, missed_beacon = wifi.getStatistics()

        # Link Quality, Signal Level and Noise Level line
        line = "          "
        line = line + "Link Quality:%s/100  " % (qual.quality, )
        line = line + "Signal level:%sdBm  " % (qual.signallevel, )
        line = line + "Noise level:%sdBm" % (qual.noiselevel, )
        print line

        # Rx line
        line = "          "
        line = line + "Rx invalid nwid:%s  " % (discard['nwid'], )
        line = line + "Rx invalid crypt:%s  " % (discard['code'], )
        line = line + "Rx invalid frag:%s" % (discard['fragment'], )
        print line

        # Tx line
        line = "          "
        line = line + "Tx excessive retries:%s  " % (discard['retries'], )
        line = line + "Invalid misc:%s   " % (discard['misc'], )
        line = line + "Missed beacon:%s" % (missed_beacon, )
        print line

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
