import os
import subprocess
from datetime import datetime



def import_dashboards():
    print("Importing dashboards to Grafana, Please wait for the script to complete.")
    try:
        # Run the import command for the entire directory
        result = subprocess.run(
            ["grafana-import", "import", "-i", "./"],
            check=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Successfully imported dashboards.")
        else:
            print(f"Import failed. Error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to import dashboards: {e}")
        print(f"Error output: {e.stderr}")

def export_dashboards():
    # Create a new folder with the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_folder = f"grafana_exports_{timestamp}"
    os.makedirs(export_folder, exist_ok=True)

    print(f"Exporting dashboards to folder: {export_folder}")

    try:
        result = subprocess.run(
            ["grafana-import", "export", "--pretty", "-d", export_folder],
            check=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Dashboards exported successfully to {export_folder}.")
        else:
            print(f"Export failed. Error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to export dashboards: {e}")
        print(f"Error output: {e.stderr}")

if __name__ == "__main__":
    print("Choose an action:\n1. Import dashboards\n2. Export dashboards")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        import_dashboards()
    elif choice == "2":
        export_dashboards()
    else:
        print("Invalid choice. Exiting.")