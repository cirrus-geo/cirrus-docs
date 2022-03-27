Cirrus best practices
=====================

Cirrus has a few guardrails, but generally aims to stay out of the way and
retain as much flexibility as possible to ensure arbitrary constraints cannot
get in the way and prevent any legitimate use-cases. That said, following
certain guidelines can help to ensure a Cirrus deployment remains easy to
manage and administer, which is why we compiled this set of Cirrus best
practices.

Keep in mind the rules on this list are not hard and fast, but it's recommended
to understand the how and why behind a rule before deciding to break it.

Generally good ideas
--------------------

Keep things simple
^^^^^^^^^^^^^^^^^^

Before reaching for a complicated knob or obscure feature, make sure it is
truly required.


Task guidelines
---------------

Use the smallest viable instance size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For batch tacks, use the smallest instance possible. Not only for cost reasons,
but because larger instances can take significantly longer to become available
and start up.


Workflows guidelines
--------------------

Use only one input item per workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Keep workflows short and focused
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Don't use workflows for side-effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. _one-output-set:

Workflows should not produce different outputs from the same set of inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the :doc:`Cirrus Process Payload docs <payload>` for additional details on
how Cirrus's idempotency check works. Generally speaking, cirrus will use the
set of input items as a proxy for the outputs produced by a given workflow.
Don't rely on workflow/task parameters to change the set outputs, as those
settings are not referenced as part of the idempotency check.

This also leads into the next best practice...


Make workflows specific, not flexible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is tempting to make workflows as flexible as possible, having them use
parameters in the process definition to control all sorts of dynamic behavior.
While certain types of dynamism can be advantageous (picking resource
requirements for a batch job depending on input data properties, for example),
generally dynamism in workflows is best avoided, for a few reasons:

* Dynamism within a workflow means one cannot simply assume different
  executions of the same workflow did similar things. This makes
  troubleshooting harder and raises the cognitive load of pipeline management.
* Dynamic workflows can lead to needing to run the workflow multiple times to
  create different sets of outputs. See :ref:`above <one-output-set>`.
* A single workflow path is easier to describe and name explicitly, leading to
  be documentation and easier pipeline on-boarding.
