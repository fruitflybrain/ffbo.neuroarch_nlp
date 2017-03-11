#from neuroarch_nlp.interface import Translator

import logging
def set_loglevel( level=logging.INFO ):
    log = logging.getLogger( 'neuroarch_nlp' )
    log.setLevel( level )
