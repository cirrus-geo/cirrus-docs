Cirrus Components
=================

Cirrus features several component types, which each represent a specific role
within the Cirrus architecture.

A single component is made up of a collection of files, minimally a
``definition.yml`` file containing the component configuration, and a
``README.md`` file outlining the component usage and any other necessary
documentation for the component. Additional required files vary per component
type. All the files for a given component are stored in a single directory named for the component instance::

    <component_name>/
        definition.yml
        README.md
        ...

Within a Cirrus project directory, components are organized in subdirectories
named for their respective component types, like so::

    <project_dir>/
        feeders/
            feeder1/
            feeder2/
        functions/
        tasks/
            atask/
        workflows/
            aworkflow/

Each component types has in-depth documentation detailing any supported files
and the ``definition.yml`` format. Some components share a common set of
required files and configuration format, such as all :doc:`Lambda-based
components <lambdas>`.


Feeders
-------

Conceptually, a feeder is anything that generates a :doc:`Cirrus Process
Payload <../payload>` and queues it for processing. In practice this could be
anything from a user hand-rolling JSON and pasting it into the AWS console, to
an automated process that turns external events into process payloads and
publishes them to the Cirrus process topic.

Within a Cirrus project instance, however, the term ``feeder`` refers
specifically to an AWS Lambda function that takes arbitrary input in, generates
one or more Cirrus Process Payloads, and publishes them to the Cirrus process
SNS topic.

As a component with a Lambda base, the :doc:`Lambda-based components <lambdas>`
documentation contains relevant information for this and other Lambda
components.

See the :doc:`feeders documentation <feeders>` for more details specific to
feeders.


Tasks
-----

Tasks represent the basic building block of Cirrus processing. Implemented as
AWS Lambda functions and/or AWS batch job definitions, tasks use a Cirrus
Process Payload for both input and output, and are intended to be composed into
a Cirrus workflow.

In other other words, to implement custom processing routines for a pipeline,
use a task. The best tasks are modular, simple, focused, and composable. Most
projects end up with more custom tasks than other component types, so it pays
to be familiar with the tasks ins and outs.

For tasks supporting Lambda executions, the :doc:`Lambda-based components
<lambdas>` documentation contains relevant information for this and other
Lambda components.

See the :doc:`tasks documentation <tasks>` for in-depth usage information.


Workflows
---------

Cirrus workflows are the component that puts the "pipe" in "pipeline".
Workflows model a transformation of an input item or set of input items with a
process definition into one or more output items via processing from one or
more tasks.

Cirrus also provides several mechanisms for modeling workflow dependencies.

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

As a component with a Lambda base, the :doc:`Lambda-based components <lambdas>`
documentation contains relevant information for this and other Lambda
components.

Further details regarding functions are available in the :doc:`functions
documentation <functions>`.
