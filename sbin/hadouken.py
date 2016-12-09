#!/usr/bin/python2

# Collect information about RHEL 5 or higher and Ubuntu 12.04 or higer, it was tested with python2.7.

import os
import platform
import subprocess

# try to import json module, if got an error use simplejson instead of json.
try:
    import json
except ImportError:
    import simplejson as json

# if your server uses fqdn, you can suppress the domain, just change the bellow variable to your domain.
my_domain = ".internal.timbrasil.com.br"

# checks if operating system is Linux.
if platform.system() == 'Linux':
    # get the server name
    def get_hostname():
        x = platform.node()
        return x.replace(my_domain, '').lower()

    # in my case the first 3 letters of the server name indicates the site location, change if you want.
    def get_site():
        sites = ('SNE', 'RJO', 'BFC')
        x = platform.node()
        site = x.replace(my_domain, '').upper()[:3]
        if site in sites:
            return site

    # get operation system release.
    def get_release():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["/usr/bin/lsb_release -d | gawk -F':' '{{print $2}}'"], stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get the hardware serial number.
    def get_hw_serialnumber():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-serial-number | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get hardware vendor.
    def get_hw_vendor():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-manufacturer | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get hardware model.
    def get_hw_model():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-product-name | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get fibre channel id wwpn.
    def get_fc_wwpn():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["cat /sys/class/fc_host/host*/port_name | xargs"], stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return str(x).strip().replace('0x', '')

    # get ipv4 address.
    def get_ipaddr():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["/sbin/ip addr show|egrep inet|awk '{{print $2}}'|awk -F'/' '{{print $1}}'|egrep -v '^127|::'|xargs"],
            stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get EMC storage id.
    def get_frame():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["[ -x /sbin/powermt ] && /sbin/powermt display ports|"
             "gawk '{{print $1}}' | egrep '^[A-Z]+{2}[0-9]|[0-9]' | sort -u | xargs"], stdout=subprocess.PIPE,
            shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get total memory in GB.
    def get_memory():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["egrep MemTotal /proc/meminfo | gawk -F':' '{{print $2}}'"], stdout=subprocess.PIPE, shell=True,
            stderr=devnull)
        x = proc.communicate()[0]
        y = str(x).strip().replace('kB', '')
        z = (int(y) / int(1024000))
        return "%s GB" % z

    # get cpu info, physical and cores.
    def get_cpu():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["model=$(lscpu | egrep ^'Model name' | gawk -F\: '{{print$2}}' | xargs) \n"
             "socket=$(lscpu | egrep ^'Socket' | gawk -F\: '{{print$2}}' | xargs \n"
             "cpu=$(lscpu | egrep ^'CPU\(' | gawk -F\: '{{print$2}}' | xargs) \n"
             "core=$(lscpu | egrep ^'Core' | gawk -F\: '{{print$2}}' | xargs) \n"
             "echo -e ""$model / $socket Socket(s) / $cpu CPU(s) / $core Core(s) per Socket"""],
            stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get information about Veritas Cluster.
    def get_cluster():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(["[ -x /opt/VRTSvcs/bin/haclus ] && /opt/VRTSvcs/bin/haclus -state|"
                                 "awk '{{print $1}}' | tail -n1"], stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get the list of Veritas Cluster nodes.
    def get_clusternodes():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["[ -x /opt/VRTSvcs/bin/hasys ] && /opt/VRTSvcs/bin/hasys -list | xargs"],
            stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

    # get the name of Oracle instances.
    def get_db():
        devnull = open(os.devnull, 'w')
        proc = subprocess.Popen(
            ["ps -ef | grep pmon | gawk -F\_ '{{print $3}}' | egrep -v '^$|\+ASM' | xargs"],
            stdout=subprocess.PIPE, shell=True, stderr=devnull)
        x = proc.communicate()[0]
        return x.strip()

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
        "server_db: {13:s}".format(get_hostname(), get_release(), get_site(), get_hw_vendor(), get_hw_model(),
                                   get_hw_serialnumber(),
                                   get_cpu(), get_memory(), get_ipaddr(), get_cluster(), get_clusternodes(),
                                   get_frame(),
                                   get_fc_wwpn(), get_db()))

    # create a dict to export info to sqlite db.
    hadouken = {'server_name': get_hostname(), 'server_release': get_release(), 'server_site': get_site(),
                'server_vendor': get_hw_vendor(), 'server_model': get_hw_model(),
                'server_serial': get_hw_serialnumber(), 'server_cpu': get_cpu(), 'server_memory': get_memory(),
                'server_ip': get_ipaddr(), 'server_cluster': get_cluster(), 'server_clusternodes': get_clusternodes(),
                'server_frame': get_frame(), 'server_wwpn': get_fc_wwpn(), 'server_db': get_db()}

    # export hadouken info to be loaded into sqlite3 using db.py..
    hadouken_file = '/var/tmp/%s.json' % get_hostname()
    fp = open(hadouken_file, 'w')
    json.dump(hadouken, fp)

else:
    # if the operation system is not Linux, sorry.
    print("OS not supported.")
