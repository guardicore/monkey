---
title: "Zero Trust report"
date: 2020-06-24T21:16:18+03:00
weight: 2
draft: false
description: "Generates a status report with detailed explanations of Zero Trust security gaps and prescriptive instructions on how to rectify them"
---

{{% notice info %}}
Check out [the documentation for other reports available in the Infection Monkey](../).
{{% /notice %}}

The Guardicore Infection Monkey runs different tests to evaluate your network's adherence to the Zero Trust framework's key components established by Forrester, such as whether you have applied segmentation, verified user identities, enabled encryption and more. Then, the Infection Monkey generates a status report with detailed explanations of security gaps and prescriptive instructions for rectifying them.

Watch the overview video here:

{{% youtube z4FNu3WCd9o %}}

## Summary

This diagram provides you with a quick glance at how your organization scores on each pillar of the Forrester Zero Trust model with **Failed**, **Verify**, **Passed** and **Unexecuted** verdicts.

- {{< label danger Failed >}} At least one of the tests related to this component failed. This means that the Infection Monkey detected an unmet Zero Trust requirement.
- {{< label warning Verify >}} At least one of the tests' results related to this component requires further manual verification.
- {{< label success Passed >}} All Tests related to this pillar passed. No violation of a Zero Trust guiding principle was detected.
- {{< label unused Unexecuted >}} This status means no tests were executed for this pillar.

![Zero Trust Report summary](/images/usage/reports/ztreport1.png "Zero Trust Report summary")

## Test results

This section shows how your network fared against each of the tests the Infection Monkey ran. The tests are ordered by Zero Trust pillar, so you can quickly navigate to the category you want to prioritize.

![Zero Trust Report test results](/images/usage/reports/ztreport2.png "Zero Trust Report test results")

## Findings

This section shows each test's details, including the explicit events and exact timestamps for the activities that took place in your network. This enables you to compare results with your SOC logs and alerts to gain more in-depth insights.

![Zero Trust Report Findings](/images/usage/reports/ztreport3.png "Zero Trust Report Findings")

## Events

Your results are exportable. Click **Export** after clicking on **Events** to view them in a machine-readable format.

![Zero Trust Report events](/images/usage/reports/ztreport4.png "Zero Trust Report events")
