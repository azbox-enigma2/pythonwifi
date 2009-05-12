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
    print "%s     %02d channels in total; available frequencies :" % \
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
    print "%s     %02d available bit-rates :" % (wifi.ifname, num_bitrates)
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

    print wifi.ifname,
    print "   ",
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
    iwcommands = { "scanning"     : print_scanning_results,
                   "channel"      : print_channels,
                   "frequency"    : print_channels,
                   "bitrate"      : print_bitrates,
                   "rate"         : print_bitrates,
                   "encryption"   : print_encryption,
                   "keys"         : print_encryption,
                   #"power"        : print_power,
                   #"txpower"      : print_power,
                   #"retry"        : print_retry,
                   #"ap"           : print_aps,
                   #"accesspoints" : print_aps,
                 }

    wifi = Wireless(ifname)
    for command in iwcommands.keys():
        if command.startswith(option):
            iwcommands[command](wifi)
            sys.exit(0)

    print "pyiwlist.py: unknown command '%s' (check 'pyiwlist.py --help')." % (command, )


if __name__ == "__main__":
    main()
