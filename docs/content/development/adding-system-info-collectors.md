---
title: "Adding System Info Collectors"
date: 2020-06-09T11:03:42+03:00
draft: false
tags: ["contribute"]
weight: 80
---

## What does this guide cover?

This guide will show you how to create a new _System Info Collector_ for the Infection Monkey. System Info Collectors are modules that each of the Infection Monkey agents runs that collect specific information and send it back to the Monkey Island as part of the System Info Telemetry.

### Do I need a new System Info Collector?

If all you want to do is execute a shell command, then there's no need to add a new System Info Collector - just configure the required commands in the Monkey Island's post-breach action (PBA) section! Also, if there is a relevant System Info Collector and you only need to add more information to it, simply expand the existing one. Otherwise, you must add a new System Info Collector.

## How to add a new System Info Collector

### Modify the Infection Monkey Agent

#### Framework

1. Create your new System Info Collector in the following directory: `monkey/infection_monkey/system_info/collectors` by first creating a new file with the name of your System Info Collector.
2. In that file, create a class that inherits from the `SystemInfoCollector` class:

```py
from infection_monkey.system_info.system_info_collector import SystemInfoCollector

class MyNewCollector(SystemInfoCollector):
```

3. Set the System Info Collector name in the constructor, like so:

```py
class MyNewCollector(SystemInfoCollector):
    def __init__(self):
        super(MyNewCollector, self).__init__(name="MyNewCollector")
```

#### Implementation

Override the `collect` method with your own implementation. See the `EnvironmentCollector.py` System Info Collector for reference. You can log during collection as well.

### Modify the Monkey Island

#### Configuration

##### Definitions

You'll need to add your Sytem Info Collector to the `monkey_island/cc/services/config_schema.py` file, under `definitions/system_info_collectors_classes/anyOf`, like so:

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

##### Properties

Also, you can add the System Info Collector to be used by default by adding it to the `default` key under `properties/monkey/system_info/system_info_collectors_classes`:

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

1. Add a process function under `monkey_island/cc/telemetry/processing/system_info_collectors/{DATA_NAME_HERE}.py`. The function should parse the System Info Collector's result. See `processing/system_info_collectors/environment.py` for example.

2. Add that function to `SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSORS` under `monkey_island/cc/services/telemetry/processing/system_info_collectors/system_info_telemetry_dispatcher.py`.
