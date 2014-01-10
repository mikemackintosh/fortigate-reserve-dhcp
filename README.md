fortigate-reserve-dhcp
======================

Python Script to help with the correlation of reserved DHCP and Policy Object

## Usage

Pass the following arguments to the command

  - Device Name
  - IP Address
  - MAC Address

    ./fortigate_reserved_dhcp.py iPod 10.1.1.80 b8:c7:gg:3f:gh:ij

## Example

    👻 chronosec: ~/Desktop% ./fortigate_reserved_dhcp.py Michaels-iPod 10.1.4.80 b8:c7:5d:3d:fe:6a
    Initiating Fortinet Reserved DHCP Address
    
    Connecting to Device: 10.1.4.99
    We found 1 entries
    Our next entry will be: 2
    Loading template
    
    Pushing Config:
    config system dhcp server
        edit 1
            config reserved-address
                edit 2
                    set description "Michaels-iPod"
                    set ip 10.1.4.80
                    set mac b8:c7:5d:3d:fe:6a
                next
            end
        next
    end
    config firewall addres
        edit "Michaels-iPod"
            set associated-interface LAN
            set subnet 10.1.4.80 255.255.255.255
        next
    end
