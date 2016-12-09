CREATE TABLE info (
    server_id           INTEGER    PRIMARY KEY
                                   UNIQUE
                                   NOT NULL,
    server_name         TEXT (256) UNIQUE,
    server_release      TEXT (256) NOT NULL,
    server_site         TEXT (256) NOT NULL,
    server_vendor       TEXT (256) NOT NULL,
    server_model        TEXT (256) NOT NULL,
    server_serial       TEXT (256) NOT NULL,
    server_cpu          TEXT (256) NOT NULL,
    server_memory       TEXT (256) NOT NULL,
    server_ip           TEXT (256) NOT NULL,
    server_cluster      TEXT (256),
    server_clusternodes TEXT (256),
    server_frame        TEXT (256),
    server_wwpn         TEXT (256),
    server_db           TEXT (256),
    server_owner        TEXT (256),
    server_rack         TEXT (256),
    server_console      TEXT (256),
    last_update         TIME       NOT NULL
                                   DEFAULT (date('now') )
);
