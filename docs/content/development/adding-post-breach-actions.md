---
title: "Adding Post Breach Actions"
date: 2020-06-08T19:53:13+03:00
draft: false
tags: ["contribute"]
weight: 90
---

## What does this guide cover?

This guide will show you how to create a new _post-breach action_ (PBA) for the Infection Monkey. PBA are "extra" actions that the Infection Monkey can perform on victim machines after propagating to them.

## Do I need a new PBA?

If all you want to do is execute shell commands, then there's no need to add a new PBA - just configure the required commands in the Monkey Island configuration! If you think that those specific commands have reuse value in other deployments besides your own, you can add a new PBA. Additionally, if you need to run actual Python code, you must add a new PBA.

## How to add a new PBA

### Modify the Infection Monkey Agent

#### Framework

1. Create your new action in the following directory: `monkey/infection_monkey/post_breach/actions` by first creating a new file with the name of your action.
2. In that file, create a class that inherits from the `PBA` class:

```python
from infection_monkey.post_breach.pba import PBA

class MyNewPba(PBA):
```

3. Set the action name in the constructor, like so:

```python
class MyNewPba(PBA):
    def __init__(self):
        super(MyNewPba, self).__init__(name="MyNewPba")
```

#### Implementation

If your PBA consists only of simple shell commands, you can reuse the generic PBA by passing the commands into the constructor. See the `account_discovery.py` PBA for reference.

Otherwise, you'll need to override the `run` method with your own implementation. See the `communicate_as_backdoor_user.py` PBA for reference. Make sure to send the relevant PostBreachTelem upon success/failure. You can log during the PBA as well.

### Modify the Monkey Island

#### Configuration

You'll need to add your PBA to the `config_schema.py` file, under `post_breach_acts`, like so:

```json
"post_breach_acts": {
            "title": "Post breach actions",
            "type": "string",
            "anyOf": [
                # ...
                {
                    "type": "string",
                    "enum": [
                        "MyNewPba"
                    ],
                    "title": "My new PBA",
                },
            ],
        },
```

Now you can choose your PBA when configuring the Infection Monkey on the Monkey island:

![PBA in configuration](https://i.imgur.com/9PrcWr0.png)

#### Telemetry processing

If you wish to process your PBA telemetry (for example, to analyze it for report data), add a processing function to the `POST_BREACH_TELEMETRY_PROCESSING_FUNCS`, which can be found at `monkey/monkey_island/cc/services/telemetry/processing/post_breach.py`. You can reference the `process_communicate_as_backdoor_user_telemetry` method as an example.
