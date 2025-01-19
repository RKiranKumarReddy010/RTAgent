import winapps
import os
import csv
from datetime import datetime

def get_installed_applications():
    """Retrieve detailed information about installed applications."""
    applications = []
    for app in winapps.list_installed():
        app_info = {
            'Name': app.name,
            'Version': app.version,
            'Publisher': app.publisher,
            'Install Date': app.install_date,
            'Install Location': str(app.install_location),
            'Uninstall String': app.uninstall_string
        }
        applications.append(app_info)
    return applications

def scan_application_directory(app_location):
    """Scan the directory structure of an application."""
    if not os.path.exists(app_location):
        return []
    
    file_structure = []
    for root, dirs, files in os.walk(app_location):
        for file in files:
            full_path = os.path.join(root, file)
            file_info = {
                'Path': full_path,
                'Size': os.path.getsize(full_path),
                'Modified': datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
            }
            file_structure.append(file_info)
    
    return file_structure

def export_to_csv(applications, filename='installed_apps.csv'):
    """Export application information to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Version', 'Publisher', 'Install Date', 'Install Location', 'Uninstall String']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for app in applications:
            writer.writerow(app)

def export_file_structure_to_csv(file_structures, filename='app_file_structures.csv'):
    """Export application file structures to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Path', 'Size', 'Modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for structure in file_structures:
            writer.writerow(structure)

def main():
    # Get installed applications
    installed_apps = get_installed_applications()
    
    # Export application information
    export_to_csv(installed_apps)
    
    # Scan and export file structures for each application
    all_file_structures = []
    for app in installed_apps:
        if app['Install Location'] and app['Install Location'] != 'None':
            try:
                file_structure = scan_application_directory(app['Install Location'])
                all_file_structures.extend(file_structure)
            except Exception as e:
                print(f"Could not scan {app['Name']}: {e}")
    
    # Export file structures
    export_file_structure_to_csv(all_file_structures)
    
    print("Application scan completed. Check 'installed_apps.csv' and 'app_file_structures.csv'")

if __name__ == "__main__":
    main()
