#!/usr/bin/env python
import sys, os, re
import paramiko

# Update your Fortigate IP Address Here
gateway_ip = "10.x.x.x" 

# Forwards compatablity?
netmask = "255.255.255.255"

""" Get log from server """
def connect_to_server(server="localhost",username="",password="",command=""):
    ssh = paramiko.SSHClient()
    ssh.connect(server, username=username, password=password)

    return ssh.exec_command(command)


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
        
    for key in agent_keys:
        print('Trying ssh-agent key {}'.format(hexlify(key.get_fingerprint()))),
        try:
            transport.auth_publickey(username, key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')


def group_by_section( content, match ):
    buffer = []
    for line in content:
        line = line.strip()
        line = line.replace("--More-- \r         \r            ", "")
        if line.startswith("config") or line == "end":
            if buffer: yield buffer
            buffer = [ line ]
        else:
            buffer.append( line )
    yield buffer

def get_config_value( config, find):
    for line in config:
        line = line.strip()
        line = line.replace("--More-- \r         \r            ", "")
        if line.startswith( find ):
            found = line.replace( find, "")
            return found.split(" ")

""" <Main> Init """
if __name__ == "__main__":
    
    devicename = sys.argv[1]
    ipaddress = sys.argv[2]
    macaddress = sys.argv[3]

    """ !! Print Message """
    print "Initiating Fortinet Reserved DHCP Address\n"

    """ SSH Connect To Device """
    print "Connecting to Device: %s" % gateway_ip

    """  """
    ssh_host = gateway_ip
    ssh_port = 22
    ssh_user = "admin"
    ssh_password = "password" # // We use SSH key instead
    ssh_auth_type = "key"
    ssh_key_file = "PathToKeyFile/id_rsa" # "~/.ssh/id_rsa"

    # Create SSH Object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if ssh_auth_type == 'key':
        #key = paramiko.RSAKey.from_private_key_file(ssh_key_file, ssh_password)
        ssh.connect(ssh_host, username=ssh_user, key_filename=ssh_key_file)
    else:
        ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
        # print "Failed to connect with SSH key, Password access not enabled";
        # exit()

    # Get STDOUT/IN/ERR from SSH
    stdin, stdout, stderr = ssh.exec_command('show system dhcp server')
    fortigate_config = stdout.readlines()    

    # Create int holders
    last_entry = 0;
    entry_count = 0;

    # Loop through the retrieved data
    for sections in group_by_section(fortigate_config, 'reserved-address'):
        if(sections[0] == "config reserved-address"):
            for config in sections:
                config = config.lstrip()
                if config.startswith("edit"):
                    entry = config.split(" ")[1]
                    last_entry = int(entry)
                    entry_count = entry_count+1
    
    interface = get_config_value(fortigate_config, "set interface")[1].replace('"', "")
    
    # Allocate Next Entry
    next_entry = last_entry+1

    print "We found %d entries" % entry_count
    print "Our next entry will be: %d" % next_entry

    print "Loading template"
    template = open("dhcp_template.erb", "r").read()
    
    result = template.format(ID=next_entry,DEVICENAME=devicename,IPADDRESS=ipaddress,NETMASK=netmask,MACADDRESS=macaddress,INTERFACE=interface)

    print "Pushing Config:"
    print result

    stdin, stdout, stderr = ssh.exec_command( result )
    response = stdout.readlines()    
    print "\nFinished!" 

    ssh.close()
    exit()



