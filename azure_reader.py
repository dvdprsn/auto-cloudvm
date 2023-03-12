import os
import configparser
import subprocess
import vm_out
import re


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

    doc_items = ['purpose', 'os', 'team', 'name', 'location']
    az_command = ['az', 'vm', 'create']
    az_portcommand = ['az', 'vm', 'open-port']
    open_ports = False
    name = ''
    location = ''
    resource_group = ''

    # Capture name first to ensure it gets appended to the correct place
    if "name" in config:
        name = config['name']
        az_command.append("--name")
        az_command.append(config['name'])
    else:
        # Change error here
        print("Name not specified")
        return

    # Get location
    if "location" in config:
        location = config['location']
        az_command.append("--location")
        az_command.append(config['location'])
    else:
        print("Location not found in config")
        return

    # Get and create resource group if needed
    if "resource-group" in config:
        resource_group = config['resource-group']
        # Does the resource-group already exist
        rgExists = subprocess.run(['az', 'group', 'exists', '--name', resource_group], capture_output=True, text=True).stdout
        # If it does not create it
        if 'false' in rgExists:
            # create resource group
            print(f'az group create --name {resource_group} --location {location}')
            rgCreate = subprocess.run(['az', 'group', 'create', '--name', resource_group, '--location', location], capture_output=True, text=True).stdout
            print(rgCreate)
        az_command.append('--resource-group')
        az_command.append(resource_group)
    else:
        print("resource-group not found in config")
        return

    # Handle OS specific requirements
    if 'os' not in config:
        print("OS must be defined in config")
        return
    if 'linux' in config['os']:
        az_command.append('--generate-ssh-keys')
    elif 'windows' in config['os']:
        if "admin-password" in config:
            az_command.append("--admin-password")
            # Validate password
            if pass_validation(config['admin-password']):
                az_command.append(config['admin-password'])
            else:
                # Password validation failed
                return
        else:
            print("admin-password required for windows VMs on Azure")
            return
    else:
        print("OS should be linux or windows")
        return

    # For all other keys in the file
    for key in config:
        if "image" == key:
            az_command.append('--image')
            az_command.append(config[key])
        elif "admin-username" == key:
            az_command.append('--admin-username')
            az_command.append(config[key])
        elif "open-ports" == key:
            open_ports = True
            az_portcommand.append('--port')
            az_portcommand.append(config[key])
            az_portcommand.append('--resource-group')
            az_portcommand.append(resource_group)
            az_portcommand.append('--name')
            az_portcommand.append(name)
        elif key not in doc_items:
            az_command.append(f"--{key}")
            az_command.append(config[key])

    print(" ".join(az_command))
    # Uncomment to create VMs
    # creation_output = subprocess.run(az_command, capture_output=True, text=True).stdout
    # print(creation_output)
    if open_ports:
        # port_output = subprocess.run(az_portcommand, capture_output=True, text=True).stdout
        # print(port_output)
        pass

    vm_out.create_log()


def image_validation(image, images):
    return any(item == image for item in images)


def loc_validation(loc, locs):
    return any(item == loc for item in locs)


def pass_validation(password):
    if not (any(c.islower() for c in password)):
        print('admin-password must contain 1 lowercase')
        return False
    if not (any(c.isupper() for c in password)):
        print('admin-password must contain 1 uppercase')
        return False
    if not (any(c.isdigit() for c in password)):
        print('admin-password must contain a number')
        return False
    if (len(password) <= 12 or len(password) >= 123):
        print("admin-password must be between 12 and 123 characters")
        return False
    if not (re.search('[\\W_]', password)):
        print("admin-password must contain a special character")
        return False
    return True


def min_contents(config):
    # AZ has no project or should it??
    req_contents = ["name", "purpose", "resource-group", "team", "os", "image", "admin-username", "location"]
    return set(req_contents).issubset(config)
