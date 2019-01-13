from pypuppetdb import connect

from puppetdb_exporter.config import get_config

PUPPETDB_CONNEXION = None


def _get_puppetdb_connexion():
    global PUPPETDB_CONNEXION
    if PUPPETDB_CONNEXION is None:
        config = get_config()
        PUPPETDB_CONNEXION = connect(host=config['PUPPETDB_HOST'],
                                     port=config['PUPPETDB_PORT'],
                                     ssl_verify=config['PUPPETDB_SSL_VERIFY'],
                                     ssl_key=config['PUPPETDB_KEY'],
                                     ssl_cert=config['PUPPETDB_CERT'],
                                     timeout=config['PUPPETDB_TIMEOUT'],
                                     protocol=config['PUPPETDB_PROTO'],)
    return PUPPETDB_CONNEXION


def get_nodes():
    database = PUPPETDB_CONNEXION
    return database.nodes()
