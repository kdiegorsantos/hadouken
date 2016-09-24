#!/usr/bin/python

'''
Collect information about RHEL 5/6 and 7, it was tested with python2.x.
'''

import subprocess
import platform

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


    # in my case the first 3 letters of the server name indicates the site location.
    def get_site():
        x = platform.node()
        return x.replace(my_domain, '').upper()[:3]


    # get operation system release.
    def get_release():
        proc = subprocess.Popen(
            ["/usr/bin/lsb_release -d 2>/dev/null | awk -F':' '{{print $2}}'"], stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get the hardware serial number.
    def get_hw_serialnumber():
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-serial-number 2>/dev/null | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get hardware vendor.
    def get_hw_vendor():
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-manufacturer 2>/dev/null | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get hardware model.
    def get_hw_model():
        proc = subprocess.Popen(
            ["/usr/sbin/dmidecode -s system-product-name 2>/dev/null | egrep -v '^#'"], stdout=subprocess.PIPE,
            shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get scsi target wwpn.
    def get_fc_wwpn():
        proc = subprocess.Popen(
            ["cat /sys/class/fc_host/host*/port_name 2>/dev/null| xargs"], stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return str(x).strip().replace('0x', '')


    # get ipv4 address.
    def get_ipaddr():
        proc = subprocess.Popen(
            ["/sbin/ip addr show|egrep inet|awk '{{print $2}}'|awk -F'/' '{{print $1}}'|egrep -v '^127|::'|xargs"],
            stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get EMC storage storage id.
    def get_frame():
        proc = subprocess.Popen(
            ["[ -x /sbin/powermt ] && /sbin/powermt display ports|"
             "awk '{{print $1}}' | egrep '^[A-Z]+{2}[0-9]|[0-9]' | sort -u | xargs"], stdout=subprocess.PIPE,
            shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get total memory in GB.
    def get_memory():
        proc = subprocess.Popen(
            ["egrep MemTotal /proc/meminfo | awk -F':' '{{print $2}}'"], stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        y = str(x).strip().replace('kB', '')
        z = (int(y) / int(1024000))
        return "%s GB" % z


    # get cpu info, physical and cores.
    def get_cpu():
        proc = subprocess.Popen(
            ["cpuinfo=/proc/cpuinfo \n"
             "model_cpu=$(gawk -F: '/^model name/{{print $2; exit}}' <$cpuinfo) \n"
             "model_cpu=$(sed -e 's/(R)//g ; s/(TM)//g ; s/  */ /g ; s/^ // ; s/ 0 @//g' <<<$model_cpu) \n"
             "num_cpu=$(gawk '/^processor/{{n++}} END{{print n}}' <$cpuinfo) \n"
             "num_cores_per_cpu=$(gawk '/^cpu cores/{{print $4; exit}}' <$cpuinfo) \n"
             "echo -e \"${num_cpu} CPU(s) ${model_cpu} / ${num_cores_per_cpu} Core(s) per socket\""
             ""], stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get information about Veritas Cluster.
    def get_cluster():
        proc = subprocess.Popen(["[ -x /opt/VRTSvcs/bin/haclus ] && /opt/VRTSvcs/bin/haclus -state|"
                                 "awk '{{print $1}}' | tail -n1"], stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get the list of Veritas Cluster nodes.
    def get_clusternodes():
        proc = subprocess.Popen(
            ["[ -x /opt/VRTSvcs/bin/hasys ] && /opt/VRTSvcs/bin/hasys -list | xargs"],
            stdout=subprocess.PIPE, shell=True)
        x = proc.communicate()[0]
        return x.strip()


    # get the name of Oracle instances.
    def get_db():
        proc = subprocess.Popen(
            ["ps -ef | grep pmon | awk -F\_ '{{print $3}}' | egrep -v '^$|\+ASM' | xargs"],
            stdout=subprocess.PIPE, shell=True)
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
                                  get_cpu(), get_memory(), get_ipaddr(), get_cluster(), get_clusternodes(), get_frame(),
                                  get_fc_wwpn(), get_db()))

    # create a dict to export info to sqlite db.
    hadouken = {'server_name': get_hostname(), 'server_release': get_release(), 'server_site': get_site(),
                'server_vendor': get_hw_vendor(), 'server_model': get_hw_model(),
                'server_serial': get_hw_serialnumber(), 'server_cpu': get_cpu(), 'server_memory': get_memory(),
                'server_ip': get_ipaddr(), 'server_cluster': get_cluster(), 'server_clusternodes': get_clusternodes(),
                'server_frame': get_frame(), 'server_wwpn': get_fc_wwpn(), 'server_db': get_db()}

    # export hadouken info to be loaded into sqlite3.
    hadouken_file = '/var/tmp/%s.json' % get_hostname()
    fp = open(hadouken_file, 'w')
    json.dump(hadouken, fp)

else:
    print("OS not supported.")
