# OSF Workflows

[![Join the chat at https://gitter.im/cos-labs/osf-workflows](https://badges.gitter.im/cos-labs/osf-workflows.svg)](https://gitter.im/cos-labs/osf-workflows?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

OSF Workflows is an open source workflow engine that allows users to quickly and easily create backends that implement collections of operations to define workflows, visualize workflows as flowcharts, and evaluate these workflows.

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
* install npm and bower dependencies
* `ember s`
