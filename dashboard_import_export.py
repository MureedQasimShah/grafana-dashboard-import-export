import os
import subprocess
import sys
import shutil

def check_python_package(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def import_dashboards(dir_path):
    if not os.path.isdir(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist!")
        sys.exit(1)

    if not any(fname.endswith('.json') for fname in os.listdir(dir_path)):
        print(f"Error: No JSON files found in '{dir_path}'!")
        sys.exit(1)

    print(f"Importing dashboards from directory: {dir_path}")
    for json_file in os.listdir(dir_path):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(dir_path, json_file)
            print(f"Processing: {json_file_path}")
            result = subprocess.run(['grafana-import', 'import', '-i', json_file_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error importing {json_file_path}: {result.stderr}")

def export_dashboards():
    export_dir = input("Enter the directory path where you want to export the dashboards: ")

    if not os.path.isdir(export_dir):
        print(f"Error: Directory '{export_dir}' does not exist!")
        sys.exit(1)

    print(f"Exporting dashboards to directory: {export_dir}")

    dashboards = ["ArgoCD", "CoreDNS"]
    for dashboard in dashboards:
        print(f"Exporting {dashboard} dashboards...")
        output_file = os.path.join(export_dir, f"{dashboard}.json")
        result = subprocess.run(
            ['grafana-import', 'export', '--pretty', '-d', dashboard],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error exporting {dashboard} dashboards: {result.stderr}")
        else:
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            print(f"Exported {dashboard} dashboard to {output_file}")

def main():
    print("Checking if 'grafana-import' is installed...")
    if check_python_package("grafana_import"):
        print("'grafana-import' is already installed. Skipping installation.")
    else:
        print("'grafana-import' is not installed. Installing now...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'grafana-import[builder]'])

    os.environ["GRAFANA_URL"] = "http://admin:hello123@localhost:3000"
    print(f"Grafana URL set to: {os.environ['GRAFANA_URL']}")

    print("Choose an action:")
    print("1. Import dashboards")
    print("2. Export dashboards")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        dir_path = input("Enter the directory path containing dashboards to import: ")
        import_dashboards(dir_path)
        print("Dashboard import process completed!")
    elif choice == '2':
        export_dashboards()
        print("Dashboard export process completed!")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()