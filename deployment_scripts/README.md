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

You must have root permissions, but don't run the script as root.<br>
Launch deploy_linux.sh from scripts directory.<br>
First argument should be an empty directory (script can create one) and second is branch you want to clone (develop by default).
Choose a directory where you have all the relevant permissions, for e.g. /home/your_username
Example usages:<br>
./deploy_linux.sh (deploys under ./infection_monkey)<br>
./deploy_linux.sh "/home/test/monkey" (deploys under /home/test/monkey)<br>
./deploy_linux.sh "" "master" (deploys master branch in script directory)<br>
./deploy_linux.sh "/home/user/new" "master" (if directory "new" is not found creates it and clones master branch into it)<br>
