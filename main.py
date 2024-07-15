import os
import xml.etree.ElementTree as ET

import requests

project_directory_path = '/folder/path/containing/dotnet_projects'


def print_separator():
    print("-" * 25)


def identify_package_mismatch(proj_packages: list):
    mismatch_found = False
    for outer_package in proj_packages[0:]:
        for inner_package in proj_packages[1:]:
            outer_package_name = outer_package[1]
            outer_package_version = outer_package[2]
            inner_package_name = inner_package[1]
            inner_package_version = inner_package[2]
            if outer_package_name == inner_package_name and outer_package_version != inner_package_version:
                mismatch_found = True
                print(
                    f'Mismatch found, {outer_package[0]} contains {outer_package_name} {outer_package_version} whereas {inner_package[0]} contains {inner_package_name} {inner_package_version}')

    if not mismatch_found:
        print('No package mismatch found')
    return


def identify_newer_package_version(proj_packages: list):
    new_version_found = False
    for package in proj_packages[0:]:
        package_name = package[1]
        package_version = package[2]

        package_uri = f"https://api.nuget.org/v3-flatcontainer/{
            package_name}/index.json"
        data = requests.get(package_uri)
        version_json = data.json()
        package_latest_version = None

        for version in version_json['versions']:
            if not ('beta' in version or 'alpha' in version or 'preview' in version or 'dev' in version or 'release' in version) or \
                    ('beta' in package_version and 'beta' in version):
                package_latest_version = version

        if package_latest_version and package_latest_version != package_version:
            new_version_found = True
            print(
                f'Package {package_name} in {package[0]} file can be upgraded from {package_version} to {package_latest_version}')

    if not new_version_found:
        print('No newer package version was found')
    return


def identify_nuget_package_versions() -> list:
    package_list = []

    for current_dir_path, current_subdirs, current_files in os.walk(project_directory_path):
        for aFile in current_files:
            if aFile.endswith(".csproj"):
                prj_file_path = os.path.join(current_dir_path, aFile)
                print(f'Processing {prj_file_path}')

                with open(prj_file_path, 'r') as project_file:
                    file_content = str.replace(
                        str.join('', project_file.readlines()), '\n', '')

                    # print(file_content)
                    tree = ET.fromstring(file_content)

                    for item in tree.findall('ItemGroup'):
                        for package_ref in item.findall('PackageReference'):
                            package_list.append((aFile,
                                                 package_ref.get('Include'),
                                                 package_ref.get('Version')))
                        break
                    break

    return package_list


# Identify all the nuget packages used in project(s)
project_packages = identify_nuget_package_versions()
print_separator()

# Identify any mismatch between nuget package(s) used in the project(s)
identify_package_mismatch(project_packages)
print_separator()

# Identify if any newer package version is available
identify_newer_package_version(project_packages)
print_separator()
