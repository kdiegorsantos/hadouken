#!/bin/bash

regex=$(echo -e "'%${1}%'")

sqlite3 -header -line  /etc/ansible/roles/kdiegorsantos.hadouken/files/db/db.sqlite "SELECT * from info where server_id LIKE $regex or server_name LIKE $regex or server_release LIKE $regex or server_site LIKE $regex or server_vendor LIKE $regex or server_model LIKE $regex or server_serial LIKE $regex or server_cpu LIKE $regex or server_memory LIKE $regex or server_ip LIKE $regex or server_cluster LIKE $regex or server_clusternodes LIKE $regex or server_frame LIKE $regex or server_wwpn LIKE $regex or server_db LIKE $regex or server_owner LIKE $regex or server_rack LIKE $regex or server_console LIKE $regex or last_update  LIKE $regex"
