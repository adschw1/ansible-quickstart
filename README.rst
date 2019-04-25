Ansible Network Configuration Quickstart Guide
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

Spaces are not mandatory and consistency does not matter as long as the ``a:``, ``b:``, ``c:`` and ``-``'s are correctly indented.

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

Create a file named ``inventory`` with the extension ``yml``, ``yaml``, or ``ini``, this can be accomplished many different ways::

    touch inventory.ini
    vim inventory.yaml
    echo "" > inventory.yml
    
This file holds a list of devices and can be specified by using ``-i inventory``
There are many differnet types, find a inventory format that suits you. You don't really need to worry about indenting with ``.ini`` files, I would recommend starting with those.

Example of a ``.ini` inventory:

.. code-block:: ini

    [routers]
    R1 ansible_host=192.168.1.10 ansible_port=2001
    R2 ansible_host=192.168.1.20 ansible_port=2002
    [routers:vars]
    ansible_user=cisco
    ansible_password=admin

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
      vars:
        ansible_user: cisco
        ansible_password: admin



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

  # poc_playbook.yml
  ---
  - name: Configure Cisco IOU
    hosts: routers
    gather_facts: False
    tasks:
      - name: Now Configuring
        debug:
          msg: '{{inventory_hostname}}: {{ansible_host}} {{ansible_port}}'
      - name: 
        shell: |
          set timeout 5
          
          spawn telnet {{ansible_host}} {{ansible_port}}

          expect "Escape character is '^]'."
          send "\n\n\n"
      
          expect "Router>"
          send "\nterm length 0\nen\nconf t\nhost {{inventory_hostname}}\n"

            args:
              executable: /usr/bin/expect
            changed_when: yes
            delegate_to: localhost

Now right away you may notice this doesn't look very pratical, and you would be right, but who in their right mind would ever configure emulated devices through Ansible anyways?

Generate Config Files through Templates
=======================================

Template File Structure for Jinja
---------------------------------

File Structure::

  templates/
  ├── roles/
  │   ├── computer/
  │   │   ├── tasks/
  │   │   │   └── main.yaml
  │   │   ├── templates/
  │   │   │   └── computer.j2
  │   │   └── vars/
  │   │       └── main.yaml
  │   ├── router/
  │   │   ├── tasks/
  │   │   │   └── main.yaml
  │   │   ├── templates/
  │   │   │   └── router.j2
  │   │   └── vars/
  │   │       └── main.yaml
  │   └── switch/
  │       ├── tasks/
  │       │   └── main.yaml
  │       ├── templates/
  │       │   └── switch.j2
  │       └── vars/
  │           └── main.yaml
  └── site.yaml

This is the file structure I used, although I am certain it can be accomplished several other ways. The great thing about this file structure is you don't need to specify an inventory file.

Generate Configs from Templates 
-------------------------------

Let's first create our "driver" that will call upon all the individual roles.

I named mine ``site.yaml`` but anything will work::

  ---
  - name: Generate All Configuration Files
    hosts: localhost
    gather_facts: false
    roles:
      - router
      - switch
      - computer

Notice this calls upon the directory roles, and then the individual types of devices. This will activate the ``/router/tasks/main.yaml`` file.

Let's take the role ``router`` as an example::

  ---
  - name: Generate configuration files
    # TODO: be sure to change the path to the configs directory
    template: src=~/playground/ansithon/templates/roles/router/templates/router.j2 dest=~/playground/ansithon/configs/{{item.hostname}}.txt
    with_items: "{{ routers }}"

Let's break this down, template has two variables ``src`` and dest`` which take us to the location of the router jinja template and config directory respectively.

The line ``with_items: "{{ routers }}"`` tells Ansible which group to use from the ``/router/vars/main.yaml`` file. For instance you may have different groups of routers or different configuration templates, if so you could send the configurations to different destinations.

Obviously my directories will be different than yours, I recommend using ``/etc/ansible/configs`` on Linux. **Note:** do not confuse this with the Ansible Template module, that is for disseminating the configs to devices.

Next, let's look at our ``/router/vars/main.yaml`` file::

  ---
  routers:
    - hostname: R1
      secret: cisco1
      loopback: 1.1.1.1 255.255.255.255

    - hostname: R2
      secret: cisco2
      loopback: 2.2.2.2 255.255.255.255

    - hostname: R3
      secret: cisco3
      loopback: 3.3.3.3 255.255.255.255

We can see this is a basic yaml inventory file, although the indentation is a little different from what we did previously. These items can be referenced in the ``router.j2`` template by using ``{{ item.hostname }}``, ``{{ item.secret }}``, and ``{{ item.loopback }}``.

Calling our template generation couldn't be simpler, since my file is named ``/templates/site.yaml`` all I need to do is run ``ansible-playbook site.yaml`` and configurations are quickly generated and sent to my ``/configs`` directory

Finally we need to create our template, this is done in the ``/router/templates/router.j2`` file::

  !
  no service pad
  service tcp-keepalives-in
  service tcp-keepalives-out
  service timestamps debug datetime msec localtime show-timezone
  service timestamps log datetime msec localtime show-timezone
  service password-encryption
  !
  hostname {{item.hostname}}
  !
  interface loopback0
  description loopback
  ip address {{item.loopback}}
  !
  enable secret {{item.secret}}
  boot-start-marker
  boot-end-marker
  !
  logging buffered 32000
  no logging console