from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import traceback
import six
import collections

from .quepy_analysis.grammar import modifiers_and_regions, arborization_regions
from .data import colors_values


na_unigrams = { unigram
                for term in list(modifiers_and_regions.keys()) + list(colors_values.keys()) + list(arborization_regions.keys())
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
                     'inputs', 'outputs', 'interneurons', 'innervations', 'cells',
                     'than','atleast','least','at','most','atmost','more','less',
                     'synapse','synapses'])

digit_or_rgbhex = re.compile( r'\b[0-9]+\b|\b(#?[a-fA-F0-9]{1,6})\b' )
simple_tokens = re.compile( r"\b[a-zA-Z0-9_\-']+\b", re.I )
special_char = set("*?+\.()[]|{}^$'")

def replace_special_char(text):
    return ''.join(['\\\\'+s if s in special_char else s for s in text])

def convert(data):
    if isinstance(data, (basestring, str)):
        return six.u(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

class PrototypeBaselineTranslator(object):
    def __init__(self):
        import quepy
        from .quepy_analysis import settings
        settings.PARSER = 'spaCy'
        self.translator = quepy.install('neuroarch_nlp.quepy_analysis')
        self.translate = self.translator.get_query

    def nlp_query( self, nl_string, user='test', format_type=None, spell_correct=True ):
        """ Process an input NL string. Attempt to translate it to NeuroArch-speak.
            The translator assumes 'morphology' is the default output format,
            but if the user inputs a specific format (i.e. outside of the NL query),
            then that setting will be considered "disambiguating" and will be used.
        """
        try:
            reg_exp = None
            query_field = "any('uname', 'name', 'label')"
            if '/r' in nl_string:
                exps = nl_string.split('/r')
                nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
                reg_exp = '/r{}'.format(exps[1])
            elif '$' in nl_string:
                exps = nl_string.split('$')
                nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
                shorthand = replace_special_char(exps[1])
                reg_exp = '/r(.*){}(.*)'.format(shorthand)
            elif '/[' in nl_string:
                tmp = nl_string.split('[')
                exps = [tmp[0]] + tmp[1].split(']')
                nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
                reg_exp = ["{}".format(i.strip()) for i in exps[1].split(',')]
            elif '/:' in nl_string:
                tmp = nl_string.split('/:')
                tmp1 = tmp[1].split(':[')
                query_field = tmp1[0]
                exps = [tmp[0]] + tmp1[1].split(']')
                nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
                reg_exp = ["{}".format(i.strip()) for i in exps[1].split(',')]
            nl_string = nl_string.strip()
            if spell_correct:
                nl_string = self.correct_spelling( nl_string )
                if nl_string == '':
                    return { 'user': user, 'format': format_type }

            # The target and metadata (1st and 3rd returned value) from quepy are ignored
            _, na_query, _ = self.translate( nl_string )

            if reg_exp is not None:
                queries_with_name = []
                neuron_class_queries = []
                state_queries = []
                memory_queries = []
                for i, n in enumerate(na_query['query']):
                    try:
                        if 'query' in n['action']['method']:
                            nn = n['action']['method']['query']
                        elif 'has' in n['action']['method']:
                            nn = n['action']['method']['has']
                        else:
                            continue
                        if 'name' in nn:
                            if 'class' in n['object']:
                                if n['object']['class'] == 'Neuron':
                                    neuron_class_queries.append(i)
                            elif 'state' in n['object']:
                                state_queries.append(i)
                            elif 'memory' in n['object']:
                                memory_queries.append(i)
                    except KeyError:
                        continue

                if len(neuron_class_queries):
                    n = na_query['query'][neuron_class_queries[0]]['action']['method']
                    if 'query' in n:
                        n['query'][query_field] = reg_exp
                        n['query'].pop('name')
                    elif 'has' in n:
                        n['has'][query_field] = reg_exp
                        n['has'].pop('name')
                else:
                    if len(state_queries):
                        n = na_query['query'][state_queries[0]]['action']['method']
                        if 'query' in n:
                            n['query'][query_field] = reg_exp
                            n['query'].pop('name')
                        elif 'has' in n:
                            n['has'][query_field] = reg_exp
                            n['has'].pop('name')
                    elif len(memory_queries):
                        n = na_query['query'][memory_queries[0]]['action']['method']
                        if 'query' in n:
                            n['query'][query_field] = reg_exp
                            n['query'].pop('name')
                        elif 'has' in n:
                            n['has'][query_field] = reg_exp
                            n['has'].pop('name')

            if na_query:
                na_query[ 'user' ] = user
                if format_type:
                    na_query[ 'format' ] = format_type
                na_query1 = convert(na_query)
                return na_query1
            else:
                return {}
        except Exception as e:
            traceback.print_exc()
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
                # NOTE: Original implementation dropped words that are not in our "dictionary"
                else:
                    corr_words.append(word.lower())
        return ' '.join( corr_words )

# Currently included for compatibility with existing FFBO architecture. Likely to change.
Translator = PrototypeBaselineTranslator
