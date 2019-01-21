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
