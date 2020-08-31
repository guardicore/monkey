---
title: "Adding System Info Collectors"
date: 2020-06-09T11:03:42+03:00
draft: false
tags: ["contribute"]
weight: 80
---

## What's this?

This guide will show you how to create a new _System Info Collector_ for the Infection Monkey. _System Info Collectors_ are modules which each Monkey runs, that collect specific information and sends it back to the Island as part of the System Info Telemetry.

### Do I need a new System Info Controller?

If all you want is to execute a shell command, then there's no need to add a new collector - just configure the required commands in the Monkey Island configuration in the PBA section! Also, if there is a relevant collector and you only need to add more information to it, expand the existing one. Otherwise, you must add a new Collector.

## How to add a new System Info Collector

### Monkey side

#### Framework

1. Create your new collector in the following directory: `monkey/infection_monkey/system_info/collectors` by first creating a new file with the name of your collector.
2. In that file, create a class that inherits from the `SystemInfoCollector` class:

```py
from infection_monkey.system_info.system_info_collector import SystemInfoCollector

class MyNewCollector(SystemInfoCollector):
```

3. Set the Collector name in the constructor, like so:

```py
class MyNewCollector(SystemInfoCollector):
    def __init__(self):
        super(MyNewCollector, self).__init__(name="MyNewCollector")
```

#### Implementation

Override the `collect` method with your own implementation. See the `EnvironmentCollector.py` Collector for reference. You can log during collection as well.

### Island side

#### Island Configuration

##### Definitions

You'll need to add your Collector to the `monkey_island/cc/services/config_schema.py` file, under `definitions/system_info_collectors_classes/anyOf`, like so:

```json
"system_info_collectors_classes": {
    "title": "System Information Collectors",
    "type": "string",
    "anyOf": [
        {
            "type": "string",
            "enum": [
                "EnvironmentCollector"
            ],
            "title": "Which Environment this machine is on (on prem/cloud)",
            "attack_techniques": []
        },
        {                               <=================================
            "type": "string",           <=================================
            "enum": [                   <=================================
                "MyNewCollector"        <=================================
            ],                          <=================================
            "title": "My new title",    <=================================
            "attack_techniques": []     <=================================
        },
    ],
},
```

##### properties

Also, you can add the Collector to be used by default by adding it to the `default` key under `properties/monkey/system_info/system_info_collectors_classes`:

```json
"system_info_collectors_classes": {
    "title": "System info collectors",
    "type": "array",
    "uniqueItems": True,
    "items": {
        "$ref": "#/definitions/system_info_collectors_classes"
    },
    "default": [
        "EnvironmentCollector",
        "MyNewCollector"    <=================================
    ],
    "description": "Determines which system information collectors will collect information."
},
```

#### Telemetry processing

1. Add a process function under `monkey_island/cc/telemetry/processing/system_info_collectors/{DATA_NAME_HERE}.py`. The function should parse the collector's result. See `processing/system_info_collectors/environment.py` for example.

2. Add that function to `SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSORS` under `monkey_island/cc/services/telemetry/processing/system_info_collectors/system_info_telemetry_dispatcher.py`.
