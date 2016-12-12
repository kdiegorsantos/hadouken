#!/usr/bin/python2

import os
import platform
import subprocess

# try to import json module, if got an error use simplejson instead of json.
try:
    import json
except ImportError:
    import simplejson as json

# if your server uses fqdn, you can suppress the domain, just change the bellow variable to your domain.
my_domain = ''

# checks if operating system is Linux.
if platform.system() == 'Linux':
    # subprocess funciton, pass an argument as k variable to it.
    def SubprocessPopen(k):
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen([k], stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # display hostname
    def display_hostname():
        x = platform.node()
        return x.replace(my_domain, '').lower()

    # in my case the first 3 letters of the hostname indicates the site location, change if you want.
    def display_site():
        sites = ('SNE', 'RJO', 'BFC')
        x = platform.node()
        site = x.replace(my_domain, '').upper()[:3]
        if site in sites:
            return site

    # display operation system release.
    def display_release():
        k = "lsb_release -d | awk -F':' '{{print $2}}'"
        return (SubprocessPopen(k.strip()))

    # display the hardware serial number.
    def display_hw_serialnumber():
        k = "dmidecode -s system-serial-number | egrep -v '^#'"
        return (SubprocessPopen(k.strip()))

    # display hardware vendor.
    def display_hw_vendor():
        k = "dmidecode -s system-manufacturer | egrep -v '^#'"
        return (SubprocessPopen(k.strip()))

    # display hardware model.
    def display_hw_model():
        k = "dmidecode -s system-product-name | egrep -v '^#'"
        return SubprocessPopen(k.strip())

    # display fibre channel id wwpn.
    def display_fc_wwpn():
        k = "cat /sys/class/fc_host/host*/port_name"
        return SubprocessPopen(k.strip().replace('0x', ''))

    # display ipv4 address.
    def display_ipaddr():
        k = "ip addr show | egrep inet | awk '{{print $2}}' | awk -F'/' '{{print $1}}' | egrep -v '^127|::'"
        return SubprocessPopen(k.strip())

    # display EMC storage id.
    def display_frame():
        k = "powermt display ports | awk '{{print $1}}' | egrep '^[A-Z]+{2}[0-9]|[0-9]' | sort -u"
        return SubprocessPopen(k.strip())

    # display total memory in MB.
    def display_memory():
        k = "egrep MemTotal /proc/meminfo | awk -F':' '{{print $2}}' | awk '{{print int($1/1024)}}'"
        return SubprocessPopen(k) + " MB"

    # display cpu info, physical and cores.
    def display_cpu():
        k = "model=$(lscpu | egrep ^'Model name' | awk -F\: '{{print$2}}')\n" \
            "socket=$(lscpu | egrep ^'Socket' | awk -F\: '{{print$2}}')\n" \
            "cpu=$(lscpu | egrep ^'CPU\(' | awk -F\: '{{print$2}}')\n" \
            "core=$(lscpu | egrep ^'Core' | awk -F\: '{{print$2}}')\n" \
            "echo -e ""$model / $socket Socket\\(s\\) / $cpu CPU\\(s\\) / $core Core\\(s\\) per Socket"""
        return SubprocessPopen(k)

    # display information about Veritas InforScale and Cluster Server.
    def display_cluster():
        k = "/opt/VRTSvcs/bin/haclus -state | awk '{{print $1}}' | tail -n1"
        return SubprocessPopen(k)

    # display the list of cluster nodes.
    def display_clusternodes():
        k = "/opt/VRTSvcs/bin/hasys -list"
        return SubprocessPopen(k)

    # display the name of Oracle instances.
    def display_db():
        k = "ps -ef | grep pmon | awk -F\_ '{{print $3}}' | egrep -v '^$|\+ASM'"
        return SubprocessPopen(k)

    # print all information on the screen.
    print(
        "server_name: {0:s} \n"
        "server_release: {1:s} \n"
        "server_site: {2:s} \n"
        "server_vendor: {3:s} \n"
        "server_model: {4:s} \n"
        "server_serial: {5:s} \n"
        "server_cpu: {6:s} \n"
        "server_memory: {7:s} \n"
        "server_ip: {8:s} \n"
        "server_cluster: {9:s} \n"
        "server_clusternodes: {10:s} \n"
        "server_frame: {11:s} \n"
        "server_wwpn: {12:s} \n"
        "server_db: {13:s}".format(display_hostname(), display_release(), display_site(), display_hw_vendor(), display_hw_model(),
                                   display_hw_serialnumber(),
                                   display_cpu(), display_memory(), display_ipaddr(), display_cluster(), display_clusternodes(),
                                   display_frame(),
                                   display_fc_wwpn(), display_db()))

    # create a dict to export info to sqlite db.
    hadouken = {'server_name': display_hostname(), 'server_release': display_release(), 'server_site': display_site(),
                'server_vendor': display_hw_vendor(), 'server_model': display_hw_model(),
                'server_serial': display_hw_serialnumber(), 'server_cpu': display_cpu(), 'server_memory': display_memory(),
                'server_ip': display_ipaddr(), 'server_cluster': display_cluster(), 'server_clusternodes': display_clusternodes(),
                'server_frame': display_frame(), 'server_wwpn': display_fc_wwpn(), 'server_db': display_db()}

    # export hadouken info to be loaded into sqlite3 using db.py..
    hadouken_file = '/var/tmp/%s.json' % display_hostname()
    fp = open(hadouken_file, 'w')
    json.dump(hadouken, fp)

else:
    # if the operation system is not Linux, sorry.
    print("OS not supported.")
