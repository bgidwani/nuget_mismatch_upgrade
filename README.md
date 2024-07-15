# Nuget Package comparison tool

Script to compare `nuget` packages used in the dotnet projects under specified folder. This outlines any issue(s) and/or any available upgrades for the `nuget` packages used in the projects

## Usage

- Ensure Python is installed on the machine
- Launch terminal window and navigate to this folder
- Setup virtual environment using `python3 -m venv venv` command
- Install any missing dependencies using `pip install -r requirements.txt` command
- Run `python3 main.py`

The output displayed will outline

- Package version mismatch between project(s) e.g. if `Project 1` is using `AutoMapper v13` whereas `Project 2` is using `AutoMapper v12`, the output will display message outlining version mismatch
- Availbility of newer nuget package version for upgraded e.g. if `Project 1` contains `AutoMapper v12` and `AutoMapper v13` is available, the output will display message outlining upgrade to `v13` available for `AutoMapper` in `Project 1`
