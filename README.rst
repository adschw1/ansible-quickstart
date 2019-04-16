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
