import os
import configparser
import subprocess


def read_gcp(config_path):
    res = []
    # If file does not exist
    if not os.path.exists(config_path):
        print("GCP Config file does no exists!")
        return res

    config = configparser.ConfigParser()
    config.read(config_path)
    # More than 10 VMs in config file
    if len(config.sections()) > 10:
        print("Cannot have more than 10 GCP VM instances defined")
        return res
    # For each VM in the config file
    for elem in config.sections():
        # Verify config contains min contents
        if not min_contents(config[elem]):
            print("GCP Config contains missing descriptions")
            return res
        res.append(handle_creation(config[elem]))

    return res


def handle_creation(config):
    gcp_command = ['gcloud', 'compute', 'instances', 'create']
    gcp_portcommand = ['gcloud', 'compute', 'firewall-rules', 'create']
    # Ignore these tags
    doc_items = ['project', 'team', 'purpose', 'os', 'name', 'open-ports']
    hasPorts = False

    # We should only pull these lists once to save time
    images = subprocess.run(['gcloud', 'compute', 'images', 'list', '--format=value(PROJECT, name)'], capture_output=True, text=True).stdout.split()
    zones = subprocess.run(['gcloud', 'compute', 'zones', 'list', '--format=value(name)'], capture_output=True, text=True).stdout.split()

    name = ''
    # Capture name first to ensure it gets appended to the correct place
    if "name" in config:
        # Validate that the name follows the GCP expected
        if not name_validation(config["name"]):
            print(f"Name ({config['name']}) for this VM description is invalid")
            return ''
        name = config['name']
        gcp_command.append(config['name'])
        gcp_command.append(f'--tags={config["name"]}')
        gcp_portcommand.append(config['name'])
        gcp_portcommand.append(f'--target-tags={config["name"]}')
    else:
        print("GCP VM Name not specified")
        return ''

    # Check if VM with same name already exists
    test_vm = subprocess.run(['gcloud', 'compute', 'instances', 'list'], capture_output=True, text=True).stdout
    if name in test_vm:
        print(f"A VM with this name ({name}) already exists")
        return ''

    for key in config:
        if "image" == key:
            # Image not found in list
            if not image_validation(config[key], images):
                print(f"This image ({config[key]}) does not exist")
                return ''
            gcp_command.append(f'--image={config[key]}')
        elif "imageproject" == key:
            # Image project not found in list
            if not image_validation(config[key], images):
                print(f"This image project ({config[key]}) does not exist")
                return ''
            gcp_command.append(f'--image-project={config[key]}')
        elif "zone" == key:
            # Zone not found in list
            if not zone_validation(config[key], zones):
                print(f"This zone ({config[key]}) does not exist")
                return ''
            gcp_command.append(f'--zone={config[key]}')
        elif "open-ports" == key:
            hasPorts = True
            port_list = config[key].split(',')
            gcp_portcommand.append("--action=ALLOW")
            gcp_portcommand.append(f"--rules={','.join(f'tcp:{item}' for item in port_list)}")
        elif key not in doc_items:
            gcp_command.append(f"--{key}={config[key]}")
    print(" ".join(gcp_command))
    creation_output = subprocess.run(gcp_command, capture_output=True, text=True).stdout
    print(creation_output)
    if hasPorts:
        print(" ".join(gcp_portcommand))
        subprocess.run(gcp_portcommand, capture_output=True, text=True).stdout

    return format_output(config, creation_output, hasPorts)


def format_output(config, creation_output, hasPorts):

    ret_string = ''
    name = config['name']
    project = ''
    if 'project' in config:
        project = config['project']
    purpose = config['purpose']
    team = config['team']
    os = config['os']

    ret_string += f"Name: {name}\n"
    ret_string += f"Project: {project}\n"
    ret_string += f"Purpose: {purpose}\n"
    ret_string += f"Team: {team}\n"
    ret_string += f"OS: {os}\n"

    if hasPorts:
        ret_string += f"Opened Ports: {config['open-ports']}\n"
    ret_string += f"Status: \n {creation_output} \n"
    return ret_string


def name_validation(name):
    return all(c.islower() or c.isdigit() for c in name)


def image_validation(image, images):
    return any(item == image for item in images)


def zone_validation(zone, zones):
    return any(item == zone for item in zones)


def min_contents(config):
    req_contents = ["name", "project", "team", "purpose", "os", "image", "imageproject", "zone"]
    return set(req_contents).issubset(config)
