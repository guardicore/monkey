---
title: "Adding Zero Trust Tests"
date: 2020-07-14T10:19:08+03:00
draft: false
weight: 100
---

## How do I add a new Zero Trust test to the Monkey?

Assuming the Infection Monkey agent is already sending the relevant telemetry, you'll need to add the test in two places.

### `zero_trust_consts.py`

In the file `/monkey/common/data/zero_trust_consts.py`:

1. Add the test name to the TESTS set
2. Add a relevant recommendation if it exists
3. Add the test to the TESTS_MAP dict. Ensure that all statuses (except `STATUS_UNEXECUTED`) have finding explanations.

### `telemetry/processing.py`

Find the relevant telemetry type you wish to test the finding in next. These can be found in `/monkey/monkey_island/cc/services/telemetry/processing.py`. In the relevant `process_*_telemetry` function, add your Zero Trust testing code. Please put the Zero Trust tests under the `/monkey/monkey_island/cc/services/telemetry/zero_trust_tests` directory. There you can also find examples of existing tests as well, so you'll have a reference for what you need to write.

## How do I test the new Zero Trust test I've implemented?

Test ALL possible finding statuses you've defined in a fake network. Ensure the events were formatted correctly by observing them. If there's an algorithmic part to your Zero Trust test, please cover it using a Unit Test.
