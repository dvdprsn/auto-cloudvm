import gcp_reader
import azure_reader


def main():
    # might need to capture and set the gcloud project via input before running
    # gcloud config set project PROJECT_ID

    # gcp_reader.read_gcp("gcp.conf")
    azure_reader.read_azure("azure.conf")


if __name__ == "__main__":
    main()
