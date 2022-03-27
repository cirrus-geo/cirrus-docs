Lambda-based components
=======================

Components that use Lambda (feeders, functions, and some tasks) share a common
set of required files and ``definition.yml`` format.


Required files
--------------

In addition to the ``definition.yml`` and ``README.md`` files required by all
components, Lambda-based components also require a ``lambda_function.py`` Python
file implementing a ``lambda_handler`` function, which serves as the Lambda
execution entry point. Like all components, these files are contained within a
directory named for the component within its component type's directory.

For example, if we have a Lambda task component named ``reproject``, we would
end up with a directory structure that looks like this::

    <project_dir>/
        tasks/
            reproject/
                definition.yml
                README.md
                lambda_function.py

The contents of a Lambda-based component's directory--minus the
``definition.yml`` file--will be packaged into a Lambda deployment zip file and
uploaded to AWS on project deploy. Any additional files added by the user will
also be included in the Lambda zip.


``definition.yml``
------------------

.. TODO example definition


Environment variables
*********************

Lambda tasks support the task definition's top-level ``environment``
specification, which they inherit, along with any environment variables defined
globally in the ``cirrus.yml`` file under the ``provider.environment`` key. In
the case of conflicts, inheritence will perfer a value in the Lambda
environment varaibles over one from the task, and one from the task varaibles
over that from the globals.


IAM permissions
***************


Python dependencies
*******************


