# Automatic blackbox tests
### Prerequisites
1. Download google sdk: https://cloud.google.com/sdk/docs/
2. Download service account key for MonkeyZoo project (if you deployed MonkeyZoo via terraform scripts then you already have it). 
GCP console -> IAM -> service accounts(you can use the same key used to authenticate terraform scripts)
3. Deploy the relevant branch + complied executables to the Island machine on GCP.   

### Running the tests
In order to execute the entire test suite, you must know the external IP of the Island machine on GCP. You can find 
this information in the GCP Console `Compute Engine/VM Instances` under _External IP_. 

#### Running in command line
Run the following command:

`monkey\envs\monkey_zoo\blackbox>python -m pytest --island=35.207.152.72:5000 test_blackbox.py`

#### Running in PyCharm
Configure a PyTest configuration with the additional argument `--island=35.207.152.72` on the 
`monkey\envs\monkey_zoo\blackbox`.
