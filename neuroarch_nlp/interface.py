from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

from quepy_analysis.grammar import modifiers_and_regions
from .data import colors_values

na_unigrams = { unigram
                for term in modifiers_and_regions.keys() + colors_values.keys()
                for unigram in term.split() }
# This is for (the temporary) spelling-correction. It, in part, results in a model that performs
# spelling correction on words not found in its (current--at time of writing) grammar.
na_unigrams.update([ 'to', 'in', 'show', 'display', 'hide', 'remove', 'pre', 'post', 'synaptic',
                     'inside', 'of', 'the', 'a', 'all', 'each', 'every', 'neuron', 'interneuron',
                     'transmitter', 'neurotransmitter', 'graph', 'list', 'visualize',
                     'display', 'add', 'and', 'or', 'remove', 'hide', 'for', 'me', 'express',
                     'that', 'which', 'have', 'having', 'transmit', 'release', 'be', 'is', 'are',
                     'within', 'connection', 'input', 'output', 'dendrite', 'dendritic', 'axon',
                     'axonic', 'arborization', 'axonal', 'arborize', 'connect', 'connecting',
                     'with', 'is', 'are', 'presynaptic', 'postsynaptic',
                     'has', 'as', 'single', 'home', 'cartridge', 'network', 'morphology',
                     'undo', 'clear', 'restart', 'arborizing', 'previous', 'last', 'not',
                     'channel', 'expressing', 'process', 'processes', 'transmitting',
                     'cart', 'retina', 'innervate', 'innervating', 'innervation', 'cell',
                     'from', 'keep', 'retain', 'color', 'uncolor', 'pin', 'unpin', 'blink',
                     'unblink', 'animate', 'unanimate', 'unhide',
                     'connections', 'axons', 'dendrites', 'neurons', 'arborizations',
                     'inputs', 'outputs', 'interneurons', 'innervations', 'cells' ])

digit_or_rgbhex = re.compile( r'\b[0-9]+\b|\b(#?[a-fA-F0-9]{1,6})\b' )
simple_tokens = re.compile( r"\b[a-zA-Z0-9_\-']+\b", re.I )

class PrototypeBaselineTranslator(object):
    def __init__(self):
        import quepy
        from quepy_analysis import settings
        settings.PARSER = 'spaCy'
        self.translator = quepy.install('neuroarch_nlp.quepy_analysis')
        self.translate = self.translator.get_query

    def nlp_query( self, nl_string, user='test', format_type=None, spell_correct=True ):
        """ Process an input NL string. Attempt to translate it to NeuroArch-speak.
            The translator assumes 'morphology' is the default output format,
            but if the user inputs a specific format (i.e. outside of the NL query),
            then that setting will be considered "disambiguating" and will be used.
        """
        nl_string = nl_string.strip()

        if spell_correct:
            nl_string = self.correct_spelling( nl_string )
            if nl_string == '':
                return { 'user': user, 'format': format_type }

        # The target and metadata (1st and 3rd returned value) from quepy are ignored
        _, na_query, _ = self.translate( nl_string )

        if na_query:
            na_query[ 'user' ] = user
            if format_type:
                na_query[ 'format' ] = format_type
            return na_query
        else:
            return {}

    def correct_spelling( self, nl_string ):
        """ Perform basic spelling correction. Input is tokenized by whitespace, and an edit distance
            is computed for each token that is not an integer or hexidecimal value corresponding to
            a RGB color encoding.:w
            """
        # NOTE: Currently, we're doing spelling-correction before any other step
        #       (e.g. tokenization, lemmatization). TODO: This will likely change.
        corr_words = []
        # NOTE: Spaces will impact this whitespace-based tokenization + correction.
        for word in simple_tokens.findall( nl_string ):
            # NOTE: (Incorrectly-entered) numbers will throw this off.
            if digit_or_rgbhex.match( word ): # For, e.g. "Undo previous 5" or colors in RGB hexidemical
                corr_words.append( word )
            else:
                # NOTE: score_cutoff is a parameter that could be tweaked.
                corr_word = process.extractOne( word.lower(), na_unigrams, scorer=fuzz.ratio, score_cutoff=80 )
                if corr_word:
                    corr_words.append( corr_word[0] )  # [0] is the word, [1] is its score
                    # NOTE: We drop words that are not in our "dictionary"
        return ' '.join( corr_words )

Translator = PrototypeBaselineTranslator
