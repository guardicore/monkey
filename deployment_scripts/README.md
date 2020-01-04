# Files used to deploy development version of infection monkey
## Windows

Before running the script you must have git installed.<br>
Cd to scripts directory and use the scripts.<br>
First argument is an empty directory (script can create one) and second is branch you want to clone.
Example usages:<br>
./run_script.bat (Sets up monkey in current directory under .\infection_monkey)<br>
./run_script.bat "C:\test" (Sets up monkey in C:\test)<br>
powershell -ExecutionPolicy ByPass -Command ". .\deploy_windows.ps1; Deploy-Windows -monkey_home C:\test" (Same as above)<br>
./run_script.bat "" "master"(Sets up master branch instead of develop in current dir)
Don't forget to add python to PATH or do so while installing it via this script.<br>

## Linux

Linux deployment script is meant for Ubuntu 16.x machines.
You must have root permissions, but don't run the script as root.<br>
`wget https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/deploy_linux.sh`

Then execute the resulting script with your shell. 
First argument should be an absolute path of an empty directory (script will create one if doesn't exist, default is ./infection_monkey).
Second parameter is the branch you want to clone (develop by default).
Example usages:<br>
./deploy_linux.sh (deploys under ./infection_monkey)<br>
./deploy_linux.sh "/home/test/monkey" (deploys under /home/test/monkey)<br>
./deploy_linux.sh "" "master" (deploys master branch in script directory)<br>
./deploy_linux.sh "/home/user/new" "master" (if directory "new" is not found creates it and clones master branch into it)<br>
