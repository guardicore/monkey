Usage
=======

Once configured, run the monkey using ```./monkey-linux-64 m0nk3y -c config.bin -s 41.50.73.31:5000``` (Windows is identical). This can be done at multiple points in the network simultaneously. 

Command line options include:
* `-c`, `--config`: set configuration file. JSON file with configuration values, will override compiled configuration.
* `-p`, `--parent`: set monkey’s parent uuid, allows better recognition of exploited monkeys in c&c
* `-t`, `--tunnel`: ip:port, set default tunnel for Monkey when connecting to c&c.
* `-d`, `--depth` : sets the Monkey's current operation depth.
