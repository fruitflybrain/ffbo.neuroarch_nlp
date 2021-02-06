#from neuroarch_nlp.interface import Translator

# Ignore all exceptions so that this doesn't cause package installation
# to fail if pkg_resources can't find neurokernel:
try:
    from version import __version__
except:
    pass

import logging
def set_loglevel( level=logging.INFO ):
    log = logging.getLogger( 'neuroarch_nlp' )
    log.setLevel( level )
