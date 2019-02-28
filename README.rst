=================
Puppetdb Exporter
=================

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

