import gcp_reader
import azure_reader
import vm_out


def main():

    gcp_out = gcp_reader.read_gcp("gcp.conf")
    az_out = azure_reader.read_azure("azure.conf")

    vm_out.create_log(az_out, gcp_out)


if __name__ == "__main__":
    main()
