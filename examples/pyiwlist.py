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

import pythonwifi.flags
from pythonwifi.iwlibs import Wireless, Iwrange, getNICnames

def print_scanning_results(wifi):
    """ Print the access points detected nearby.

    """
    try:
        results = wifi.scan()
    except IOError, (errno, strerror):
        print "%s" % (strerror, )
        sys.exit(0)

    (num_channels, frequencies) = wifi.getChannelInfo()
    index = 1
    for ap in results:
        print "          Cell %02d - Address: %s" % (index, ap.bssid)
        print "                    ESSID:\"%s\"" % (ap.essid, )
        print "                    Mode:%s" % (ap.mode, )
        print "                    Frequency:%s %s (Channel: %d)" % \
                            (ap.frequency.getFrequency()[:5], ap.frequency.getFrequency()[5:],
                            frequencies.index(ap.frequency.getFrequency()) + 1)
        print "                    Quality=%s/%s  Signal level=%s/%s  Noise level=%s/%s" % \
                            (ap.quality.quality,
                             wifi.getQualityMax().quality,
                             ap.quality.getSignallevel(),
                             "100",
                             ap.quality.getNoiselevel(),
                             "100")
        #print "                    Encryption key:%s" % (ap.encode, )
        if len(ap.rate) > 0:
            print "                    Bit Rates:",
            rate_lines = len(ap.rate) % 5
            rate_remainder = len(ap.rate) - (rate_lines * 5)
            line = 0
            while line < rate_lines:
                print "%s; %s; %s; %s; %s" % tuple(ap.rate[line * 5:(line * 5) + 5])
                print "                              ",
                line = line + 1
            print "%s; "*(rate_remainder - 1) % tuple(ap.rate[line * 5:line * 5 + rate_remainder - 1]),
            sys.stdout.write(ap.rate[line * 5 + rate_remainder - 1])
            print
        index = index + 1

def print_channels(wifi):
    """ Print all frequencies/channels available on the card.

    """
    # XXX The channel information is bogus here, because it just
    # numerates how many channels the card provides, but doesn't give
    # any information about *which* channel *which* frequencies has
    (num_frequencies, channels) = wifi.getChannelInfo()
    current_freq = wifi.getFrequency()
    print "%-8.16s  %02d channels in total; available frequencies :" % \
                (wifi.ifname, num_frequencies)
    for channel in channels:
        print "          Channel %02d : %s %s" % \
                (channels.index(channel)+1, channel[:5], channel[5:])
    print "          Current Channel=%s" % (channels.index(current_freq) + 1, )

def print_bitrates(wifi):
    """ Print all bitrates available on the card.

    """
    num_bitrates, bitrates = wifi.getBitrates()
    if num_bitrates == 0:
        print "\t 0 Bit Rates found."
        sys.exit(0)

    bitrate_type =  type(bitrates[-1]) is types.StringType
    print "%-8.16s  %02d available bit-rates :" % (wifi.ifname, num_bitrates)
    for rate in bitrates:
        # rate is Iwfreq
        # XXX - there are to much bitrates?
        if bitrate_type:
            print "          %s" % rate
        elif rate.getBitrate() is not None:
            print "          %s" % rate.getBitrate()
    print "          Current Bit Rate:%s\n" % wifi.getBitrate()

def print_encryption(wifi):
    """ Print encryption keys on the card.

    """
    keys = wifi.getKeys()
    range_info = Iwrange(wifi.ifname)

    print "%-8.16s  " % (wifi.ifname, )
    print range_info.num_encoding_sizes,
    print "key sizes :",
    for index in range(range_info.num_encoding_sizes - 1):
        print repr(range_info.encoding_size[index] * 8) + ",",
    print repr(range_info.encoding_size[range_info.num_encoding_sizes - 1] * 8) + "bits"
    print "          %d keys available :" % (len(keys), )
    index = 1
    for key in keys:
        print "                [%d]: %s" % (index, key[1])
        index = index + 1
    print "          Current Transmit Key: [%s]" % ("XXX", )
    print "\n"

def format_pm_value(value):
    """ Return formatted PM value.

    """
    if (value >= pythonwifi.iwlibs.MEGA):
        fvalue = "%gs" % (value / pythonwifi.iwlibs.MEGA, )
    else:
        if (value >= pythonwifi.iwlibs.KILO):
            fvalue = "%gms" % (value / pythonwifi.iwlibs.KILO, )
        else:
            fvalue = "%dus" % (value, )
    return fvalue

