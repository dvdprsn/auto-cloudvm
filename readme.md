# CIS\*4010 VM Creation

David Pearson

1050197

## Usage

- Have files gcp.conf and azure.conf ready in the project directory
- Requires GCP CLI and Azure CLI

execute `python3 automate.py`

- To open ports, add `open-ports = port[,ports]` to the VM conf
- Any additional variables can be added with no issues, although it must follow the documenation for the perspective cloud provider
  - For example the tag `custom-memory = 3072MB` to a GCP vm conf

## Assumptions

- For GCP VMs it is assumed the user has already selected a valid project using `gcloud init`
- Azure CLI must be signed in
- For Azure Windows VMs it is assumed that the config will contain `admin-password` as this is required
- For Azure Linux VMs ssh keys will be automatically generated
- The OS defined in the config is used to determine whether or not SSH keys are generated or admin-password should be validated and used for Azure VMs
- Error handling is fairly good but generally correct inputs are expected
- Azure requires at least the following tags: ["name", "purpose", "resource-group", "team", "os", "image", "admin-username", "location"]
  - If a windows VM is being created then `admin-password` is also required
- GCP requires at least the following tags: ["name", "project", "team", "purpose", "os", "image", "imageproject", "zone"]
