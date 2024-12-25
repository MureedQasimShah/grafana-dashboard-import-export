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

if [[ "$choice" -eq 1 ]]; then
    # Import dashboards
    read -p "Enter the directory path containing dashboards to import: " dir_path

    if [[ -d "$dir_path" ]]; then
        echo "Importing dashboards from directory: $dir_path"
        grafana-import import -i "$dir_path"
        echo "Dashboards imported successfully!"
    else
        echo "Error: Directory '$dir_path' does not exist!"
        exit 1
    fi
elif [[ "$choice" -eq 2 ]]; then
    cd "exported_dashboard"
    echo "Exporting dashboards to directory: exported_dashboard"
    grafana-import export --pretty -d "ArgoCD"
    grafana-import export --pretty -d "CoreDNS"
    echo "Dashboards exported successfully to exported_dashboard directory!"
else
    echo "Invalid choice. Exiting."
    exit 1
fi