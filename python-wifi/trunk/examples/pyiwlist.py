#!/usr/bin/env python
# Copyright 2004, 2005 Roman Joost <roman@bromeco.de> - Rotterdam, Netherlands
# this file is part of the pywifi package - a python wifi library
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
from pythonwifi.iwlibs import Wireless, getNICnames

def print_scanning_results(wifi):
    for results in wifi.scan():
        results.display()
    sys.exit(0)

def print_bitrate_information(wifi):
    num_bitrates, bitrates = wifi.getBitrates()
    if num_bitrates == 0:
        print "\t 0 Bit Rates found."
        sys.exit(0)

    bitrate_type =  type(bitrates[-1]) is types.StringType
    print "\t%s available bit-rates:" % num_bitrates
    for rate in bitrates:
        # rate is Iwfreq
        # XXX - there are to much bitrates?
        if bitrate_type:
            print "\t%s" % rate
        elif rate.getBitrate() is not None:
            print "\t%s" % rate.getBitrate()
    print "\tCurrent Bit Rate: %s" %wifi.getBitrate()

def print_channel_information(wifi):
    # XXX The channel information is bogus here, because it just
    # numerates how many channels the card provides, but doesn't give
    # any information about *which* channel *which* frequencies has
    num_frequencies, channels = wifi.getChannelInfo()
    current_freq = wifi.getFrequency()
    print "%s channels in total; available frequencies: \n"\
        %num_frequencies
    for channel in channels:
        print "\tChannel %.2d: %s" %(channels.index(channel)+1, 
                                     channel)
    print "\tCurrent Frequency:%s (Channel %s)" %(current_freq,
                                                  sys.exit(1))

def main():
    if len(sys.argv) < 1:
        usage()
        sys.exit(1)
    
    try:
        ifname, option = sys.argv[1:]
    except ValueError:
        usage()
        sys.exit(2)
   
    ifnames = getNICnames()
    if ifnames == []:
        print "No wireless devices present or incompatible OS."
        sys.exit(0)
    # find out if the user passed a valid device
    try:
        ifnames.index(ifname)
    except ValueError:
        print "You passed an invalid interface name."
        sys.exit(0)
        
    wifi = Wireless(ifname)
    if option in ('channel', 'frequency'):
        print_channel_information(wifi)
    elif option == 'bitrates':
        print_bitrate_information(wifi)
    elif option == 'scanning':
        print_scanning_results(wifi)
    else:
        print "\nSorry, this is an invalid option you passed!\n"
        usage()

def usage():
    print """iwlist.py - Copyright 2004-2005 Roman Joost
Get more detailed wireless information from a wireless interface

usage:
    pyiwlist IFNAME scanning
    pyiwlist IFNAME bitrates 
    pyiwlist IFNAME channel 
    pyiwlist IFNAME frequency"""

if __name__ == "__main__":
    main()
