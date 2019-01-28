from pypuppetdb import connect

from puppetdb_exporter.config import get_config


def _get_puppetdb_connexion():
    config = get_config()
    return connect(host=config['PUPPETDB_HOST'],
                   port=config['PUPPETDB_PORT'],
                   ssl_verify=config['PUPPETDB_SSL_VERIFY'],
                   ssl_key=config['PUPPETDB_KEY'],
                   ssl_cert=config['PUPPETDB_CERT'],
                   timeout=config['PUPPETDB_TIMEOUT'],
                   protocol=config['PUPPETDB_PROTO'],)


def get_nodes():
    database = _get_puppetdb_connexion()
    return database.nodes()
