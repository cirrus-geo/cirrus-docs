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

Here is an example ``definition.yml`` file for a fairly complex Batch-only task
named ``Reproject``::

    description: A sample Batch-only task definition
    environment:
      BATCH_VAR_1: some value
      OVERRIDDEN_VAR: another_value
    enabled: true
    batch:
      enabled: true
      resources:
          Resources:

            ReprojectBatchJob:
              Type: "AWS::Batch::JobDefinition"
              Properties:
                JobDefinitionName: '#{AWS::StackName}-Reproject'
                Type: Container
                Parameters:
                  url: ""
                ContainerProperties:
                  Command:
                    - cirrus-batch.py
                    - process
                    - Ref::url
                  Environment:
                    - Name: JOB_DEF_VAR
                      Value: 1234
                    - Name: OVERRIDDEN_VAR
                      Value: last_value
                  ResourceRequirements:
                    - Type: VCPU
                      Value: 32
                    - Type: MEMORY
                      Value: 240000
                    - Type: GPU
                      Value: 4
                  Image: '123456789012.dkr.ecr.#{AWS::Region}.amazonaws.com/some-image-name:${opt:stage}'

            ReprojectLaunchTemplate500GB:
              Type: AWS::EC2::LaunchTemplate
              Properties:
                LaunchTemplateName: '#{AWS::StackName}-Reproject-500GB'
                LaunchTemplateData:
                  BlockDeviceMappings:
                    - Ebs:
                        VolumeSize: 500
                        VolumeType: gp3
                        DeleteOnTermination: true
                        Encrypted: true
                      DeviceName: /dev/xvda

            ReprojectComputeEnvironment500GB:
              Type: AWS::Batch::ComputeEnvironment
              Properties:
                ComputeEnvironmentName: '#{AWS::StackName}-Reproject-500GB'
                Type: MANAGED
                ServiceRole: !GetAtt BatchServiceRole.Arn
                ComputeResources:
                  MaxvCpus: 2000
                  SecurityGroupIds: ${self:custom.batch.SecurityGroupIds}
                  Subnets: ${self:custom.batch.Subnets}
                  InstanceTypes:
                    - p3.8xlarge
                  Type: EC2
                  AllocationStrategy: BEST_FIT_PROGRESSIVE
                  MinvCpus: 0
                  InstanceRole: !GetAtt ReprojectInstanceProfile.Arn
                  LaunchTemplate:
                    LaunchTemplateId: !Ref ReprojectLaunchTemplate500GB
                    Version: $Latest
                  Tags: {"Name": "Batch Instance - #{AWS::StackName}"}
                  DesiredvCpus: 0
                State: ENABLED

            ReprojectJobQueue500GB:
              Type: AWS::Batch::JobQueue
              Properties:
                JobQueueName: '#{AWS::StackName}-Reproject-500GB'
                ComputeEnvironmentOrder:
                  - Order: 1
                    ComputeEnvironment: !Ref ReprojectComputeEnvironment500GB
                State: ENABLED
                Priority: 1

            ReprojectInstanceRole:
              Type: AWS::IAM::Role
              Properties:
                AssumeRolePolicyDocument:
                  Version: '2012-10-17'
                  Statement:
                    - Effect: Allow
                      Principal:
                        Service:
                          - ec2.amazonaws.com
                      Action:
                        - sts:AssumeRole
                Path: /
                ManagedPolicyArns:
                  - arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role
                Policies:
                  - PolicyName: Cirrus
                    PolicyDocument:
                      Version: '2012-10-17'
                      Statement:
                        - Effect: Allow
                          Action:
                            - s3:PutObject
                          Resource:
                            - Fn::Join:
                                - ''
                                - - 'arn:aws:s3:::'
                                  - ${self:provider.environment.CIRRUS_DATA_BUCKET}
                                  - '*'
                            - Fn::Join:
                                - ''
                                - - 'arn:aws:s3:::'
                                  - ${self:provider.environment.CIRRUS_PAYLOAD_BUCKET}
                                  - '*'
                        - Effect: Allow
                          Action:
                            - s3:ListBucket
                            - s3:GetObject
                            - s3:GetBucketLocation
                          Resource: '*'
                        - Effect: Allow
                          Action: secretsmanager:GetSecretValue
                          Resource:
                            - arn:aws:secretsmanager:#{AWS::Region}:#{AWS::AccountId}:secret:cirrus*
                        - Effect: Allow
                          Action:
                            - lambda:GetFunction
                          Resource:
                            - arn:aws:lambda:#{AWS::Region}:#{AWS::AccountId}:function:#{AWS::StackName}-*

            ReprojectInstanceProfile:
              Type: AWS::IAM::InstanceProfile
              Properties:
                Path: /
                Roles:
                  - Ref: ReprojectInstanceRole


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

The ``ReprojectBatchJob`` resource defines a CloudFormation resouce of job
definition type, and represents the job configuration used when running our
``Reproject`` job. The job definition includes such configuration settings as
the container image to run, the command to run inside that container, and the
resource requirements of the container. See the `AWS Job Definition
CloudFormation reference`_ for the full list of supported settings.

It is worth highlighting a few aspects of job definition resources.

.. _AWS Job Definition CloudFormation reference: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html


Job parameters
**************

The job definition ``Parameters`` key defines a list of parameter and optional
default values that can be passed in to a job instance when run. In the example
above, the ``url`` parameter is used to pass an S3 URL of the process payload
in to the executed command.

