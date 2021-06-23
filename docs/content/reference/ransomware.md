---
title: "Ransomware"
date: 2021-06-23T18:13:59+05:30
draft: true
pre: '<i class="fas fa-lock"></i> '
weight: 10
---

The Infection Monkey has the capability of simulating a ransomware attack on your network.
All actions performed by the encryption routine are safe for production environments.

To ensure minimum intereference and easy recoverability, the ransomware simulation will only run if
it is configured properly. To do so, you must specify the path to a directory in the configuration.
If no directory is specified, the simulation will not run.

<!-- add config screenshot here -->

## Which files are encrypted?

All regular files with [relevant extensions](#relevant-file-extensions-for-encryption) in the
configured directory are attempted to be encrypted during the simulation.

The simulation is not recursive, i.e. it will not touch any files in sub-directories of the
configured directory — only appropriate files in the top level of the tree.

Symlinks and shortcuts are ignored.


## How are the files encrypted?

Files are "encrypted" in place with a simple bit flip. Encrypted files are renamed to have
`.m0nk3y` appended to their names.

To "decrypt" your files, you can simply perform a bit flip on them again.


## Relevant file extensions for encryption

Encryption attempts are only performed on regular files with the following extensions.

This list is based on the [analysis of the ??? ransomware by ???]().

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
