# Setting up a Monkey Zoo using Terraform

## Getting started:

Requirements:

- Have `monkey/envs/monkey_zoo` folder downloaded as it contains all the instructions.

- For building images:
    1.  Have `packer` installed.
        [[Installation instructions](https://developer.hashicorp.com/packer/tutorials/docker-get-started/get-started-install-cli)]
    2.  Have `ansible` installed.
        [[Installation instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible)]

- For deploying instances:
    1.  Have `terraform` installed.
        [[Installation instructions](https://learn.hashicorp.com/tutorials/terraform/install-cli)]

- For using the Google Cloud Platform (GCP):
    1.  Have a Google Cloud Platform account (upgraded if you want to test
        whole network at once).
    2.  Have `gcloud` CLI installed.
        [[Installation instructions](https://cloud.google.com/sdk/docs/install#linux)]


To deploy:
1.  Configure service account for your project:

    a. Create a service account (GCP website -> IAM & Admin -> Service Accounts -> + CREATE SERVICE ACCOUNT) and name it “your\_name-monkeyZoo-user”

    b. Give these permissions to your service account:

        Compute Engine -> Compute Network Admin
        Compute Engine -> Compute Instance Admin (v1)
        Compute Engine -> Compute Security Admin
        Service Account User

    or just give

        Project -> Owner
        Note: Adds more permissions then are needed

    c. Create and download its `Service account key` in JSON and place it in `monkey_zoo/gcp_keys` as `gcp_key.json`.

2.  Get these permissions in our monkeyZoo production project (guardicore-22050661) for your service account.<br>
    **Note: Ask monkey developers to add them. Check [Infection Monkey documentation](https://techdocs.akamai.com/infection-monkey/docs/welcome-infection-monkey) on how to receive usage and support**.

        Compute Engine -> Compute image user

3.  (Optional) Generate images

    To build the images, run the script located at `envs/monkey_zoo/build_images.sh`, providing it:
        - The target project in which the images will be stored
        - The account file, e.g. `gcp_key.json`
        - The packer files to build

    For example,

        `build_images.sh -p guardicore-22050661 --account-file gcp_keys/gcp_key.json` packer/tunneling.pkr.hcl

4.  Change configurations located in the
    ../monkey/envs/monkey\_zoo/terraform/config.tf file (don’t forget to
    link to your service account key file):

         provider "google" {

           // Change to your project id
           project = "test-000000"

           // Change to your desired region or leave default
           region  = "europe-west3"

           // Change to your desired zone or leave default
           zone    = "europe-west3-b"

           // Change to the location and name of the service key. If you followed the instructions above, leave it as is
           // The account must have permissions to use the service account in the below section
           credentials = file("../gcp_keys/gcp_key.json")
         }

         locals {

           // All of the resources will have this prefix.
           // Only change if you want to have multiple zoos in the same project
           resource_prefix = ""

           // Service account email. This service account must have permissions to modify instances on your project.
           service_account_email="tester-monkeyZoo-user@testproject-000000.iam.gserviceaccount.com"

           // Project where monkeyzoo images are kept. Leave as is.
           // If deploying images generated using the build_images.sh script,
           // set to the same project provided to the -p option.
           monkeyzoo_project="guardicore-22050661"
         }

5.  Deploy the zoo

    `terraform init`<br>
    `cd ../monkey/envs/monkey_zoo/terraform`<br>
    `terraform plan` (review the changes it will make on GCP)<br>
    `terraform apply` (adds machines to these networks)


## Using MonkeyZoo islands:

### How to get into the islands:

`island-linux-250`: SSH from GCP

`island-windows-251`: In GCP/VM instances page click on
`island-windows-251`. Set password for your account and then RDP into
the island.

You can find more information on MonkeyZoo machines in [MonkeyZoo network](zoo_network.md).


## Installing Monkey Island in MonkeyZoo

### For users

Depending on your preferred operating system login to `island-linux-250` for Linux and
`island-windows-251` for Windows. After successful login refer to our
[setup guide](https://techdocs.akamai.com/infection-monkey/docs/setting-up-infection-monkey) on next steps.

### For developers

To set up a development environment in the MonkeyZoo island refer to our
[development setup](https://techdocs.akamai.com/infection-monkey/docs/development-setup).

## Using the MonkeyZoo

Refer to the [blackbox tests documentation](../blackbox/README.md) to understand how MonkeyZoo test
network can be used.
