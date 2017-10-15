About
=======

Welcome to the Infection Monkey! 

The Infection Monkey is an open source security tool for testing a data center's resiliency to perimeter breaches and internal server infection. The Monkey uses various methods to self propagate across a data center and reports success to a centralized C&C server. To read more about the Monkey, visit https://www.infectionmonkey.com 

Features include:

* Multiple propagation techniques:
  * Predefined passwords
  * Common exploits
  * Password stealing using mimikatz
* Multiple exploit methods:
  * SSH
  * SMB
  * RDP
  * WMI
  * Shellshock
  * SambaCry
  * Elastic Search
  
* A C&C server with a dedicated UI to visualize the Monkey's progress inside the data center

The Infection Monkey is comprised of two parts: the Monkey and the C&C server.
The monkey is the tool which infects other machines and propagates to them, while the C&C server collects all Monkey reports and displays them to the user.

Building the Monkey from source
-------------------------------
If you want to build the monkey from source instead of using our provided packages, follow the instructions at the readme files under [chaos_monkey](chaos_monkey) and [monkey_island](monkey_island). 