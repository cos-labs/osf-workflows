# OSF Workflows

OSF Workflows is an open source workflow engine that allows users to quickly and easily create backends that implement collections of operations, visualize workflows as flowcharrts, and evaluate these workflows.

## Development

### Dependencies

* node.js / npm / bower
* Python 3.6 / pip / virtualenv
* Postgres 9.6 or greater

### Installation

#### Service
* create a new venv with python 3.6
* `pip install -r requirements`
* Create a local.py with an entry for `DATABASES` to connect to postgres
* Ensure DJANGO_SETTINGS_MODULE points to the correct settings file.
* Load fixtures if desired

#### Client App
* 
