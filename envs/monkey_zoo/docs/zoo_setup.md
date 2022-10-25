# Setting up a Monkey Zoo using Terraform

## Getting started:

Requirements:
1.  Have `terraform` installed (for installation instructions check this
    [link](https://learn.hashicorp.com/tutorials/terraform/install-cli)).
2.  Have a Google Cloud Platform account (upgraded if you want to test
    whole network at once).
3.  Have `gcloud` installed (for installation instructions check this
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
        **Note: Adds more permissions then are needed**

    c. Create and download its `Service account key` in JSON and place it in `monkey_zoo/gcp_keys` as `gcp_key.json`.

2.  Get these permissions in our monkeyZoo production project (guardicore-22050661) for your service account.<br>
    **Note: Ask monkey developers to add them. Check [Infection Monkey documentation](https://techdocs.akamai.com/infection-monkey/docs/welcome-infection-monkey) on how to recieve usage and support**.

        Compute Engine -\> Compute image user

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

#### Linux

Upload the [`AppImage deployment`](https://github.com/guardicore/monkey/releases/latest)
option and run it in [`island-linux-250`](zoo_network.md#_Toc536021489).

#### Windows

Upload the [`MSI deployment`](https://github.com/guardicore/monkey/releases/latest)
option, install it and run it in [`island-windows-251`](zoo_network.md#_Toc536021490).
After that use the Monkey as you would on local network.


### For developers

#### Linux:

Get into `island-linux-250` using SSH from GCP.

To run monkey island from source:<br>
`sudo /usr/run\_island.sh`<br>

To run monkey from source:<br>
`sudo /usr/run\_monkey.sh`<br>

To update repository:<br>
`git pull /usr/infection_monkey`<br>

Update all requirements using deployment script:<br>
1\. `cd /usr/infection_monkey/deployment_scripts`<br>
2\. `./deploy_linux.sh "/usr/infection_monkey" "develop"`<br>

#### Windows:

RDP into `island-windows-251`.

To run monkey island from source:<br>
Execute C:\\run\_monkey\_island.bat as administrator

To run monkey from source:<br>
Execute C:\\run\_monkey.bat as administrator

To update repository:<br>
1\. Open cmd as an administrator<br>
2\. `cd C:\infection_monkey`<br>
3\. `git pull` (updates develop branch)<br>

Update all requirements using deployment script:<br>
1\. `cd C:\infection_monkey\deployment_scripts`<br>
2\. `./run_script.bat "C:\infection_monkey" "develop"`<br>

## Running blackbox tests in MonkeyZoo

To run blackbox tests in the MonkeyZoo network refer to [blackbox tests documentation](../blackbox/README.md).
