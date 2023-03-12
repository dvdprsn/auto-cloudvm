import gcp_reader
import azure_reader
import vm_out


def main():
    # might need to capture and set the gcloud project via input before running
    # gcloud config set project PROJECT_ID

    # gcp_out = gcp_reader.read_gcp("gcp.conf")
    az_out = azure_reader.read_azure("azure.conf")

    gcp_out = []
    vm_out.create_log(az_out, gcp_out)


if __name__ == "__main__":
    main()
