# Grafana Dashboard Import/Export Script

This script allows you to easily import and export Grafana dashboards. It interacts with the [grafana-import](https://github.com/grafana/grafana-import) Python package to facilitate importing and exporting dashboards from your Grafana instance.

## Features
- **Import dashboards**: Import dashboards from a specified directory.
- **Export dashboards**: Export specific dashboards to a designated directory.
  
## Prerequisites
- **Grafana** instance up and running.
Use the below command to run the grafana locally for the testing.

docker run --rm -it --name=grafana --publish=3000:3000 \
  --env='GF_SECURITY_ADMIN_PASSWORD=admin' grafana/grafana:latest

- **Python 3** installed on the system.
- **pip** for installing dependencies.
pip install --upgrade 'grafana-import[builder]'
- **grafana-import** package installed (the script will install it if necessary).

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/MureedQasimShah/grafana-dashboard-import-export.git
   cd grafana-dashboard-import-export

## Install required dependencies:
pip install --upgrade 'grafana-import[builder]'

## Configure the script:

Modify the GRAFANA_URL variable in the script to match your Grafana instance. Example:
export GRAFANA_URL="http://admin:admin@localhost:3000"

Ensure the dashboard names or directories you want to export are correctly specified in the script. By default, it will export ArgoCD and CoreDNS.

## Run the script:
./import_export_dashboard.sh
You'll be prompted to choose an action:

- **1** to import dashboards
- **2** to export dashboards

## Example Usage
- **Importing dashboards**:


./import_export_dashboard.sh
Enter the directory containing your dashboards when prompted.

- **Exporting dashboards**: The script will automatically export the ArgoCD and CoreDNS dashboards to the exported_dashboard directory.

## Notes
This script assumes that your Grafana instance is running on http://localhost:3000 with default credentials (admin:hello123).
You can modify the script to support more customized configurations, like different Grafana URLs or authentication methods.
