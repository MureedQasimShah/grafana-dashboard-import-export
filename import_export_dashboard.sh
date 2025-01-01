#!/bin/bash

# Ensure the script exits on error and prints commands for debugging
set -e

# Function to check if a Python package is installed
check_python_package() {
    package=$1
    if ! python3 -c "import $package" &>/dev/null; then
        return 1 # Package is not installed
    else
        return 0 # Package is installed
    fi
}

# Function to import dashboards with error handling
import_dashboards() {
    local dir_path=$1
    
    # Check if directory exists and contains JSON files
    if [[ ! -d "$dir_path" ]]; then
        echo "Error: Directory '$dir_path' does not exist!"
        exit 1
    fi
    
    # Check if directory contains JSON files
    if ! find "$dir_path" -name "*.json" -print -quit | grep -q .; then
        echo "Error: No JSON files found in '$dir_path'!"
        exit 1
    fi
    
    echo "Importing dashboards from directory: $dir_path"
    for json_file in "$dir_path"/*.json; do
        echo "Processing: $json_file"
        grafana-import import -i "$json_file" || {
            echo "Error importing $json_file"
            continue
        }
    done
}

# Function to export dashboards with error handling
export_dashboards() {
    local export_dir="exported_dashboards"
    
    # Create export directory if it doesn't exist
    mkdir -p "$export_dir"
    
    echo "Exporting dashboards to directory: $export_dir"
    
    # Export each dashboard type to its own subdirectory
    for dashboard in "ArgoCD" "CoreDNS"; do
        mkdir -p "$export_dir/$dashboard"
        echo "Exporting $dashboard dashboards..."
        grafana-import export --pretty -d "$export_dir/$dashboard" || {
            echo "Error exporting $dashboard dashboards"
            continue
        }
    done
}

# Check if grafana-import is installed
echo "Checking if 'grafana-import' is installed..."
if check_python_package "grafana_import"; then
    echo "'grafana-import' is already installed. Skipping installation."
else
    echo "'grafana-import' is not installed. Installing now..."
    pip install --upgrade 'grafana-import[builder]'
fi

# Set the Grafana URL environment variable
export GRAFANA_URL="http://admin:hello123@localhost:3000"
echo "Grafana URL set to: $GRAFANA_URL"

# Menu to select action
echo "Choose an action:"
echo "1. Import dashboards"
echo "2. Export dashboards"
read -p "Enter your choice (1 or 2): " choice

case "$choice" in
    1)
        read -p "Enter the directory path containing dashboards to import: " dir_path
        import_dashboards "$dir_path"
        echo "Dashboard import process completed!"
        ;;
    2)
        export_dashboards
        echo "Dashboard export process completed!"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac