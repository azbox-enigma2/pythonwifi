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
import errno
import sys
import types

import pythonwifi.flags
from pythonwifi.iwlibs import Wireless, Iwrange, getNICnames

def print_scanning_results(wifi, args=None):
    """ Print the access points detected nearby.

    """
    # "Check if the interface could support scanning"
    try:
        iwrange = Iwrange(wifi.ifname)
    except IOError, (error_number, error_string):
        print "%-8.16s  Interface doesn't support scanning.\n" % \
            (wifi.ifname)
    # "Check for Active Scan (scan with specific essid)"
    # "Check for last scan result (do not trigger scan)"
    # "Initiate Scanning"
    try:
        results = wifi.scan()
    except IOError, (error_number, error_string):
        if error_number != errno.EPERM:
            print "%-8.16s  Interface doesn't support scanning : %s\n" % \
                (wifi.ifname, error_string)
    else:
        (num_channels, frequencies) = wifi.getChannelInfo()
        index = 1
        for ap in results:
            print "\t  Cell %02d - Address: %s" % (index, ap.bssid)
            print "\t\t    ESSID:\"%s\"" % (ap.essid, )
            print "\t\t    Mode:%s" % (ap.mode, )
            print "\t\t    Frequency:%s (Channel: %d)" % \
                                (wifi._formatFrequency(ap.frequency.getFrequency()),
                                 frequencies.index(wifi._formatFrequency(ap.frequency.getFrequency())) + 1)
            print "\t\t    Quality=%s/%s  Signal level=%s/%s  Noise level=%s/%s" % \
                                (ap.quality.quality,
                                wifi.getQualityMax().quality,
                                ap.quality.getSignallevel(),
                                "100",
                                ap.quality.getNoiselevel(),
                                "100")
            #print "\t\t    Encryption key:%s" % (ap.encode, )
            if len(ap.rate) > 0:
                print "\t\t    Bit Rates:",
                rate_lines = len(ap.rate) / 5
                rate_remainder = len(ap.rate) % 5
                line = 0
                while line < rate_lines:
                    print "%s; %s; %s; %s; %s" % \
                        tuple(wifi._formatBitrate(x) for x in ap.rate[line * 5:(line * 5) + 5])
                    print "\t\t              ",
                    line = line + 1
                print "%s; "*(rate_remainder - 1) % \
                    tuple(wifi._formatBitrate(x) for x in ap.rate[line * 5:line * 5 + rate_remainder - 1]),
                sys.stdout.write(wifi._formatBitrate(ap.rate[line * 5 + rate_remainder - 1]))
                print
            index = index + 1

def print_channels(wifi, args=None):
    """ Print all frequencies/channels available on the card.

    """
    try:
        (num_frequencies, channels) = wifi.getChannelInfo()
        current_freq = wifi.getFrequency()
    except IOError, (error_number, error_string):
        # Channel/frequency info not available
        if (error_number == errno.EOPNOTSUPP) or \
           (error_number == errno.EINVAL) or \
           (error_number == errno.ENODEV):
            print "%-8.16s  no frequency information.\n" % (wifi.ifname, )
        else:
            report_error("channel", wifi.ifname, error_number, error_string)
    else:
        # Channel/frequency info available
        print "%-8.16s  %02d channels in total; available frequencies :" % \
                    (wifi.ifname, num_frequencies)
        for channel in channels:
            print "\t  Channel %02d : %s" % \
                    (channels.index(channel)+1, channel)
        # Do some low-level comparisons on frequency info
        iwfreq = wifi.wireless_info.getFrequency()
        # XXX - this is not the same flags value as iwlist.c
        if iwfreq.flags & pythonwifi.flags.IW_FREQ_FIXED:
            fixed = "="
        else:
            fixed = ":"
        if iwfreq.getFrequency() < pythonwifi.iwlibs.KILO:
            return_type = "Channel"
        else:
            return_type = "Frequency"
        # Output current channel/frequency
        current_freq = wifi.getFrequency()
        print "\t  Current %s%c%s (Channel %d)\n" % \
                    (return_type, fixed, current_freq, channels.index(current_freq) + 1 )

def print_bitrates(wifi, args=None):
    """ Print all bitrates available on the card.

    """
    try:
        num_bitrates, bitrates = wifi.getBitrates()
    except IOError, (error_number, error_string):
        if (error_number == errno.EOPNOTSUPP) or (error_number == errno.EINVAL):
            # not a wireless device
            print "%-8.16s  no bit-rate information." % (wifi.ifname, )
        else:
            report_error("bit rate", wifi.ifname, error_number, error_string)
    else:
        if (num_bitrates > 0) and \
           (num_bitrates <= pythonwifi.flags.IW_MAX_BITRATES):
            # wireless device with bit rate info, so list 'em
            print "%-8.16s  %02d available bit-rates :" % \
                    (wifi.ifname, num_bitrates)
            for rate in bitrates:
                print "\t  %s" % rate
        else:
            # wireless device, but no bit rate info available
            print "%-8.16s  unknown bit-rate information." % (wifi.ifname, )
    # current bit rate
    try:
        bitrate = wifi.wireless_info.getBitrate()
    except IOError, (error_number, error_string):
        # no bit rate info is okay, error was given above
        pass
    else:
        if bitrate.fixed:
            fixed = "="
        else:
            fixed = ":"
        print "\t  Current Bit Rate%c%s" % (fixed, wifi.getBitrate())
    # broadcast bit rate
    # XXX add broadcast bit rate
    print

