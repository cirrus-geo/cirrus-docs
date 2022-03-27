Tasks
=====

Anatomy of a task
-----------------

Tasks in Cirrus implement a unit of processing, to be composed together into a
:doc:`Workflow <workflows/index>`. Tasks are expected to support both input and
output formatted as a :doc:`Cirrus Process Payload </payload>`. As part of its
processing, a task can make any requisite modifications to its input payload
and/or derive any output assets, pushing them to the canonical storage location
in S3.

Tasks can make use of AWS Lambda and/or AWS Batch for execution. Lambda tasks
are simpler to manage and quicker to start up, but the Lambda runtime
constraints can be prohibitive or untenable for some task workloads. In those
cases, Batch allows for extended runtimes, greater resource limits, and
specialized instance types.

In a Cirrus project, tasks are stored inside the ``tasks/`` directory, each in a
subdirectory named for the task. Each task requires a ``definition.yml`` file with
the task's configuration, and a ``README.md`` file documenting the task's usage.


Lambda-only tasks
^^^^^^^^^^^^^^^^^^

Lambda-only tasks follow the specifications outlined in the :doc:`Lambda-based
components <lambdas>` documentation. Refer there for specifics on what files
are requried for Lambda tasks and how to structure the ``definition.yml`` file.


Batch-only tasks
^^^^^^^^^^^^^^^^

Tasks that support only Batch operation need only a ``definition.yml`` file and
``README.md`` file. Batch-only tasks include CloudFormation resource
declarations in the ``definition.yml`` file for all resources required for the
Batch execution environment.

At minimum, a Batch job definition resource is required, which should specify a
link to an ECR image managed/built via an external source. Often Batch tasks
include dedicated compute environment and job queue resources. Other common
resources such as launch templates, IAM roles and profiles, and ECR
repositories can be found in Batch task definitions.

That said, it is sometimes advantageous to share resources between multiple
Batch tasks, in which case these resources can also be declared within the
project's ``cloudformation/`` directory, unattached to any specific task
instance. When in doubt, however, defer to declaring unique resources per Batch
task rather than sharing, even at the expense of duplication. Duplicating
resources in this way is often easier to manage and allows more-specific
configurations.


Environment variables
*********************

Batch job definition resources support defining a list of environment variable
names and values, similar to Lambda functions, though with a slightly different
format. Like Lambda tasks, Batch tasks job definitions support the task
definition's top-level ``environment`` specification, which they inherit, along
with any environment variable defined globally in the ``cirrus.yml`` file under
the ``provider.environment`` key, with preference to any duplicate varaibles
defined on the Batch job defintion.

Additionally, ``AWS_REGION`` and ``AWS_DEFAULT_REGION`` are added to the job
defintion's environment variables with the value derived from the stack's
deployment region.


IAM permissions
***************

.. TODO

Batch permissions are specified via an instance IAM role assigned in
the compute environment. Best practice suggests that a unique role should be
used per Batch task, as is the case for Lambda tasks.


Lambda vs Batch
---------------

When to chose Lambda
^^^^^^^^^^^^^^^^^^^^

.. TODO

* small code size/not many dependencies
* single-threaded
* short runtime (no more than 15 minutes max)
* need code to live in the cirrus project repo


When to chose Batch
^^^^^^^^^^^^^^^^^^^

.. TODO

* long runtimes
* large package size/non-native dependecies
* can use multiple CPUs
* easier to manage code as separate container images
* need significant RAM
* need more than 10GB disk
* need special hardware resources (e.g., GPU)


Or maybe both?
^^^^^^^^^^^^^^

Sometimes both Lambda and Batch can fit the task requirements, depending on
input. Other times, avoiding the overhead of managing/deploying a Batch
container image makes Lambda attractive, but runtime constraints like max
execution time mean that only Batch is viable.

In each of these cases, one can specify a task as *both* Lambda and Batch,
using the Cirrus Batch Lambda runner container to run the packaged Lambda code.
Doing this allows the user to choose which execution mechanism is most
appropriate in a given context. This could be parameterized in a workflow based
on the input (like a ``batch`` flag in the task parameters), or on logic in an
separate input inspection Lambda. Some workflows could always run the Lambda
version of a task, and others the batch version. Or maybe the Batch version is
the only ever actually used, taking advantage of the Lambda packaging support
solely to make it easier to keep task code inside the Cirrus project.

Using the Batch Lambda runner
*****************************

.. TODO

See the `cirrus-task-image`_ repo for more information.

.. _cirrus-task-image: https://github.com/cirrus-geo/cirrus-task-images


Creating a new task
-------------------

Lambda-only
^^^^^^^^^^^

Batch-only
^^^^^^^^^^

Lambda and Batch
^^^^^^^^^^^^^^^^


Compute Environments
^^^^^^^^^^^^^^^^^^^^

Using the AWS spot market
*************************

Task parameters
---------------

Running tasks locally
---------------------
