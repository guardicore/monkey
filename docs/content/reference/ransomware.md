---
title: "Ransomware"
date: 2021-06-23T18:13:59+05:30
draft: true
pre: '<i class="fas fa-lock"></i> '
weight: 10
---

The Infection Monkey has the capability of simulating a ransomware attack on your network through a series of activities.

#### Encrypting user-specified files
All actions performed by the encryption routine are designed to be safe for production
environments.

To ensure minimum interference and easy recoverability, the ransomware simulation will encrypt
files only if the user specifies a directory that contains files that are safe to encrypt.
If no directory is specified, no files will be encrypted.

#### Leaving a README.txt file
Many ransomware packages leave a README.txt file on the victim machine with an explanation of what has occurred and instructions for paying the attacker. Infection Monkey can also leave a README.txt file on the victim machine in order to replicate this behavior. This can be enabled or disabled by checking the box in the configuration screen. Note that if no target directory is specified, Infection Monkey will not leave a README.txt file.

<!-- add screenshot highlighting readme option -->

The README.txt file informs the user that a ransomware simulation has taken place and that they should contact their administrator. The contents of the file can be found [here](https://github.com/guardicore/monkey/tree/develop/monkey/infection_monkey/ransomware/ransomware_readme.txt).


<!-- add config screenshot here -->


## How are the files encrypted?

Files are "encrypted" in place with a simple bit flip. Encrypted files are renamed to have
`.m0nk3y` appended to their names.

This is a safe way to simulate encryption since it is easy to "decrypt" your files. You can simply perform a bit flip on the files again and rename them to remove the appended `.m0nk3y` extension.

This is sufficient to mock a ransomware attack on your network as the data in your files has been manipulated (temporarily leaving them unusuable) and are renamed with a different extension, similar to the way that many ransomwares act. As this is a simulation, your security solutions should be triggered to notify and prevent these changes from taking place.


## Which files are encrypted?

All regular files with [valid extensions](#file-extensions-targeted-for-encryption) in the configured directory are attempted to be encrypted during the simulation.

The simulation is not recursive, i.e. it will not touch any files in sub-directories of the configured directory. Symlinks and shortcuts are ignored.

These precautions are taken to prevent the monkey from going rogue and accidentally encrypting files that you didn't intend to encrypt.


## File extensions targeted for encryption

Encryption attempts are only performed on regular files with the following extensions.

This list is based on the [analysis of the Goldeneye ransomware by BitDefender](https://labs.bitdefender.com/2017/07/a-technical-look-into-the-goldeneye-ransomware-attack/).

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
