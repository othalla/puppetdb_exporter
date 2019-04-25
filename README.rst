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

Configuration reads one of these files in this order:

- `/etc/puppetdb_exporter/config.ini`
- `.config/puppetdb_exporter/config.ini`
- `config.ini`

You can specify a custom config file by setting the CONFIG_FILE environment var.

Example
~~~~~~~

.. code-block:: ini

   [main]
   puppetdb_host = puppetdb.example.local
   puppetdb_port = 8080
   puppetdb_ssl_verify = path/to/authority
   puppetdb_key = path/to/key
   puppetdb_cert = path/to/cert
   puppetdb_proto = https
   [optional]
   fact_list = kernelrelease values.architecture


