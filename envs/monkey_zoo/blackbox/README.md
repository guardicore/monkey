# Automatic blackbox tests
### Prerequisites
1. Download google sdk: https://cloud.google.com/sdk/docs/
2. Have a MonkeyZoo project set up. For setup instructions refer to [MonkeyZoo setup](../docs/zoo_setup.md).
3. Download service account key for MonkeyZoo project (if you deployed MonkeyZoo via terraform scripts then you already have it).
GCP console -> IAM -> service accounts(you can use the same key used to authenticate terraform scripts).
Place the key in `envs/monkey_zoo/gcp_keys/gcp_key.json`.
3. Deploy the relevant branch + complied executables to the Island machine on GCP.

### Running the tests
In order to execute the entire test suite, you must know the external IP of the Island machine on GCP. You can find
this information in the GCP Console `Compute Engine/VM Instances` under _External IP_.

#### Running in command line
Either run pytest from `/monkey` directory or set `PYTHONPATH` environment variable to
`/monkey` directory so that blackbox tests can import other monkey code.
Blackbox tests have following parameters:
- `--island=IP` Sets island's IP
- `--no-gcp` (Optional) Use for no interaction with the cloud (local test).

Example run command:

`monkey\monkey>python -m pytest -s --island=35.207.152.72:5000 ..\envs\monkey_zoo\blackbox\test_blackbox.py`

#### Running in PyCharm
Configure a PyTest configuration with the additional arguments `-s --island=35.207.152.72:5000`, and to run from
directory `monkey\envs\monkey_zoo\blackbox`.
