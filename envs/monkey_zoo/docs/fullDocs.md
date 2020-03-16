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
[Nr. 4 Elastic](#_Toc526517184)<br>
[Nr. 5 Elastic](#_Toc526517185)<br>
[Nr. 6 Sambacry](#_Toc536021459)<br>
[Nr. 7 Sambacry](#_Toc536021460)<br>
[Nr. 8 Shellshock](#_Toc536021461)<br>
[Nr. 9 Tunneling M1](#_Toc536021462)<br>
[Nr. 10 Tunneling M2](#_Toc536021463)<br>
[Nr. 11 SSH key steal](#_Toc526517190)<br>
[Nr. 12 SSH key steal](#_Toc526517191)<br>
[Nr. 13 RDP grinder](#_Toc526517192)<br>
[Nr. 14 Mimikatz](#_Toc536021467)<br>
[Nr. 15 Mimikatz](#_Toc536021468)<br>
[Nr. 16 MsSQL](#_Toc536021469)<br>
[Nr. 17 Upgrader](#_Toc536021470)<br>
[Nr. 18 WebLogic](#_Toc526517180)<br>
[Nr. 19 WebLogic](#_Toc526517181)<br>
[Nr. 20 SMB](#_Toc536021473)<br>
[Nr. 21 Scan](#_Toc526517196)<br>
[Nr. 22 Scan](#_Toc526517197)<br>
[Nr. 23 Struts2](#_Toc536021476)<br>
[Nr. 24 Struts2](#_Toc536021477)<br>
[Nr. 250 MonkeyIsland](#_Toc536021478)<br>
[Nr. 251 MonkeyIsland](#_Toc536021479)<br>
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

    a. Create a service account (GCP website -> IAM -> service accounts) and name it “your\_name-monkeyZoo-user” 
    
    b. Give these permissions to your service account:
    
    **Compute Engine -> Compute Network Admin**
    and
    **Compute Engine -> Compute Instance Admin**
    and
    **Compute Engine -> Compute Security Admin**
    and
    **Service Account User**
    
    or
    
    **Project -> Owner**
    
    c. Download its **Service account key** in JSON and place it in **/gcp_keys** as **gcp_key.json**.
2.  Get these permissions in monkeyZoo project for your service account (ask monkey developers to add them):

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

###How to get into the islands:

**island-linux-250:** SSH from GCP

**island-windows-251:** In GCP/VM instances page click on
island-windows-251. Set password for your account and then RDP into
the island.

###These are most common steps on monkey islands:

####island-linux-250:

To run monkey island:<br>
`sudo /usr/run\_island.sh`<br>

To run monkey:<br>
`sudo /usr/run\_monkey.sh`<br>

To update repository:<br>
`git pull /usr/infection_monkey`<br>

Update all requirements using deployment script:<br>
1\. `cd /usr/infection_monkey/deployment_scripts`<br>
2\. `./deploy_linux.sh "/usr/infection_monkey" "develop"`<br>

####island-windows-251:

To run monkey island:<br>
Execute C:\\run\_monkey\_island.bat as administrator

To run monkey:<br>
Execute C:\\run\_monkey.bat as administrator

To update repository:<br>
1\. Open cmd as an administrator<br>
2\. `cd C:\infection_monkey`<br>
3\. `git pull` (updates develop branch)<br>

Update all requirements using deployment script:<br>
1. `cd C:\infection_monkey\deployment_scripts`<br>
2. `./run_script.bat "C:\infection_monkey" "develop"`

# Running tests:

Once you start monkey island you can import test configurations from
../monkey/envs/configs.

fullTest.conf is a good config to start, because it covers all machines.

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
<th><p><span id="_Toc526517184" class="anchor"></span>Nr. <strong>4</strong> Elastic</p>
<p>(10.2.2.4)</p></th>
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
<p><a href="https://www.elastic.co/downloads/past-releases/elasticsearch-1-4-2">Elastic 1.4.2</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>9200</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="odd">
<td>Scan results:</td>
<td>Machine exploited using Elastic exploiter</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td><a href="https://www.elastic.co/guide/en/elasticsearch/reference/1.4/_index_and_query_a_document.html">Quick</a> tutorial on how to add entries (was useful when setting up).</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517185" class="anchor"></span>Nr. <strong>5</strong> Elastic</p>
<p>(10.2.2.5)</p></th>
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
<p><a href="https://www.elastic.co/downloads/past-releases/elasticsearch-1-4-2">Elastic 1.4.2</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>9200</td>
</tr>
<tr class="even">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="odd">
<td>Scan results:</td>
<td>Machine exploited using Elastic exploiter</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td><a href="https://www.elastic.co/guide/en/elasticsearch/reference/1.4/_index_and_query_a_document.html">Quick</a> tutorial on how to add entries (was useful when setting up).</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021459" class="anchor"></span>Nr. <strong>6</strong> Sambacry</p>
<p>(10.2.2.6)</p></th>
<th>(Not implemented)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Samba &gt; 3.5.0 and &lt; 4.6.4, 4.5.10 and 4.4.14</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>-</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>;^TK`9XN_x^</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td></td>
</tr>
<tr class="even">
<td>Scan results:</td>
<td>Machine exploited using Sambacry exploiter</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td></td>
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
<th><p><span id="_Toc536021460" class="anchor"></span>Nr. <strong>7</strong> Sambacry</p>
<p>(10.2.2.7)</p></th>
<th>(Not implemented)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 16.04.05 x32</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Samba &gt; 3.5.0 and &lt; 4.6.4, 4.5.10 and 4.4.14</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>-</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>*.&amp;A7/W}Rc$</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td></td>
</tr>
<tr class="even">
<td>Scan results:</td>
<td>Machine exploited using Sambacry exploiter</td>
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
<th><p><span id="_Toc536021461" class="anchor"></span>Nr. <strong>8</strong> Shellshock</p>
<p>(10.2.2.8)</p></th>
<th>(Vulnerable)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>OS:</td>
<td><strong>Ubuntu 12.04 LTS x64</strong></td>
</tr>
<tr class="even">
<td>Software:</td>
<td>Apache2, bash 4.2.</td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>80</td>
</tr>
<tr class="even">
<td>Scan results:</td>
<td>Machine exploited using Shellshock exploiter</td>
</tr>
<tr class="odd">
<td>Notes:</td>
<td>Vulnerable app is under /cgi-bin/test.cgi</td>
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
<td>3Q=(Ge(+&amp;w]*</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td>Default</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only trough Nr.9</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021463" class="anchor"></span>Nr. <strong>11</strong> Tunneling M3</p>
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
<td>Default</td>
</tr>
<tr class="even">
<td>Notes:</td>
<td>Accessible only trough Nr.10</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021463" class="anchor"></span>Nr. <strong>12</strong> Tunneling M4</p>
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
<td>Accessible only trough Nr.10</td>
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
<tr class="odd">
<td></td>
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
<tr class="odd">
<td></td>
<td></td>
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
<tr class="odd">
<td></td>
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
<tr class="even">
<td></td>
<td></td>
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
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc526517180" class="anchor"></span>Nr. <strong>18</strong> WebLogic</p>
<p>(10.2.2.18)</p></th>
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
<p><a href="https://www.oracle.com/technetwork/middleware/weblogic/downloads/wls-main-097127.html">Oracle WebLogic server 12.2.1.2</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>7001</td>
</tr>
<tr class="even">
<td>Admin domain credentials:</td>
<td>weblogic : B74Ot0c4</td>
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
<th><p><span id="_Toc526517181" class="anchor"></span>Nr. <strong>19</strong> WebLogic</p>
<p>(10.2.2.19)</p></th>
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
<p><a href="https://www.oracle.com/technetwork/middleware/weblogic/downloads/wls-main-097127.html">Oracle WebLogic server 12.2.1.2</a></p></td>
</tr>
<tr class="odd">
<td>Default server’s port:</td>
<td>7001</td>
</tr>
<tr class="even">
<td>Admin servers credentials:</td>
<td>weblogic : =ThS2d=m(`B</td>
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
<th><p><span id="_Toc536021473" class="anchor"></span>Nr. <strong>20</strong> SMB</p>
<p>(10.2.2.20)</p></th>
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
<td>Default service’s port:</td>
<td>445</td>
</tr>
<tr class="even">
<td>Root password:</td>
<td>YbS,&lt;tpS.2av</td>
</tr>
<tr class="odd">
<td>Server’s config:</td>
<td><a href="https://social.technet.microsoft.com/Forums/windows/en-US/8160d62b-0f5d-48a3-9fe9-5cd319837917/how-te-reenable-smb1-in-windows1o?forum=win10itprogeneral">SMB</a> turned on</td>
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
<tr class="even">
<td></td>
<td></td>
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
<th><p><span id="_Toc536021476" class="anchor"></span>Nr. <strong>23</strong> Struts2</p>
<p>(10.2.2.23)</p></th>
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
<p>struts2 2.3.15.1,</p>
<p>tomcat 9.0.0.M9</p></td>
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
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021477" class="anchor"></span>Nr. <strong>24</strong> Struts2</p>
<p>(10.2.2.24)</p></th>
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
<p>struts2 2.3.15.1,</p>
<p>tomcat 9.0.0.M9</p></td>
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
<td></td>
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
<th><p><span id="_Toc536021478" class="anchor"></span>Nr. <strong>250 MonkeyIsland</strong></p>
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
<td>Only accessible trough GCP</td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</table>

<table>
<thead>
<tr class="header">
<th><p><span id="_Toc536021478" class="anchor"></span>Nr. <strong>251 MonkeyIsland</strong></p>
<p>(10.2.2.251)</p></th>
<th></th>
</tr>
</thead>
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
<td>Only accessible trough GCP</td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>

# Network topography:

<img src="/envs/monkey_zoo/docs/images/networkTopography.jpeg" >
