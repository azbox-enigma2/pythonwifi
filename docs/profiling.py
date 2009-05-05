import profile
from wirelessconfig import WirelessConfig 

def main():
    wc = WirelessConfig()
    profile.run('wc.get_nic()')
#    profile.run(wc.get_nic_from_file())

if __name__ == '__main__':
    main()
