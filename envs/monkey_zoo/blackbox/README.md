# Automatic blackbox tests
### Prerequisites
1. Download google sdk: https://cloud.google.com/sdk/docs/
2. Download service account key for MonkeyZoo project (if you deployed MonkeyZoo via terraform scripts then you already have it).
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
- `--quick-performance-tests` (Optional) If enabled performance tests won't reset island and won't send telemetries,
instead will just test performance of endpoints in already present island state.

Example run command:

`monkey\monkey>python -m pytest -s --island=35.207.152.72:5000 ..\envs\monkey_zoo\blackbox\test_blackbox.py`

#### Running in PyCharm
Configure a PyTest configuration with the additional arguments `-s --island=35.207.152.72:5000`, and to run from
directory `monkey\envs\monkey_zoo\blackbox`.

### Running telemetry performance test

**Before running performance test make sure browser is not sending requests to island!**

To run telemetry performance test follow these steps:
0. Set no password protection on the island.
Make sure the island parameter is an IP address(not localhost) as the name resolution will increase the time for requests.
1. Gather monkey telemetries.
    1. Enable "Export monkey telemetries" in Configuration -> Internal -> Tests if you don't have
    exported telemetries already.
    2. Run monkey and wait until infection is done.
    3. All telemetries are gathered in `monkey/telem_sample`. If not, restart the island process.
2. Run telemetry performance test.
    1. Move directory `monkey/telem_sample` to `envs/monkey_zoo/blackbox/tests/performance/telemetry_sample`
    2. (Optional) Use `envs/monkey_zoo/blackbox/tests/performance/telem_sample_parsing/sample_multiplier/sample_multiplier.py` to multiply
    telemetries gathered.
        1. Run `sample_multiplier.py` script with working directory set to `monkey\envs\monkey_zoo\blackbox`
        2. Pass integer to indicate the multiplier. For example running `telem_parser.py 4` will replicate
        telemetries 4 times.
        3. If you're using pycharm check "Emulate terminal in output console" on debug/run configuration.
    3. Add a `--run-performance-tests` flag to blackbox scripts to run performance tests as part of BlackBox tests.
    You can run a single test separately by adding `-k 'test_telem_performance'` option.
