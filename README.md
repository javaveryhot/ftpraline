# FTPraline
A Python FTP script for transferring files over HTTPS.
Generally used for Repl.it.
Useful for quickly transferring and copying files and directories to your server.

Include this in your Python project to support FTPraline and start managing files.

There is no third-party between the transferring.

## Setting up
### Add requirements
Here's how to set up FTPraline in your project.

##### 1. Create an `__ftpraline` directory.
##### 2. Create an `init.py` file inside the `__ftpraline` directory.
##### 3. Paste the `ftpmanage.py` file content from this repository into the `init.py` file.
##### 4. --- For Repl.it only --- Create a `.replit` file if you are using Repl.it, and put `run = "python3 __ftpraline/init.py"`.
##### 4. --- Not Repl.it --- Import the `init.py` file inside your `main.py`. In this event, add `ftpraline_execute_main=no` to `.env`.
##### 5. Add the password, shown in the next step.

### Set password
Make a `.env` file and add the key `ftpraline_password` with a value of a password.
The `.env` file should then look like this:
```
ftpraline_password=mypasswordhere
```
Where `mypasswordhere` is the password.
This password can later be used with the FTPraline client software.
### Set command prefix
To change the console FTPraline prefix, add the key `ftpraline_prefix_override` with a value of the new prefix in the `.env` file.

## Operations
The FTPraline script allows anyone with the password to make file system operations.
These are the operations that anyone with the password can do:
* Read files and directories.
* Create files and directories.
* Edit files and directories (rename and change content).
* Delete files and directories.

## Use
### Commands
The default prefix is `/ftp`, so a `help` command would look like `/ftphelp`.
#### help
Shows information about FTPraline and the installation.
#### stop
Stop the FTPraline server.
**This will just stop the FTPraline server, your script will continue.**
#### restart
Restart the server.
**This will just restart the FTPraline server, your script will continue.**
#### github
Shows the GitHub repository.
