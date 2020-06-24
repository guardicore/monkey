---
title: "Zero Trust report"
date: 2020-06-24T21:16:18+03:00
draft: false
---

The Guardicore Infection Monkey runs different tests to evaluate your network adherence to key components of the Zero Trust framework as established by Forrester, such as whether you have applied segmentation, user identity, encryption and more. Then, the Monkey generates a status report with detailed explanations of security gaps and prescriptive instructions on how to rectify them.

## Summary

This diagram provides a quick glance at how your organization scores on each component of the Forrester’s Zero Trust model with **Failed**, **Verify**, **Passed** and **Unexecuted** verdicts.

- **Failed**: At least one of the tests related to this component failed. This means that the Infection Monkey detected an unmet Zero Trust requirement.
- **Verify**: At least one of the tests’ results related to this component requires further manual verification.
- **Passed**: All Tests related to this pillar passed. No violation of a Zero Trust guiding principle was detected.
- **Unexecuted**: This status means no tests were executed for this pillar.
