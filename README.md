# FIWARE-CEF JIRA Synchronisation

[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Synchronisation tool between CEF Building Block and FIWARE JIRAs.

## Install

### Requirements

The following software must be installed:

- Python 3.7
- pip
- virtualenv


### Installation

The recommend installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies, because the python code do not need 
installation.

1. Clone this repository.
2. Define the configuration file, sample in ``./jirasync/conf/jirasync.ini``
3. Create the virtualenv ``virtualenv -p python3.7 env``.
4. Activate the virtualenv and download requirements ``source ./env/bin/activate``.

The script is searching the configuration parameters or in the ``/etc/init.d``
directory or in the environment variables. Firstly, The script try to find if there 
is defined an environment variable whose name is ``CEF_SYNC_CONFIGFILE``. 
If the script cannot get this environment variable, it tries to find the file 
``jirasync.ini`` in ``/etc/init.d`` directory. In any oder case or the file does 
not exist, the scripts will give you an error.

[Top](#fiware-cef-jira-synchronisation)


## Execution

To execute the scripts, you only need to execute the following command:

```console
./jirasync.py <command>
```

Where command could be one of the following:
- **status**, provide the current status of pending synchronization issues.
- **create**, take the new open CEF Jira issues and create the corresponding FIWARE Jira issue together with a new register
in the synchronization DB.
- **update**, update the status of a closed FIWARE Jira issue in the corresponding CEF Jira issue together with any comments
on the issue.
- **sync**, make the operation of create and update in that order.

[Top](#fiware-cef-jira-synchronisation)


### Execute with the corresponding docker image

In order to execute the corresponding docker images, you can take a look to the documentation provided in
docker folder, [How to execute it using docker](docker/README.md)

[Top](#fiware-cef-jira-synchronisation)


## License

These scripts are licensed under Apache License 2.0.
