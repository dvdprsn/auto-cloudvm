import os
import configparser
import subprocess
import vm_out


def read_azure(config_path):

    # If file does not exist
    if not os.path.exists(config_path):
        print("Config file does no exists!")
        return

    config = configparser.ConfigParser()
    config.read(config_path)
    # More than 10 VMs in config file
    if len(config.sections()) > 10:
        print("Cannot have more than 10 VM instances defined")
        return
    # For each VM in the config file
    for elem in config.sections():
        # Verify config contains min contents
        if not min_contents(config[elem]):
            print("Config contains missing descriptions")
            return
        handle_creation(config[elem])


def handle_creation(config):

    doc_items = ['purpose', 'os', 'team']
    az_command = ['az', 'vm', 'create']

    # !TODO: Cpu choice, Memory size, disk space
    # IMPORTANT -- Ports
    # We should only pull these lists once to save time

    # images = subprocess.run(['gcloud', 'compute', 'images', 'list', '--format=value(PROJECT, name)'], capture_output=True, text=True).stdout.split()
    # zones = subprocess.run(['gcloud', 'compute', 'zones', 'list', '--format=value(name)'], capture_output=True, text=True).stdout.split()

    # Capture name first to ensure it gets appended to the correct place
    if "name" in config:
        # Validate that the name follows the GCP expected
        # if not name_validation(config["name"]):
        #     print("Name for this VM description is invalid")
        #     return
        print(config["name"])
        # gcp_command.append(config['name'])
    else:
        print("Name not specified")
        return
    for key in config:
        if "image" == key:
            # Image not found in list
            # if not image_validation(config[key], images):
            #     print("This image does not exist")
            #     return
            print(config[key])
            # gcp_command.append(f'--image={config[key]}')
        elif "resource-group" == key:
            # Image project not found in list
            # if not image_validation(config[key], images):
            #     print("This image project does not exist")
            #     return
            print(config[key])
            # gcp_command.append(f'--image-project={config[key]}')
        elif "location" == key:
            # Zone not found in list
            # if not zone_validation(config[key], zones):
            #     print("This zone does not exist")
            #     return
            print(config[key])
        elif "resource-group" == key:
            # Zone not found in list
            # if not zone_validation(config[key], zones):
            #     print("This zone does not exist")
            #     return
            print(config[key])
            # gcp_command.append(f'--zone={config[key]}')
        elif key not in doc_items:
            az_command.append(f"--{key}={config[key]}")
    # print(" ".join(gcp_command))
    vm_out.create_log()
    # Uncomment to create VMs
    # creation_output = subprocess.run(gcp_command, capture_output=True, text=True).stdout
    # print(creation_output)


# def name_validation(name):
#     return all(c.islower() or c.isdigit() for c in name)


def image_validation(image, images):
    return any(item == image for item in images)


def loc_validation(loc, locs):
    return any(item == loc for item in locs)


def min_contents(config):
    # AZ has no project
    req_contents = ["name", "purpose", "resource-group", "team", "os", "image", "admin-username", "location"]
    return set(req_contents).issubset(config)
