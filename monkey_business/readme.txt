How to install Monkey Business server:

---------------- On Linux ----------------:
1. Create the following directories:
    sudo mkdir /var/monkey_business
    sudo chmod 777 /var/monkey_business
    mkdir -p /var/monkey_business/bin/mongodb
    mkdir -p /var/monkey_business/db
    mkdir -p /var/monkey_business/cc

2. Install the following packages:
	sudo pip install flask
	sudo pip install Flask-Pymongo
	sudo pip install Flask-Restful
	sudo pip install python-dateutil
	sudo pip install pyVmomi
	sudo pip install celery
	sudo pip install -U celery[mongodb]

4. Download MongoDB and extract it to /var/monkey_business/bin/mongodb
    for debian64 - https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-3.0.7.tgz
    for ubuntu64 14.10 - https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1410-clang-3.0.7.tgz
    find more at - https://www.mongodb.org/downloads#production
	untar.gz with: tar -zxvf filename.tar.gz -C /var/monkey_business/bin/mongodb
	(make sure the content of the mongo folder is in this directory, meaning this path exists:
		/var/monkey_business/bin/mongodb/bin)

5. install OpenSSL
    sudo apt-get install openssl

6. Generate SSL Certificate, Run create_certificate.sh (located under /linux)

7. Copy monkey business server to /var/monkey_business:
    cp -r [monkey_island_source]/cc /var/monkey_business/


How to run:
1. run run.sh
   * This performs:
   		DB startup:
			/var/monkey_business/bin/mongodb/bin/mongod --dbpath db --fork --logpath db.log
		Jobs worker startup:
			nohup celery -A tasks_manager worker --loglevel=info
		Main Web Server startup:
			nohup python main.py