def print_power(wifi):
    """ Print power management info for the card.

    """
    (pm_capa, power_period, power_timeout, power_saving, power_params) = \
        wifi.getPowermanagement()
    print "%-8.16s " % (wifi.ifname, ),
    if (pm_capa & pythonwifi.flags.IW_POWER_MODE):
        print "Supported modes :"
        if pm_capa & (pythonwifi.flags.IW_POWER_UNICAST_R | 
                    pythonwifi.flags.IW_POWER_MULTICAST_R):
            print "\t\t\to Receive all packets (unicast & multicast)"
            print "\t ",
        if pm_capa & pythonwifi.flags.IW_POWER_UNICAST_R:
            print "\t\to Receive Unicast only (discard multicast)"
            print "\t ",
        if pm_capa & pythonwifi.flags.IW_POWER_MULTICAST_R:
            print "\t\to Receive Multicast only (discard unicast)"
            print "\t ",
        if pm_capa & pythonwifi.flags.IW_POWER_FORCE_S:
            print "\t\to Force sending using Power Management"
            print "\t ",
        if pm_capa & pythonwifi.flags.IW_POWER_REPEATER:
            print "\t\to Repeat multicast"
            print "\t ",
    if (power_period[0] & pythonwifi.flags.IW_POWER_PERIOD):
        if (power_period[0] & pythonwifi.flags.IW_POWER_MIN):
            print "Auto  period  ; ",
        else:
            print "Fixed period  ; ",
        print "min period:%s\n\t\t\t  " % \
                (format_pm_value(power_period[1]), ),
        print "max period:%s\n\t " % (format_pm_value(power_period[2]), ),
    if (power_timeout[0] & pythonwifi.flags.IW_POWER_TIMEOUT):
        if (power_timeout[0] & pythonwifi.flags.IW_POWER_MIN):
            print "Auto  timeout ; ",
        else:
            print "Fixed timeout ; ",
        print "min period:%s\n\t\t\t  " % \
                (format_pm_value(power_timeout[1]), ),
        print "max period:%s\n\t " % (format_pm_value(power_timeout[2]), ),
    if power_params.disabled:
        print "Current mode:off"
    print

def usage():
    print """pyiwlist.py - Copyright 2004-2005 Roman Joost, 2009 Sean Robinson
Get more detailed wireless information from a wireless interface

Usage: pyiwlist [interface] scanning [essid NNN] [last]
                [interface] frequency
                [interface] channel
                [interface] bitrate
                [interface] encryption
                [interface] keys
                [interface] power
                [interface] txpower
                [interface] retry
                [interface] ap
                [interface] accesspoints

"""

def main():
    if len(sys.argv) < 1:
        usage()
        sys.exit(1)
    try:
        # Get the interface and command from command line
        ifname, option = sys.argv[1:]
    except ValueError:
        usage()
        sys.exit(2)

    # Make sure provided interface is a wireless device
    try:
        ifnames = getNICnames()
    except IOError, (errno, strerror):
        print "Error: %s" % (strerror, )
        sys.exit(0)
    if ifnames == []:
        print "No wireless devices present or incompatible OS."
        sys.exit(0)
    try:
        ifnames.index(ifname)
    except ValueError:
        print "%s is not a wireless device." % (ifname, )
        sys.exit(0)

    # build dictionary of commands and functions
    iwcommands = { "s"   : ("scanning", print_scanning_results),
                   "c"   : ("channel", print_channels),
                   "f"   : ("frequency", print_channels),
                   "b"   : ("bitrate", print_bitrates),
                   "ra"  : ("rate", print_bitrates),
                   "en"  : ("encryption", print_encryption),
                   "k"   : ("keys", print_encryption),
                   "po"  : ("power", print_power),
                   "t"   : ("txpower", print_power),
                   #"re" : ("retry", print_retry),
                   #"ap" : ("ap", print_aps),
                   #"ac" : ("accesspoints", print_aps),
                   #"pe" : ("peers", print_aps),
                   #"ev" : ("event", print_event),
                   #"au" : ("auth", print_auth),
                   #"w"  : ("wpakeys", print_wpa),
                   #"g"  : ("genie", print_genie),
                   #"m"  : ("modulation", print_modulation),
                 }

    wifi = Wireless(ifname)
    for command in iwcommands.keys():
        if option.startswith(command):
            if iwcommands[command][0].startswith(option):
                iwcommands[command][1](wifi)
                sys.exit(0)

    print "pyiwlist.py: unknown command '%s' (check 'pyiwlist.py --help')." % (option, )


if __name__ == "__main__":
    main()
