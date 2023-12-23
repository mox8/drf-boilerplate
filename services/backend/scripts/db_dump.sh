#!/bin/bash

# Default values
host=""
port=""
name=""
user=""
password=""
directory=""

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
        -d|--directory)
        directory="$2"
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
if [[ -z $host || -z $port || -z $name || -z $user || -z $password ]]
then
    echo "Missing required arguments!"
    echo "Usage: ./script.sh -h <host> -p <port> -n <name> -u <user> -P <password> [-d <directory>]"
    exit 1
fi

# Generate export file name with current date and time in ISO 8601 format
datetime=$(date -u +"%Y-%m-%dT%H:%M:%S")
export_file="${datetime}-${name}-dump.sql"

# Create the directory if it doesn't exist
if [[ -n $directory ]]
then
    mkdir -p "$directory"
    if [[ $? -ne 0 ]]
    then
        echo "Failed to create directory: $directory"
        exit 1
    fi

    export_file="$directory/$export_file"
fi

# Test connection to the PostgreSQL database
PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$name" -c "SELECT 1" >/dev/null 2>&1
if [[ $? -ne 0 ]]
then
    echo "Failed to connect to the PostgreSQL database."
    exit 1
fi

# Create SQL dump and save it to the export file
PGPASSWORD="$password" pg_dump -h "$host" -p "$port" -U "$user" -d "$name" -f "$export_file"
if [[ $? -ne 0 ]]
then
    echo "Failed to create SQL dump."
    exit 1
fi
# Calculate the size of the dump in megabytes
dump_size=$(du -h -m "$export_file" | awk '{print $1}')

echo "SQL dump created successfully and saved to $export_file. Size: $dump_size MB."