---
title: " Ransomware Simulation"
date: 2021-06-23T18:13:59+05:30
draft: false
description: "Simulate a ransomware attack on your network and assess the potential damage."
weight: 6
pre: "<i class='fa fa-lock'></i> "
---

The Infection Monkey is capable of simulating a ransomware attack on your
network using a set of configurable behaviors.


## Encryption

In order to simulate the behavior of ransomware as accurately as possible,
the Infection Monkey can [encrypt user-specified files](#configuring-encryption)
using a [fully reversible algorithm](#how-are-the-files-encrypted). A number of
mechanisms are in place to ensure that all actions performed by the encryption
routine are safe for production environments.

### Preparing your environment for a ransomware simulation

The Infection Monkey will only encrypt files that you allow it to. In
order to take full advantage of the Infection Monkey's ransomware simulation, you'll
need to provide the Infection Monkey with a directory that contains files that
are safe for it to encrypt. The recommended approach is to use a remote
administration tool, such as
[Ansible](https://docs.ansible.com/ansible/latest/user_guide/) or
[PsExec](https://theitbros.com/using-psexec-to-run-commands-remotely/) to add a
"ransomware target" directory to each machine in your environment. The Infection
Monkey can then be configured to encrypt files in this directory.

### Configuring encryption

To ensure minimum interference and easy recoverability, the ransomware
simulation will only encrypt files contained in a user-specified directory. If
no directory is specified, no files will be encrypted.

Infection Monkey appends the `.m0nk3y` file extension to files that it
encrypts. You may optionally provide a custom file extension for Infection
Monkey to use instead. You can even provide no file extension, but take
caution: you'll no longer be able to tell if the file has been encrypted based
on the filename alone!

![Ransomware
configuration](/images/island/configuration_page/ransomware_configuration.png
"Ransomware configuration")

### How are the files encrypted?

Files are "encrypted" in place with a simple bit flip. Encrypted files are
renamed to have a file extension (`.m0nk3y` by default) appended to their
names. This is a safe way to simulate encryption since it is easy to "decrypt"
your files. You can simply perform a bit flip on the files again and rename
them to remove the appended `.m0nk3y` extension.

Flipping a file's bits is sufficient to simulate the encryption behavior of
ransomware, as the data in your files has been manipulated (leaving them
temporarily unusable). Files are then renamed with a new extension appended,
which is similar to the way that many ransomwares behave. As this is a
simulation, your
security solutions should be triggered to notify you or prevent these changes
from taking place.

### Which files are encrypted?

During the ransomware simulation, attempts will be made to encrypt all regular
files with [targeted file extensions](#files-targeted-for-encryption) in the
configured directory. The simulation is not recursive, i.e. it will not touch
any files in sub-directories of the configured directory. The Infection Monkey will
not follow any symlinks or shortcuts.

These precautions are taken to prevent the Infection Monkey from accidentally
encrypting files that you didn't intend to encrypt.

### Files targeted for encryption

Only regular files with certain extensions are encrypted by the ransomware
simulation. This list is based on the [analysis of the Goldeneye ransomware by
BitDefender](https://labs.bitdefender.com/2017/07/a-technical-look-into-the-goldeneye-ransomware-attack/).

- .3ds
- .7z
- .accdb
- .ai
- .asp
- .aspx
- .avhd
- .avi
- .back
- .bak
- .c
- .cfg
- .conf
- .cpp
- .cs
- .ctl
- .dbf
- .disk
- .djvu
- .doc
- .docx
- .dwg
- .eml
- .fdb
- .giff
- .gz
- .h
- .hdd
- .jpg
- .jpeg
- .kdbx
- .mail
- .mdb
- .mpg
- .mpeg
- .msg
- .nrg
- .ora
- .ost
- .ova
- .ovf
- .pdf
- .php
- .pmf
- .png
- .ppt
- .pptx
- .pst
- .pvi
- .py
- .pyc
- .rar
- .rtf
- .sln
- .sql
- .tar
- .tiff
- .txt
- .vbox
- .vbs
- .vcb
- .vdi
- .vfd
- .vmc
- .vmdk
- .vmsd
- .vmx
- .vsdx
- .vsv
- .work
- .xls
- .xlsx
- .xvd
- .zip


## Leaving a README.txt file

Many ransomware packages leave a README.txt file on the victim machine with an
explanation of what has occurred and instructions for paying the attacker.
The Infection Monkey will also leave a README.txt file in the target directory on
the victim machine in order to replicate this behavior.

The README.txt file informs the user that a ransomware simulation has taken
place and that they should contact their administrator. The contents of the
file can be found
[here](https://github.com/guardicore/monkey/tree/develop/monkey/infection_monkey/ransomware/ransomware_readme.txt).
