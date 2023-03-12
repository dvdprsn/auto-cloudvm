import os
import pwd
import datetime


def create_log(az_log, gcp_log):

    ts_string = get_timestamp()
    with open(f'VMcreation_{ts_string}.txt', 'w') as f:
        f.write(f"Time Stamp: {ts_string}\n")
        f.write(f"Admin Username: {pwd.getpwuid(os.getuid())[0]}\n")
        f.write("---------GCP VMs---------\n")
        for o in gcp_log:
            f.write('\n')
            f.write(o)
        f.write("----------AZURE VMs--------\n")
        for o in az_log:
            f.write('\n')
            f.write(o)

    move_conf("gcp.conf", ts_string)
    move_conf("azure.conf", ts_string)


def move_conf(config_path, ts):
    if not os.path.exists(config_path):
        return
    conf_name = config_path.replace(".conf", "")
    os.rename(config_path, conf_name + f"_{ts}.conf")


def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d;%H;%M;%S")
