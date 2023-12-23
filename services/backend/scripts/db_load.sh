#!/bin/bash

# Default values
host=""
port=""
name=""
user=""
password=""
file=""

# Parse command-line arguments
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -h|--host)
        host="$2"
        shift
        shift
        ;;
        -p|--port)
        port="$2"
        shift
        shift
        ;;
        -n|--name)
        name="$2"
        shift
        shift
        ;;
        -u|--user)
        user="$2"
        shift
        shift
        ;;
        -P|--password)
        password="$2"
        shift
        shift
        ;;
        -f|--file)
        file="$2"
        shift
        shift
        ;;
        *)
        # Unknown option
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

# Check if all required arguments are provided
if [[ -z $host || -z $port || -z $name || -z $user || -z $password || -z $file ]]
then
    echo "Missing required arguments!"
    echo "Usage: ./script.sh -h <host> -p <port> -n <name> -u <user> -P <password> -f <file>"
    exit 1
fi

# Test connection to the PostgreSQL database
PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$name" -c "SELECT 1" >/dev/null 2>&1
if [[ $? -ne 0 ]]
then
    echo "Failed to connect to the PostgreSQL database."
    exit 1
fi

# Load data from the file into the PostgreSQL database
PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$name" -f "$file"
if [[ $? -ne 0 ]]
then
    echo "Failed to load data into the PostgreSQL database."
    exit 1
fi

echo "Data loaded successfully from $file into the PostgreSQL database."
