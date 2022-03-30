Batch tasks
===========


Required files
--------------

Tasks that support Batch-only operation need just the standard
``definition.yml`` and ``README.md`` files. Tasks that support both Batch and
Lambda will additionally need all files required for :doc:`Lambda-based
components <../lambdas>`. In the Batch-only case specifically, the task
directory structure looks very similar to Lambda-based tasks::

    <project_dir>/
        tasks/
            BatchTask/
                definition.yml
                README.md


Definition file
---------------

The ``definition.yml`` contains a Lambda component's configuration. The format
is similar to that used by the Serverless Framework, which underlies cirrus's
deployment mechanism, but is subtly different.

Batch tasks include CloudFormation resource declarations in the
``definition.yml`` file for all resources required for the Batch execution
environment. At minimum, a Batch job definition resource is required, which
should specify a link to an ECR image managed/built via an external source.
Often Batch tasks include dedicated compute environment and job queue
resources. Other common resources found in Batch task definitions include
launch templates, IAM roles and profiles, and ECR repositories.

Here is an example ``definition.yml`` file for a fairly complex Batch-only task::

   <Placeholder>

.. TODO

Let's break down the resources at play in this Batch example.

Description
^^^^^^^^^^^

The top-level ``description`` value is used for the component's description
within Cirrus. It has no further purpose in the case of Batch.

Enabled state
^^^^^^^^^^^^^

Components can be disabled within Cirrus, which will exclude them from the
compiled configuration. All components support a top-level ``enabled`` parameter
to completely enable/disable the component. Batch tasks also support
an ``enabled`` parameter under the ``batch`` key, which will enable/disable
just the Batch portion of the component.

For Batch-only components these ``enabled`` controls function more or less
identically. For tasks that support both Batch and Lambda, the
``lambda.enabled`` and ``batch.enabled`` paramters can prove useful in certain
circumstances. However, note that if the Lambda component of a dual
Lambda/Batch task is disabled, the Lambda deployment zip will not be
packaged/deployed and the Lambda will be deleted from AWS. This can leave the
Batch task unable to execute due to the missing code package.


Job definition
^^^^^^^^^^^^^^

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


Compute environments
^^^^^^^^^^^^^^^^^^^^

Using the AWS spot market
*************************


Job queues
^^^^^^^^^^


IAM permissions
^^^^^^^^^^^^^^^

.. TODO

Batch permissions are specified via an instance IAM role assigned in
the compute environment. Best practice suggests that a unique role should be
used per Batch task, as is the case for Lambda tasks.


Other consdierations
--------------------

Shared resources
^^^^^^^^^^^^^^^^

While it is generally encouraged to keep Batch resources isolated to each task,
it can sometimes be advantageous to share resources between multiple Batch
tasks. In this case, these resources can also be declared within the project's
``cloudformation/`` directory, unattached to any specific task instance.

When in doubt, however, defer to declaring unique resources per Batch task
rather than sharing, even at the expense of duplication. Duplicating resources
in this way is often easier to manage and allows more-specific configurations.
Consider shared resources an "expert-paattern", as shared resources bring a lot
of baggage along with them that can increase the potential for issues and other
unintended side effects.

Other CloudFormation template sections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to CloudFormation ``Resources``, Cirrus also supports defining
other CloudFormation template section types such as ``Outputs`` or
``Conditions``. Use those as required to keep such items together with the
associated Batch task.


Viewing Batch CloudFormation resources with the cli
---------------------------------------------------

Best practices for managing changes to Batch resources
------------------------------------------------------
