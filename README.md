Fortigate Reserved DHCP Manager
======================

This script allows you to easily manage reserved DHCP as well as correlating firewall address objects. This simplified the policy workflow for static devices tied to users.

***NOTE***: There is no input validation or error checking applied yet. Will come shortly.

## Usage

The following details are needed:

  - Device Name
  - IP Address
  - MAC Address

Then pass them to the script like so:

    ./fortigate_reserved_dhcp.py iPod 10.1.1.80 b8:c7:gg:3f:gh:ij

## Example

    👻 chronosec: ~/Desktop% ./fortigate_reserved_dhcp.py iPod 10.1.1.80 b8:c7:gg:3f:gh:ij
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
                    set description "iPod"
                    set ip 10.1.1.80
                    set mac  b8:c7:gg:3f:gh:ij
                next
            end
        next
    end
    config firewall addres
        edit "iPod"
            set associated-interface LAN
            set subnet 10.1.1.80 255.255.255.255
        next
    end
