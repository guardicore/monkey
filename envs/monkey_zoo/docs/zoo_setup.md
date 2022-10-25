# Setting up a Monkey Zoo using Terraform

## Getting started:

Requirements:
1.  Have `terraform` installed (for installation instructions check this
    [link](https://learn.hashicorp.com/tutorials/terraform/install-cli)).
2.  Have a Google Cloud Platform account (upgraded if you want to test
    whole network at once).
3.  Have `gcloud` CLI installed (for installation instructions check this
    [link](https://cloud.google.com/sdk/docs/install#linux))
4.  Have `monkey/envs/monkey_zoo` folder downloaded as all the instructions are done
    in there.

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
    **Note: Ask monkey developers to add them. Check [Infection Monkey documentation](https://techdocs.akamai.com/infection-monkey/docs/welcome-infection-monkey) on how to recieve usage and support**.

        Compute Engine -> Compute image user

3.  Change configurations located in the
    ../monkey/envs/monkey\_zoo/terraform/config.tf file (don’t forget to
    link to your service account key file):

         provider "google" {

         project = "test-000000" // Change to your project id

           region  = "europe-west3" // Change to your desired region or leave default

           zone    = "europe-west3-b" // Change to your desired zone or leave default

           credentials = "${file("../gcp_keys/gcp_key.json")}" // Change to the location and name of the service key.
                                                               // If you followed instruction above leave it as is

         }

         locals {

           resource_prefix = "" // All of the resources will have this prefix.
                                // Only change if you want to have multiple zoo's in the same project

           service_account_email="tester-monkeyZoo-user@testproject-000000.iam.gserviceaccount.com" // Service account email

           monkeyzoo_project="guardicore-22050661" // Project where monkeyzoo images are kept. Leave as is.

         }

4.  Run terraform init

To deploy the network run:<br>
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
