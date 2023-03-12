import os
import configparser
import subprocess
import vm_out


def read_gcp(config_path):

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
    gcp_command = ['gcloud', 'compute', 'instances', 'create']
    gcp_portcommand = ['gcloud', 'compute', 'firewall-rules', 'create']
    doc_items = ['project', 'team', 'purpose', 'os', 'name', 'open-ports']
    hasPorts = False
    # IMPORTANT -- Ports
    # We should only pull these lists once to save time
    images = subprocess.run(['gcloud', 'compute', 'images', 'list', '--format=value(PROJECT, name)'], capture_output=True, text=True).stdout.split()
    zones = subprocess.run(['gcloud', 'compute', 'zones', 'list', '--format=value(name)'], capture_output=True, text=True).stdout.split()
    # Capture name first to ensure it gets appended to the correct place
    if "name" in config:
        # Validate that the name follows the GCP expected
        if not name_validation(config["name"]):
            print("Name for this VM description is invalid")
            return
        gcp_command.append(config['name'])
        gcp_command.append(f'--tags={config["name"]}')
        gcp_portcommand.append(config['name'])
        gcp_portcommand.append(f'--target-tags={config["name"]}')
    else:
        print("Name not specified")
        return
    for key in config:
        if "image" == key:
            # Image not found in list
            if not image_validation(config[key], images):
                print("This image does not exist")
                return
            gcp_command.append(f'--image={config[key]}')
        elif "imageproject" == key:
            # Image project not found in list
            if not image_validation(config[key], images):
                print("This image project does not exist")
                return
            gcp_command.append(f'--image-project={config[key]}')
        elif "zone" == key:
            # Zone not found in list
            if not zone_validation(config[key], zones):
                print("This zone does not exist")
                return
            gcp_command.append(f'--zone={config[key]}')
        elif "open-ports" == key:
            hasPorts = True
            port_list = config[key].split(',')
            gcp_portcommand.append("--action=ALLOW")
            gcp_portcommand.append(f"--rules={','.join(f'tcp:{item}' for item in port_list)}")
        elif key not in doc_items:
            gcp_command.append(f"--{key}={config[key]}")
            pass
    print(" ".join(gcp_command))
    # Uncomment to create VMs
    creation_output = subprocess.run(gcp_command, capture_output=True, text=True).stdout
    print(creation_output)
    if hasPorts:
        print(" ".join(gcp_portcommand))
        port_out = subprocess.run(gcp_portcommand, capture_output=True, text=True).stdout
        print(port_out)

    vm_out.create_log()


def name_validation(name):
    return all(c.islower() or c.isdigit() for c in name)


def image_validation(image, images):
    return any(item == image for item in images)


def zone_validation(zone, zones):
    return any(item == zone for item in zones)


def min_contents(config):
    req_contents = ["name", "project", "team", "purpose", "os", "image", "imageproject", "zone"]
    return set(req_contents).issubset(config)
