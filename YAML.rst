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

Specific Scalars::

    null: ~
    true: y
    false: n
    string: '12345'