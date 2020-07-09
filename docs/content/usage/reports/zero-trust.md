---
title: "Zero Trust report"
date: 2020-06-24T21:16:18+03:00
draft: false
---

{{% notice info %}}
Check out [the documentation for the other reports as well](../).
{{% /notice %}}

The Guardicore Infection Monkey runs different tests to evaluate your network adherence to key components of the Zero Trust framework as established by Forrester, such as whether you have applied segmentation, user identity, encryption and more. Then, the Monkey generates a status report with detailed explanations of security gaps and prescriptive instructions on how to rectify them.

## Summary

This diagram provides a quick glance at how your organization scores on each component of the Forrester’s Zero Trust model with **Failed**, **Verify**, **Passed** and **Unexecuted** verdicts.

- {{< label danger Failed >}} At least one of the tests related to this component failed. This means that the Infection Monkey detected an unmet Zero Trust requirement.
- {{< label warning Verify >}} At least one of the tests’ results related to this component requires further manual verification.
- {{< label success Passed >}} All Tests related to this pillar passed. No violation of a Zero Trust guiding principle was detected.
- {{< label other Unexecuted >}} This status means no tests were executed for this pillar.

![Zero Trust Report summary](/images/usage/reports/ztreport1.png "Zero Trust Report summary")

## Test Results

See how your network fared against each of the tests the Infection Monkey ran. The tests are ordered by Zero Trust components so you can quickly navigate to the components you care about first.

![Zero Trust Report test results](/images/usage/reports/ztreport2.png "Zero Trust Report test results")

## Findings

Deep-dive into the details of each test, and see the explicit events and exact timestamps in which things happened in your network. This will enable you to match up with your SOC logs and alerts and to gain deeper insight as to what exactly happened during each of the tests.

![Zero Trust Report Findings](/images/usage/reports/ztreport3.png "Zero Trust Report Findings")

## Events

The results are exportable. Click Export after clicking on Events to view them in a machine-readable format.

![Zero Trust Report events](/images/usage/reports/ztreport4.png "Zero Trust Report events")

## Overview Video

You can check out an overview video here:

{{% youtube z4FNu3WCd9o %}}
