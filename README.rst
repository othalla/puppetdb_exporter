=================
Puppetdb Exporter
=================

.. image:: https://travis-ci.org/othalla/puppetdb_exporter.svg?branch=master
  :target: https://travis-ci.org/othalla/puppetdb_exporter
.. image:: https://codecov.io/gh/othalla/puppetdb_exporter/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/othalla/puppetdb_exporter
.. image:: https://api.codacy.com/project/badge/Grade/835f9979c70f48c698f839f5b9d0ff8f
  :target: https://www.codacy.com/app/othalla/puppetdb_exporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=othalla/puppetdb_exporter&amp;utm_campaign=Badge_Grade
.. image:: https://badge.fury.io/py/puppetdb-exporter.svg
  :target: https://badge.fury.io/py/puppetdb-exporter


Prometheus exporter for PuppetDB.

Install
-------

.. code-block:: sh

    $ git clone https://github.com/othalla/puppetdb_exporter

Configuration
-------------

Exporter reads config from `CONFIG_FILE` environment variable.

Example
~~~~~~~

.. code-block:: ini

   [puppetdb]
   host = puppetdb.example.local
   port = 8080
   ssl_verify = path/to/authority
   ssl_key = path/to/key
   ssl_cert = path/to/cert
   proto = https
   [optional]
   fact_list = kernelrelease values.architecture
