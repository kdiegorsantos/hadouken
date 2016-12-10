**[Technical overview](#technical-overview)** |
**[Prerequisites](#prerequisites)** |
**[Installation](#installation)** |
**[Running](#running)** |
**[Configuration](#configuration)** |
**[License](#license)**

# [hadouken](https://github.com/kdiegorsantos/hadouken)

This ansible role was builded to collect information about hardware and software from Linux servers and insert this informations on a sqlite3 database.

There is ansible tasks to.

- Distribute and execute hadouken.py
- Collect the json file that hadouken.py generates
- Execute db.py to load json info in the database

This application was made to run and collect information about.

- Red Hat Enterprise Linux
- EMC Storage
- Veritas InfoScale and Cluster Server
- Any virtual or physical hardware

----

## Prerequisites

On ansible server.

- ansible 1.4 or higher
- python 2.7
- sqlite3

```bash
yum install ansible sqlite3
```

On other servers.

- python 2.7
- dmidecode

```bash
yum install dmidecode
``` 

----

## Installation

Install using ansible-galaxy.

```bash
mkdir -p /etc/ansible/roles && cd /etc/ansible/roles && ansible-galaxy install kdiegorsantos.hadouken
```

----

## Configuration

Create a group in your hosts ansible file named hadouken and fill with desired hosts.
```bash
cat <EOF> /etc/ansible/hosts
[hadouken]
webserver
dbserver
EOF
```

After change the default domain variable on defaults/main.yml you can run this role using the ansible-playbook command.

```bash
ansible-playbook /etc/ansible/roles/hadouken/role.yml
```
----

## Running

- hadouken.py

Run hadouken.py manually on a host.

```bash
/usr/local/sbin/hadouken.py
server_name: snelnxa72 
server_release: Red Hat Enterprise Linux Server release 5.11 (Tikanga)
server_site: SNE
server_vendor:  HP
server_model:  ProLiant BL460c Gen8
server_serial: BRC2532JH4
server_cpu: Intel Xeon CPU E5-2650 2.00GHz / 2 Socket(s) / 32 CPU(s)/ 8 Core(s) per socket
server_memory: 32 GB 
server_ip: 10.168.81.77
server_cluster: idem_cluster 
server_clusternodes: snelnx187 snelnx189 snelnxa36 snelnxa68 snelnxa69 snelnxa70 snelnxa71 snelnxa72 snelnxa73
server_frame: 000290102907 000592600076 000595700007 000595700008 CKM00154803864
server_wwpn: 10006c3be5b076f1 10006c3be5b076f5 
server_db: None
```

Display the content from the json file generated by hadouken.py.

```bash
cat /var/tmp/snenix002.json | python -m json.tool
{
    "server_cluster": "",
    "server_clusternodes": "",
    "server_cpu": "2 Socket(s) Intel Xeon CPU E5540 @ 2.53GHz/ 16 CPU(s)/ 4 Core(s) per socket",
    "server_db": "",
    "server_frame": "",
    "server_ip": "10.168.90.103",
    "server_memory": "32 GB",
    "server_model": "ProLiant BL460c G6",
    "server_name": "snenix002",
    "server_release": "Red Hat Enterprise Linux Server release 6.8 (Santiago)",
    "server_serial": "BRC952N120",
    "server_site": "SNE",
    "server_vendor": "HP",
    "server_wwpn": ""
}
```

- db.sqlite

Run sql commands in a easy way using query-db.sh, just give an argument to begin the search.

```bash
/etc/ansible/roles/hadouken/files/bin/query-db.sh BRC50966F0
          server_id = 946
        server_name = rjolnxc15
     server_release = Red Hat Enterprise Linux Server release 6.5 (Santiago)
        server_site = RJO
      server_vendor = HP
       server_model = ProLiant DL580 Gen8
      server_serial = BRC50966F0
         server_cpu = 4 Socket(s) Intel Xeon CPU E7-4890 v2 @ 2.80GHz/ 120 CPU(s)/ 15 Core(s) per socket
      server_memory = 1292 GB
          server_ip = 10.168.34.150
     server_cluster = 
server_clusternodes = 
       server_frame = 000595700042
        server_wwpn = 5001438028cfc61c 5001438028cfc61e 5001438028cccf94 5001438028cccf96
          server_db = 
       server_owner = 
        server_rack = 
     server_console = 
        last_update = 2016-09-23
```

- sql commands using cli

Run sql commands using sqlite3.

```bash
sqlite3 -header -column /etc/ansible/roles/files/db/db.sqlite "select * from info where server_name = 'snelnxa72'"
server_id   server_name  server_release                                          server_site  server_vendor  server_model        server_serial  server_cpu                                                                   server_memory  server_ip      server_cluster  server_clusternodes  server_frame  server_wwpn  server_db   server_owner  server_rack  server_console  last_update
----------  -----------  ------------------------------------------------------  -----------  -------------  ------------------  -------------  ---------------------------------------------------------------------------  -------------  -------------  --------------  -------------------  ------------  -----------  ----------  ------------  -----------  --------------  -----------
1           snenix002    Red Hat Enterprise Linux Server release 6.8 (Santiago)  SNE          HP             ProLiant BL460c G6  BRC952N120     2 Socket(s) Intel Xeon CPU E5540 @ 2.53GHz/ 16 CPU(s)/ 4 Core(s) per socket  32 GB          10.168.90.103                                                                                                                         2016-09-23 
----

## License

This project is licensed under the MIT license. See included LICENSE.md.

Author Information

-------

- Diego R. Santos
- [github.com](https://github.com/kdiegorsantos)

