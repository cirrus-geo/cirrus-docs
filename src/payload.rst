Cirrus Process Payload
======================

A Cirrus Process Payload is JSON containing the input metadata along with a parameters
for processing that metadata. The input metadata is structured like a GeoJSON FeatureCollection
where the individual features are typically STAC Items.


.. list-table:: Cirrus Process Payload
   :widths: 25 25 50
   :header-rows: 1

   * - Field Name
     - Type
     - Description
   * - type
     - string
     - Type of the GeoJSON Object. If set, it must be set to FeatureCollection.
   * - features
     - [item]
     - An array of STAC-like input items
   * - process
     - [ProcessDefinition]
     - An array of process definitions


item
^^^^

An item is like a STAC Item, and can contain any fields in a STAC Item. While it is 
most commonly a complete STAC Item, the only absolutely required field is an `id`.

.. list-table:: STAC-like item
   :widths: 25 25 50
   :header-rows: 1

   * - Field Name
     - Type
     - Description
   * - id
     - string
     - **REQUIRED** An ID for this item


ProcessDefinition
^^^^^^^^^^^^^^^^^

.. list-table:: Cirrus Process Payload
   :widths: 25 25 50
   :header-rows: 1

   * - Field Name
     - Type
     - Description
   * - workflow
     - string
     - **REQUIRED** Name of the workflow to run
   * - asset_upload_options
     - AssetUploadOptions
     - Parameters affecting the upload of item assets


ProcessDefinition
^^^^^^^^^^^^^^^^^

.. list-table:: Cirrus Process Payload
   :widths: 25 25 50
   :header-rows: 1

   * - Field Name
     - Type
     - Description
   * - id
     - string
     - **REQUIRED** An ID for this item


.. code-block:: json-object
    {
        "type": "FeatureCollection",
        "features": [
            {
                <stac-item-1>
            },
            {
                <stac-item-2>
            }
        ],
        "process": {
            <process-definition>
        }
    }

Any number of features (STAC Items) can be input into a workflow, although it is up to
the individual tasks in the workflow to make use of the input metadata. The most common
use-case is to take in a single input Item and generate a single output Item.

Non-STAC Input
--------------

The `features` in the payload need not be fully validated STAC Items. Each task in a workflow
has it's own requirements and may do validation on the input. Payloads that fail validation
of any task in a workflow should throw an `InvalidInput` exception, which will mark the
job in the state database as `INVALID`.

The most common scenario of non-STAC input is when the workflow is for the creation of STAC
Items from other metadata formats.



Process Definition
------------------



