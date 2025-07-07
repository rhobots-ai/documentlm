#!/bin/bash

terminate_connections() {
  psql -U postgres -c "
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '$1'
    AND pid <> pg_backend_pid();"
}

terminate_connections "core"
psql -U postgres -c "DROP DATABASE IF EXISTS core;"
psql -U postgres -c "CREATE DATABASE core;"

terminate_connections "auth"
psql -U postgres -c "DROP DATABASE IF EXISTS auth;"
psql -U postgres -c "CREATE DATABASE auth;"