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
    2.  Have an S3-compatible bucket for storing terraform state
    3.  Have access keys for accessing the S3-compatible bucket

- For using the Google Cloud Platform (GCP):
    1.  Have a Google Cloud Platform account (upgraded if you want to test
        whole network at once).
    2.  Have `gcloud` CLI installed.
        [[Installation instructions](https://cloud.google.com/sdk/docs/install#linux)]


To deploy:
1.  Configure service account for your project:

    a. Create a service account (GCP website -> IAM & Admin -> Service Accounts -> + CREATE SERVICE ACCOUNT) to manage deployment to your project

    b. Give these permissions to your service account:

        Compute Engine -> Compute Image User
        Compute Engine -> Compute Network Admin
        Compute Engine -> Compute Instance Admin (v1)
        Compute Engine -> Compute Security Admin

    or just give

        Project -> Owner
        Note: Adds more permissions then are needed

    c. Create and download its `Service account key` in JSON and place it in `monkey_zoo/gcp_keys` as `gcp_key.json`.

    d. (Optional) If managing multiple zoo instances, you may find it helpful to have a service account to manage each project, and another service account that is able to impersonate those accounts, allowing you to use only one key to manage all projects. In order to do this, simply:
        - Enable the the IAM and Service Account Credentials APIs on the project(s)
        - Give an account Service Account Token Creator access to each of the project service accounts, and use that account's keys
        - Set the service_account_email variable to the service account of the project you'd like to manage

2.  Get these permissions in our monkeyZoo production project (guardicore-22050661) for your service account.<br>
    **Note: Ask monkey developers to add them. Check [Infection Monkey documentation](https://techdocs.akamai.com/infection-monkey/docs/welcome-infection-monkey) on how to receive usage and support**.

        Compute Engine -> Compute image user

3.  Configure AWS access
    First, generate the access key.

    Next, configure your environment to use the generated key. This can be done in one of two ways:
    a. (Optional) Use the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
        - Set the `AWS_ACCESS_KEY_ID` environment variable to the ID
        - Set the `AWS_SECRET_ACCESS_KEY` to the secret
    b. (Optional) Use the `~/.aws/config` and `~/.aws/credentials` config files
        - Edit or create the `~/.aws/config` file with a profile:
          ```
          [profile my-profile]
          output = text
          region = us-east-1
          ```
        - Edit or create the `~/.aws/credentials` file to specify the access key for the profile:
          ```
          [my-profile]
          aws_access_key_id=<access-key>
          aws_secret_access_key=<secret-key>
          ```

4.  Configure the Terraform backend

    Modify `envs/monkey_zoo/terraform/state.tf` `backed "s3"` section:

    endpoint: Endpoint for the S3 API
    profile: The profile from the `~/.aws/config` file, if using it
    bucket: The name of the S3-compatible bucket
    key: The path of the file in which to store the state in the S3-compatible bucket
    region: The region where the bucket is stored

    More details are provided in the [s3 backend documentation](https://developer.hashicorp.com/terraform/language/settings/backends/s3)

5.  (Optional) Generate images

    To build the images, run the script located at `envs/monkey_zoo/build_images.sh`, providing it:
        - The target project in which the images will be stored
        - The account file, e.g. `gcp_key.json`
        - The packer files to build

    For example,

        `build_images.sh -p guardicore-22050661 --account-file gcp_keys/gcp_key.json` packer/tunneling.pkr.hcl

6.  Change configurations located in the
    ../monkey/envs/monkey\_zoo/terraform/config.tf file (don’t forget to
    link to your service account key file):

    Provide values for the following variables:

    - project
    - credentials_file

    Optionally, provide values for the following variables:
    - region
    - main_zone
    - main1_zone
    - tunneling_zone
    - credentials_reuse_zone

7.  Deploy the zoo

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
