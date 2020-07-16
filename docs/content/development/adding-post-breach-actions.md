---
title: "Adding Post Breach Actions"
date: 2020-06-08T19:53:13+03:00
draft: false
tags: ["contribute"]
weight: 90
---

## What's this?

This guide will show you how to create a new _Post Breach action_ for the Infection Monkey. _Post Breach actions_ are "extra" actions that the Monkey can perform on the victim machines after it propagated to them.

## Do I need a new PBA?

If all you want is to execute shell commands, then there's no need to add a new PBA - just configure the required commands in the Monkey Island configuration! If you think that those specific commands have reuse value in all deployments and not just your own, you can add a new PBA. If you need to run actual Python code, you must add a new PBA.

## How to add a new PBA

### Monkey side

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

If your PBA consists only of simple shell commands, you can reuse the generic PBA by passing the commands into the constructor. See the `add_user.py` PBA for reference.

Otherwise, you'll need to override the `run` method with your own implementation. See the `communicate_as_new_user.py` PBA for reference. Make sure to send the relevant PostBreachTelem upon success/failure. You can log during the PBA as well.

### Island side

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
                    "attack_techniques": []
                },
            ],
        },
```

Now you can choose your PBA when configuring the Monkey on the Monkey island:

![PBA in configuration](https://i.imgur.com/9PrcWr0.png)

#### Telemetry processing

If you wish to process your Post Breach action telemetry (for example, to analyze it for report data), add a processing function to the `POST_BREACH_TELEMETRY_PROCESSING_FUNCS` which can be found at `monkey/monkey_island/cc/services/telemetry/processing/post_breach.py`. You can look at the `process_communicate_as_new_user_telemetry` method as an example.
