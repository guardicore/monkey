.. Infection Monkey documentation master file, created by
   sphinx-quickstart on Fri May 20 13:39:09 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
##################################
Infection Monkey documentation hub
##################################


.. toctree::
   :hidden:

   Home page <self>
   Monkey Island <_autosummary/monkey_island>
   Common package <_autosummary/common>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



What is Guardicore Infection Monkey?
====================================

The Infection Monkey is an open-source breach and attack simulation tool for testing a data center's resiliency to perimeter breaches and internal server infection.
Infection Monkey will help you validate existing security solutions and will provide a view of the internal network from an attacker's perspective.

Infection Monkey is free and can be downloaded from hyperlink: `our homepage <https://infectionmonkey.com/>`_.


.. image:: _static/images/monkey-teacher.svg
  :width: 400
  :alt: Infection Monkey Documentation Hub Logo
  :align: center

How it works
============

Architecturally, Infection Monkey is comprised of two components:

* Monkey Agent (Monkey for short) - a safe, worm-like binary program which scans, propagates and simulates attack techniques on the **local network**.
* Monkey Island Server (Island for short) - a C&C web server which provides a GUI for users and interacts with the Monkey Agents.

The user can run the Monkey Agent on the Island server machine or distribute Monkey Agent binaries on the network manually. Based on
the configuration parameters, Monkey Agents scan, propagate and simulate an attacker's behavior on the local network. All of the
information gathered about the network is aggregated in the Island Server and displayed once all Monkey Agents are finished.


Results
=======

The results of running Monkey Agents are:
 - A map which displays how much of the network an attacker can see, what services are accessible and potential propagation routes.
 - A security report, which displays security issues that Monkey Agents discovered and/or exploited.

..
  A more in-depth description of reports generated can be found in the [reports documentation page]({{< ref "/reports" >}}).

Getting Started
===============

If you haven't downloaded Infection Monkey yet you can do so `from our homepage <https://www.akamai.com/infectionmonkey#download>`_.

..
  After downloading the Monkey, install it using one of our [setup guides]({{< ref "/setup" >}}), and read our [getting started guide]({{< ref "/usage/getting-started" >}}) for a quick-start on Monkey!

Support and community
=====================

If you need help or want to talk all things Monkey, you can `join our public Slack workspace <https://join.slack.com/t/infectionmonkey/shared_invite/zt-2cm5qiayf-yiEg5RPau0zQhki9xTlORA>`_ or `contact us via Email <mailto:support@infectionmonkey.com>`_.
