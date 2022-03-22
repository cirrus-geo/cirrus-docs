Cirrus Components
=================

Feeders
-------

Conceptually, a feeder is anything that generates a :doc:`Cirrus Process
Payload <../payload>` and queues it for processing. In practice this could be
anything from a user hand-rolling JSON and pasting it into the AWS console, to
an automated process that turns external events into process payloads and
publishes them to the Cirrus process topic.

Within a Cirrus project instance, however, the term ``feeder`` refers
specifically to an AWS lambda function that takes arbirary input in, generates
one or more Cirrus {rocess Payloads, and publishes them to the Cirrus process
SNS topic.

See the :doc:`feeders documentation <feeders>` for more details.


Tasks
-----

Tasks represent the basic building block of Cirrus processing. Implemented as
AWS lambda functions and/or AWS batch job defintions, tasks use a Cirrus
Process Payload for both input and output, and are intended to be composed into
a Cirrus workflow.

In other other words, to implement custom processing routines for a pipeline,
use a task. The best tasks are modular, simple, focused, and composable. Most
projects end up with more custom tasks than other component types, so it pays
to be familiar with the tasks ins and outs.

See the :doc:`tasks documentation <tasks>` for in-depth usage information.


Workflows
---------

Cirrus workflows are the component that puts the "pipe" in "pipeline".
Workflows model a transformation of an input item or set of input items with a
process definition into one or more output items via processing from one or
more tasks.

Cirrus also provides several mechanisms for modeling workflow dependecies.

The :doc:`state database </statedb>` tracks the state of items processed at
the workflow level.

Refer to the :doc:`workflows documentation <workflows/index>` to find more detailed
information regarding workflows.


Functions
---------

The ``function`` component type is mainly used by the Cirrus built-ins required
to implement the core Cirrus functionality. Examples include the ``process``
lambda function, which processes all incoming Cirrus Process Payloads and
dispatches them to their specified workflows, or the ``update-state`` lambda
function that updates the :doc:`state database </statedb>` on workflow
completion events.

In typical use, most Cirrus projects will not require any additional
function-type components. However, they can be occasionally be useful for
lambda utility functions required to manage a given deployment.

Further details regarding functions are available in the :doc:`functions
documentation <functions>`.