def print_encryption(wifi, args=None):
    """ Print encryption keys on the card.

    """
    keys = wifi.getKeys()
    range_info = Iwrange(wifi.ifname)

    for index in range(range_info.num_encoding_sizes - 1):
        key_sizes = repr(range_info.encoding_size[index] * 8) + ", "
    key_sizes = key_sizes + \
                repr(range_info.encoding_size[range_info.num_encoding_sizes - 1] * 8) + \
                "bits"
    print "%-8.16s  %d key sizes : %s" % \
            (wifi.ifname, range_info.num_encoding_sizes, key_sizes)
    print "\t  %d keys available :" % (len(keys), )
    for key in keys:
        print "\t\t[%d]: %s" % (key[0], key[1])
    print "\t  Current Transmit Key: [%s]" % \
            (wifi.wireless_info.getKey().flags & pythonwifi.flags.IW_ENCODE_INDEX, )
    if wifi.wireless_info.getKey().flags & pythonwifi.flags.IW_ENCODE_RESTRICTED:
        print "\t  Security mode:restricted"
    if wifi.wireless_info.getKey().flags & pythonwifi.flags.IW_ENCODE_OPEN:
        print "\t  Security mode:open"
    print "\n"

def format_pm_value(value, args=None):
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

def print_power(wifi, args=None):
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
    if (power_saving[0] & pythonwifi.flags.IW_POWER_SAVING):
        if (power_saving[0] & pythonwifi.flags.IW_POWER_MIN):
            print "Auto  saving  ; ",
        else:
            print "Fixed saving  ; ",
        print "min period:%s\n\t\t\t  " % \
                (format_pm_value(power_saving[1]), ),
        print "max period:%s\n\t " % (format_pm_value(power_saving[2]), ),
    if power_params.disabled:
        print "Current mode:off"
    else:
        if (power_params.flags & pythonwifi.flags.IW_POWER_MODE == \
                    pythonwifi.flags.IW_POWER_UNICAST_R):
            print "Current mode:Unicast only received"
        elif (power_params.flags & pythonwifi.flags.IW_POWER_MODE == \
                    pythonwifi.flags.IW_POWER_MULTICAST_R):
            print "Current mode:Multicast only received"
        elif (power_params.flags & pythonwifi.flags.IW_POWER_MODE == \
                    pythonwifi.flags.IW_POWER_ALL_R):
            print "Current mode:All packets received"
        elif (power_params.flags & pythonwifi.flags.IW_POWER_MODE == \
                    pythonwifi.flags.IW_POWER_FORCE_S):
            print "Current mode:Force sending"
        elif (power_params.flags & pythonwifi.flags.IW_POWER_MODE == \
                    pythonwifi.flags.IW_POWER_REPEATER):
            print "Current mode:Repeat multicasts"
    print

def print_retry(wifi, args=None):
    pass

def print_aps(wifi, args=None):
    pass

def report_error(function, interface, error_number, error_string):
    """ Print error to user. """
    print """Uncaught error condition.  Please report this to the \
developers' mailing list (informaion available at \
http://lists.berlios.de/mailman/listinfo/pythonwifi-dev).  While attempting to \
print %s informaion for %s, the error "%d - %s" occurred.""" % \
(function, interface, error_number, error_string)

def usage():
    print """\
Usage: iwlist.py [interface] scanning [essid NNN] [last]
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
                 [interface] peers"""

def get_matching_command(option):
    """ Return a function for the command.

        'option' -- string -- command to match

        Return None if no match found.

    """
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
                   "re"  : ("retry", print_retry),
                   "ap"  : ("ap", print_aps),
                   "ac"  : ("accesspoints", print_aps),
                   "pe"  : ("peers", print_aps),
                   #"ev" : ("event", print_event),
                   #"au" : ("auth", print_auth),
                   #"w"  : ("wpakeys", print_wpa),
                   #"g"  : ("genie", print_genie),
                   #"m"  : ("modulation", print_modulation),
                 }

    function = None
    for command in iwcommands.keys():
        if option.startswith(command):
            if iwcommands[command][0].startswith(option):
                function = iwcommands[command][1]
    return function

def main():
    # if only program name is given, print usage info
    if len(sys.argv) == 1:
        usage()

    # if program name and one argument are given
    if len(sys.argv) == 2:
        option = sys.argv[1]
        # look for matching command
        list_command = get_matching_command(option)
        # if the one argument is a command
        if list_command is not None:
            for ifname in getNICnames():
                wifi = Wireless(ifname)
                list_command(wifi)
        else:
            print "iwlist.py: unknown command `%s' " \
                  "(check 'iwlist.py --help')." % (option, )

    # if program name and more than one argument are given
    if len(sys.argv) > 2:
        # Get the interface and command from command line
        ifname, option = sys.argv[1:]
        # look for matching command
        list_command = get_matching_command(option)
        # if the second argument is a command
        if list_command is not None:
            wifi = Wireless(ifname)
            list_command(wifi, sys.argv[3:])
        else:
            print "iwlist.py: unknown command `%s' " \
                   "(check 'iwlist.py --help')." % (option, )


if __name__ == "__main__":
    main()