This is an important note: Batch has a rather low limit on the size of a job
sent to the SubmitJob API (`30KiB at current`_). To mitigate impacts from this
limit, use the ``pre-batch`` task immediately prior to any batch tasks to upload
the payload to S3 and return a ``url`` to that payload, which can then be
referenced when calling the batch job as the value to the ``url`` parameter.

In the ``ReprojectBatchJob`` example resource above, we can see that the ``url``
parameter is referenced in the executed command::

    Command:
      - cirrus-batch.py
      - process
      - Ref::url

which tells Batch to run a command like::

    ❯ cirrus-batch.py process <contents_of_url_parameter>

Exactly what command should be specified for a job definition is dependent on
the appropriate entry point inside the specified container image. Regardless,
that entry point should be expecting an S3 URL to a process payload, specified
in some manner. ``cirrus-lib`` provides convenince classes/methods to help with
this common need.

The Batch tasks should replace the payload in S3 at the end of execution after
any modifications. Follow the Batch task with the ``post-batch`` task to resolve
that S3 URL into a JSON payload to pass to successive tasks. ``post-batch`` will
also pull any Batch errors from the logs and raise them within the workflow, in
the event of an unsuccessful Batch execution.

See :doc:`Batch tasks in workflows <../workflows/batch>` for an example of how a
payload is passed to a job using this ``url`` parameter, how ``pre-batch`` and
``post-batch`` are used, and some other tips regarding Batch tasks in workflows.

Job parameters can also be used for other job settings, but are most commonly
used within the ``Command`` specification in Cirrus.

.. _30KiB at current: https://docs.aws.amazon.com/batch/latest/userguide/service_limits.html


Environment variables
*********************

Batch job definition resources support defining a list of environment variable
names and values, similar to Lambda functions, though with a slightly different
format. Like Lambda tasks, Batch tasks job definitions support the task
definition's top-level ``environment`` specification, which they inherit, along
with any environment variable defined globally in the ``cirrus.yml`` file under
the ``provider.environment`` key, with preference given to any duplicate
varaibles defined on the Batch job defintion.

Additionally, ``AWS_REGION`` and ``AWS_DEFAULT_REGION`` are added to the job
defintion's environment variables with the value derived from the stack's
deployment region.

If ever in doubt about the final environment variables/values (or the values of
any other parameters) used in a Batch task definition, the ``cirrus`` cli
provides a ``show`` command that runs the full configuration interpolation to
generate the "complete" definition as it appears in the compiled configuration
generated by the ``build`` command. Run it like this::

    ❯ cirrus show task <TaskName>


Resource requirements
*********************

The ``ResourceRequirements`` key allows specification of a list of all hardware
resources required by the job (unfortunately with the exception of disk space).
Note that the values provided here serve as defaults for spawned jobs, and can
be overriden when calling ``SubmitJob`` in the workflow. Again, see :doc:`Batch
tasks in workflows <../workflows/batch>` for an example of overriding resource
requirements.

The specified resource requirements are used by the compute environment to pick
an appropriate-sized instance type for the job, either by doing a best fit
across all available instance types, or by selecting the best fit instance type
from a user-provided list. Additional factors come into play with instance
selection such as whether the compute environment is using on-demand or spot
instance.

Optimizing task resource requirements to the minimum required is critical.
While doing so certainly provides an important cost savings, often the more
meaningful reason to do so is to ensure fast instance start up time. Larger
instances can take much longer to become available than small instance, delaying
instance provisioning and therefore job start.


Image specification
*******************

The ``Image`` key accepts an image name within a docker registry in the form
``repository-url/image:tag``. If omitted, the ``repository-url`` will point to
Docker Hub.

For Cirrus tasks, using the AWS Elastic Container Registry to store images is
common, as is show in the example ``Image`` value::

    123456789012.dkr.ecr.#{AWS::Region}.amazonaws.com/some-image-name:${opt:stage}

Note the use of the Serverless parameter ``${opt:stage}``, which allows
specification of an image tag based on the stage in a multi-stage deployment
pipeline. For example, if we have a deployment pipeline with the stages,
``dev``, ``staging``, and ``prod``, we will want to ensure we have image
versions in the ECR repo with tags of those same names.


Compute environments
^^^^^^^^^^^^^^^^^^^^



Using the AWS spot market
*************************


Launch templates
^^^^^^^^^^^^^^^^


IAM permissions
^^^^^^^^^^^^^^^

.. TODO

Batch permissions are specified via an instance IAM role assigned in
the compute environment. Best practice suggests that a unique role should be
used per Batch task, as is the case for Lambda tasks.


Job queues
^^^^^^^^^^

Compute environments are not actually referenced when submitting a job.
Instead, a job queue is specified, which itself provides a link to a specific
compute environment. Job queues are used as a means of holding submitted jobs
while waiting for available CPUs in a saturated compute environment, and can
also provide prioritization in the case where different types of jobs share a
single compute environment.

Multiple compute environment can also be specified for a single queue. This can
be useful in the case of wanting some on-demand capacity, but pushing overflow
into the spot market, or vise versa.

Job queues can be combined with a `Batch scheduling policy`_ for advanced
use-cases.

See the `job queue CloudFormation documentation`_ for more information about
supported job queue configurations.

.. _Batch scheduling policy:
   https://docs.aws.amazon.com/batch/latest/userguide/scheduling-policies.html
.. _job queue CloudFormation documentation:
   https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html


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

In addition to support for CloudFormation ``Resources`` under
``batch.resources``, Cirrus also supports defining other CloudFormation
template section types such as ``Outputs`` or ``Conditions``. Use those as
required to keep such items together with the associated Batch task.


Viewing Batch CloudFormation resources with the cli
---------------------------------------------------

Best practices for managing changes to Batch resources
------------------------------------------------------
