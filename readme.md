# CIS\*4010 VM Creation

David Pearson

1050197

## Usage

- Have files gcp.conf and azure.conf ready in the project directory

execute `python3 automate.py`

## Assumptions

- For GCP VMs it is assumed the user has already selected a valid project using `gcloud init`
- For Azure Windows VMs it is assumed that the config will contain `admin-password` as this is required
- For Azure Linux VMs ssh keys will be automatically generated
- The OS defined in the config is used to determine whether or not SSH keys are generated or admin-password should be validated and used
