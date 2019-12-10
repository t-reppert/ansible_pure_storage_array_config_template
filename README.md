# Pure Storage Array Standard Configuration Ansible Playbooks

These playbooks are designed to either gather and list current Pure Array configuration (infra_facts.yml) or to check/apply standard configuration against target Pure Arrays(infra.yml)

Pure Array standard settings are defined and maintained in the *group_vars/all/vars_file.yml* file

## Requirements

- Ansible 2.8+
- Latest Pure Storage Ansible Modules (see https://galaxy.ansible.com/purestorage/flasharray)
    - These may need to be manually downloaded and added to the Ansible module path under *ansible/modules/storage/purestorage*
        - purefa_alert.py
        - purefa_banner.py
        - purefa_phonehome.py
        - purefa_proxy.py
        - purefa_smtp.py
        - purefa_snmp.py
        - purefa_syslog.py

- See requirements.txt for more requirements
- Vault password file (~/.vault-pass)
- TCP Ports 443 and 22 open between Ansible server and Pure Arrays

## Setup

- `git clone https://github.com/t-reppert/ansible_pure_storage_array_config_template`
- `cd ansible_pure_storage_array_config_template`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- Make sure ~/.vault-pass has correct vault password
- Make sure the latest modules mentioned in previous section are downloaded and copied into *venv/lib/python3.6/site-packages/ansible/modules/storage/purestorage/*
- To test, execute the following:  `ansible-playbook infra_facts.yml --tags api`

## Adding/Removing Pure Arrays

### Adding

- To add a new Pure array to the playbooks, you will need the following:
    - The FQDN of the Pure array
    - The API token from the Pure array
        - ssh into the Pure array as *pureuser* and run this command to get the API token:
            - `pureadmin list --api-token --expose` to get the api-token
- Once you have the above, you need to login to the Ansible control host where this repo was setup and create the encrypted token to copy into the var_files.yml for the new Pure array using the following command:
    - `ansible-vault encrypt_string --stdin-name api_token`
    - Paste in the api-token (collected in previous steps) and hit Ctrl-D to get the encrypted output
- Create a new entry for the array in the *group_vars/all/vars_file.yml* file under the pure_arrays_all section
    - Follow the same format as the other entries, providing the new array name, fa_url, ds_url, and api_token generated in the previous step
- Add the FQDN to the *arrays* file under each appropriate section or create a new section if needed

### Removing

- To remove a Pure array from the playbooks, perform the following steps:
    - Remove the array entry from the *group_vars/all/vars_file.yml* file
    - Remove all FQDN entries of the array from the *arrays* file

## Choosing the *target arrays* to execute playbooks against

- To select which Pure arrays to target the playbooks against, modify the *group_vars/all/vars_file.yml* file and change the *target_arrays* to have the array group alias ending in "_opts" you wish to run the playbooks against
    - For example:  `<<: *pure_arrays_nonprod_opts`


## Executing the *infra_facts.yml* playbook

- To produce an output of standard configuration info from the list of target arrays, execute the following playbook
    - `ansible-playbook infra_facts.yml`
    - If SSH is not yet available to the arrays from the Ansible control station you are running the playbooks from:
        - `ansible-playbook infra_facts.yml --tags api`
    - If you wish to only run the SSH portion used to check on SMI-S settings of the *infra_facts.yml* playbook:
        - `ansible-playbook infra_facts.yml --tags smis`
    
## Executing the *infra.yml* playbook

- To check/apply the **FULL** Pure Array standard configuration against the target Pure arrays, execute the following playbook
    - `ansible-playbook infra.yml`
    - If SSH is not yet available to the arrays from the Ansible control station you are running the playbook from:
        - `ansible-playbook infra.yml --tags api`
    - If you wish to only run the SSH portion used to apply/check SMI-S settings:
        - `ansible-playbook infra.yml --tags smis`

- To perform *selective* check/apply of the Pure Array standard configuration against the target Pure arrays, perform the following utilizing a comma-separated list of the chosen tags(configurations) to check/apply
    - Tags to choose from:
        - monitor
        - alert_email
        - banner
        - dns
        - ds
        - ntp
        - phonehome
        - proxy
        - smtp
        - syslog
    - Example: `ansible-playbook infra.yml --tags dns,ntp,proxy,syslog`

## Tools

- To help quickly change the target_arrays setting in the vars_file.yml, the following tool was built and :
    - pure_targets_select.py
        - Examples:

                $ python pure_targets_select.py --h
                usage: pure_targets_select.py [-h] [--t | --n | --p | --a]
            
                optional arguments:
                -h, --help  show this help message and exit
                --t         Select Test Pure Arrays list for Ansible
                --n         Select Non-Prod Pure Arrays list for Ansible
                --p         Select Prod Pure Arrays list for Ansible
                --a         Select ALL Pure Arrays list for Ansible

                $ python pure_targets_select.py --t

                Current target setting: Non-Production
                Switching to: [Test]
                Current target setting: Test
 
- To help determine if a Linux server attached to a Pure Storage Array has the appropriate settings enabled, the included Ansible playbook, `pure_linux_settings.yml`, can be used.  The target hosts can be adjusted to point to appropriate host lists for scanning.  Unfortunately, this playbook has not been fully tested yet due to lack of available test servers/arrays.
