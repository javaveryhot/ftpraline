# FTPraline
A Python FTP script for transferring files over HTTPS.
Generally used for Repl.it.
Useful for quickly transferring and copying files and directories to your server.

Include this in your Python project to support FTPraline and start managing files.

There is no third-party between the transferring.

## Setting up
### Set password
Make a `.env` file and add the key `ftpraline_password` with a value of a password.
The `.env` file should then look like this:
```
ftpraline_password=mypasswordhere
```
Where `mypasswordhere` is the password.
This password can later be used with the FTPraline client software.

## Operations
The FTPraline script allows anyone with the password to make file system operations.
These are the operations that anyone with the password can do:
* Read files and directories.
* Create files and directories.
* Edit files and directories (rename and change content).
* Delete files and directories.
