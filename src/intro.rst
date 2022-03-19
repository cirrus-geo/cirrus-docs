Introduction to Cirrus
======================

What is Cirrus?
---------------

Cirrus is a `STAC`_-based geospatial processing pipeline built using a serverless
and scalable architecture. Cirrus can scale from tiny workloads of tens of items
to massive workloads of millions of items in both a cost-efficient and
performance-efficient manner, regardless if your pipeline processing takes
seconrds, hours, or longer.

Cirrus made of `cirrus-geo`_, a cli-based project mangement and deploy tool, as
well as `cirrus-lib`_, a Python library providing a number of useful
abstractions solving common needs for users writing their own Cirrus components.

.. _STAC: https://github.com/cirrus-geo/cirrus-docs
.. _cirrus-geo: https://cirrus-geo.github.com/cirrus-geo
.. _cirrus-lib: https://cirrus-geo.github.com/cirrus-lib


Why Cirrus?
-----------


Concepts
--------

Cirrus Components
^^^^^^^^^^^^^^^^^

Cirrus is organized into reusable blocks called :doc:`Components
<components/index>`, which can be broken down into three main types:

* :doc:`Feeders <components/feeders>`: take arbitrary input in and create a
  Cirrus Process Payload, which is enqueue for processing
* :doc:`Tasks <components/tasks>`: the basic unit of work in a Workflow, uses a
  Cirrus Process Payload for both input and output
* :doc:`Worflows <components/workflows>`: a set of Tasks implementing a
  processing pipeline to transform a given input into one or more output STAC
  items

An additional component type is that of a :doc:`Function
<components/functions>`, though they are less commonly extended by end users.


STAC-based workflows
^^^^^^^^^^^^^^^^^^^^


Horizontal vs vertical scaling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Relationship with stac-server
-----------------------------

Cirrus Workflows create STAC items, which are stored in S3 for persistence and
can be published to `stac-server`_ (or any other STAC API) for indexing/search.
In other words, Cirrus generates the data, stac-server makes it easily
accessible to end-users and the whole world of STAC tooling.

.. _stac-server: https://github.com/stac-utils/stac-server


Example use cases
-----------------


AWS services used
-----------------

Cirrus is built on top of a number of AWS services that allow its serverless and
scalable architecture, including:

* Lambda: underlays tasks, feeders, and functions
* Batch: supports longer runtimes and/or custom resource requirements for
  feeders and tasks
* SNS: messages to multiple subscribers
* SQS: message queueing for reliability
* DynamoDB: State-tracking database
* Step Functions: multi-step functions underlying workflows
* ECR: image hosting for batch and lambda containers
* IAM: funciton roles and associated permissions/access policies
* S3: persistent storage for input payloads and generated items and their assets
* CloudFormation: infrastructure-as-code and deployment automation
* EventBridge: trigger processing on specific events, like workflow completion
