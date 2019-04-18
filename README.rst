Ansible/Python Network Configuration Quickstart Guide
=====================================================

.. contents::

Installing Ansible
==================

How to install Ansible on your machine

Requirements
------------

- ``Python 2.6`` or *higher*, ``Python 3.x`` is not currently supported.
- If using Windows, ``VirtualBox`` with Ubuntu, CentOS or Mininet

Install using Pip
-----------------

This is probably the easiest way if you have pip installed on your machine.

**Note:** using a virtualenv is ALWAYS recommended.

If you need to install pip:

.. code-block:: bash

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py

Once pip is installed:

.. code-block:: bash

    #sudo if not in Virtualenv
    sudo pip install ansible

Installing on Mac w/ Homebrew
-----------------------------

.. code-block:: bash

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew update
    brew install ansible

Installing on Linux w/ repository
---------------------------------

.. code-block:: bash

    #Ubuntu
    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

    #CentOS
    sudo yum install ansible

Basic Syntax
============


YAML Basics
-----------

- YAML is case sensitive
- The files should have **.yaml** as the extension
- YAML does not allow the use of tabs while creating YAML files; spaces are allowed instead

Block List Format uses ``hypen`` + ``space`` to add new items to a list

.. code-block:: yaml

    --- # Favorite TV shows
    - Breaking Bad
    - New Girl
    - Game of Thrones

Inline List format uses ``comma`` + ``space`` in ``braces``

.. code-block:: yaml

    --- # Todo List
        [dishes, vacuum, workout, cook]

Folded Text format converts newlines to spaces and removes leading whitespace

.. code-block:: yaml

    - {name: John Doe, age: 33}
    # vs
    - name: John Doe
      age: 33

Two more examples of variations

.. code-block:: yaml

    men: [John Doe, Jim Jones]
    women:
    - Jane Doe
    - Diane Williams

Indentation in YAML
-------------------

Spaces are not mandatory and consistency does not matter

.. code-block:: yaml

    a:
    b:
        - 1
        -   2
        -  3
    c:
        "xyz"

Comments in YAML
----------------

.. code-block:: yaml

    # this is a comment

    # yaml does not
    # support
    # multiline Comments

Data Types in YAML
------------------

YAML supports sequences and scalars

Scalar Syntax::

    integer: 25
    string: "25"
    float: 25.0
    boolean: Yes
    null: ~

Mapping scalars to scalars::

    name: Harry
    university: Hogwarts
    major: Wizard

Sequence of scalars::

    - Star Wars
    - Star Trek
    - Harry Potter

Scalar of secquence of scalars::

    Universities:
    - Illinois State University
    - University of Illinois
    - Northwestern University

Nested lists::

    -
     - Cat
     - Dog
     - Goldfish
    -
     - Python
     - Lion
     - Tiger

Configuring Cisco Devices in Ansible
====================================

The sections below will help you get started configuring your Cisco IOS devices.


Building your Inventory
-----------------------

Create a ``txt`` file named ``inventory``, this can be accomplished many different ways::

    touch inventory.ini
    vim inventory.yaml
    echo "" > inventory.etc
    
This file holds a list of devices and can be specified by using ``-i inventory``
There are many differnet types, find a inventory format that suits you.

Example of a ``.ini` inventory:

.. code-block:: ini

    [routers]
    R1 ansible_host=192.168.1.10 ansible_port=2001
    R2 ansible_host=192.168.1.20 ansible_port=2002
    [routers:vars]
    user=cisco
    passwd=admin

Example of a ``.yml`` or ``.yaml`` inventory:

.. code-block:: yaml

    routers:
        hosts:
            R1:  
            ansible_host: 10.110.20.94    
            ansible_port: 2001
            R2:  
            ansible_host: 10.110.20.94    
            ansible_port: 2002



Building your Playbook (in a perfect world)
-------------------------------------------

Wouldn't it be great if things just worked? 

Well, Ansible is one of those tools that is very easy to understand and use, but things aren't always perfect in the real world.

Ansible assumes you are able to ssh into your devices, most of your configurations will be done through ssh.

Below is an example of how one may configure a Cisco device through Ansible:

.. code-block:: yaml

    # perfet_world.yml
    ---
    - name: Configure My Routers
        hosts: routers
        gather_facts: false
        connection: local
        tasks:
            - name: Configure Router Names
            ios_config:
                lines:
                - host {{ inventory_hostname }}
            - name: Configure Router Interfaces
            ios_config:
                lines:
                - ip address {{ ip_address }} {{ subnet_mask}}
                parents: interface Ethernet0


Building your Playbook (in a semi perfect world)
------------------------------------------------

Even if you don't have access to ssh you still have Telnet as a backup, right? Well I couldn't get the Telnet module to work very well.

Below is an example of how one may configure a Cisco device through Telnet:

.. code-block:: yaml
    
    # semi_perfect_world.yml
    ---
    - name: Configure Routers through Telnet  
      telnet:
        host: {{ ansible_host }}
        port: {{ ansible_port }}
        prompts:
        - "[>|#]"
        command:
        - term length 0
        - enable     
        - show version
        - configure terminal
        - hostname {{ inventory_hostname }}
        - end
        - write memory

Building your Playbook (the not fun way)
----------------------------------------

So you tried the other ways and it didn't work, you must be using emulated devices. When all else fails, it's time to get our hands dirty and do things the hard way. Ansible can do just about anything you tell it to, even imitating you using a shell to create a Telent session.

Example of using a bash shell and expect script to create a Telnet session into routers:

.. code-block:: yaml

    ---
    - name: Configure Cisco IOU
      hosts: routers
      gather_facts: False
      tasks:
        - debug:
            msg: '{{ansible_host}} {{ansible_port}}'
        - name: Configure Devices
          shell: |
            set timeout 120
            spawn telnet {{ansible_host}} {{ansible_port}}

            expect "Escape character is '^]'."
            send "\n"        
            spawn telnet {{ansible_host}} {{ansible_port}}

            expect "Router>"
            send "\nterm length 0"

            expect "Router>"
            send "\nen"

            expect "Router#"        
            send "\nconf t\nhost {{inventory_hostname}}\nend\nwr"      

          args:
            executable: /usr/bin/expect
          changed_when: yes
          delegate_to: localhost

Now right away you may notice this doesn't look very pratical, and you would be right, but who in their right mind would ever configure emulated devices through Ansible anyways?