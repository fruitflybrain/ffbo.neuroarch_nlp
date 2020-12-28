from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import traceback
import six
import collections
import importlib
import quepy

from .data import colors_values


# This is for (the temporary) spelling-correction. It, in part, results in a model that performs
# spelling correction on words not found in its (current--at time of writing) grammar.
na_unigrams = {'to', 'in', 'show', 'display', 'hide', 'remove', 'pre', 'post', 'synaptic',
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
                     'from', 'keep', 'retain', 'color', 'uncolor', 'varcolor', 'pin', 'unpin', 'blink',
                     'unblink', 'animate', 'unanimate', 'unhide',
                     'connections', 'axons', 'dendrites', 'neurons', 'arborizations',
                     'inputs', 'outputs', 'interneurons', 'innervations', 'cells',
                     'than','atleast','least','at','most','atmost','more','less',
                     'synapse','synapses'}

digit_or_rgbhex = re.compile( r'\b[0-9]+\b|\b(#?[a-fA-F0-9]{1,6})\b' )
simple_tokens = re.compile( r"\b[a-zA-Z0-9_\-']+\b", re.I )
special_char = set("*?+\.()[]|{}^$'")
closing = {'$': '$', '/r': '/r', '/[': ']', '/:': ']'}

def replace_special_char(text):
    return ''.join(['\\\\'+s if s in special_char else s for s in text])

def convert(data):
    # TODO: Still in py2
    if isinstance(data, (basestring, str)):
        if isinstance(data, unicode):
            return data
        else:
            return six.u(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

class PrototypeBaselineTranslator(object):
    def __init__(self, app_name):
        settings = importlib.import_module('neuroarch_nlp.{}.settings'.format(app_name))
        grammar = importlib.import_module('neuroarch_nlp.{}.grammar'.format(app_name))
        modifiers_and_regions = grammar.modifiers_and_regions
        arborization_regions = grammar.arborization_regions

        self.na_unigrams = { unigram
                        for term in list(modifiers_and_regions.keys()) + list(colors_values.keys()) + list(arborization_regions.keys())
                        for unigram in term.split() }
        self.na_unigrams.update(na_unigrams)

        settings.PARSER = 'spaCy'
        self.translator = quepy.install('neuroarch_nlp.{}'.format(app_name)) #quepy.install('neuroarch_nlp.quepy_analysis')
        self.translate = self.translator.get_query

    def nlp_query( self, nl_string, user='test', format_type=None, spell_correct=True ):
        """ Process an input NL string. Attempt to translate it to NeuroArch-speak.
            The translator assumes 'morphology' is the default output format,
            but if the user inputs a specific format (i.e. outside of the NL query),
            then that setting will be considered "disambiguating" and will be used.
        """
        try:
            # reg_exp = None
            # query_field = 'any()'
            # if '/r' in nl_string:
            #     exps = nl_string.split('/r')
            #     nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
            #     reg_exp = '/r{}'.format(exps[1])
            # elif '$' in nl_string:
            #     exps = nl_string.split('$')
            #     nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
            #     shorthand = replace_special_char(exps[1])
            #     reg_exp = '/r(.*){}(.*)'.format(shorthand)
            # elif '/[' in nl_string:
            #     tmp = nl_string.split('[')
            #     exps = [tmp[0]] + tmp[1].split(']')
            #     nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
            #     reg_exp = ["{}".format(i.strip()) for i in exps[1].split(',')]
            # elif '/:' in nl_string:
            #     tmp = nl_string.split('/:')
            #     tmp1 = tmp[1].split(':[')
            #     query_field = tmp1[0]
            #     exps = [tmp[0]] + tmp1[1].split(']')
            #     nl_string = ''.join([exp if i != 1 else 'regex' for i, exp in enumerate(exps)])
            #     reg_exp = ["{}".format(i.strip()) for i in exps[1].split(',')]
            # nl_string = nl_string.strip()
            a = nl_string
            signs = [(i, a[i] if a[i] in ['$',']'] else a[i:i+2]) \
                     for i in range(len(a)) if a[i] == '$' or \
                                               a[i:].startswith('/r') or \
                                               a[i:].startswith('/[') or \
                                               a[i:].startswith('/:') or \
                                               a[i] == ']']
            current = None
            new_exp = ''
            last = -1
            count = 0
            reg_dict = {}
            for k, (i, sign) in enumerate(signs):
                if current is None:
                    current = sign
                    new_exp += a[last+1:i]
                    last = i
                    continue
                else:
                    if sign == closing[current]:
                        new_exp += ' regex{} '.format(count)
                        reg_dict['regex{}'.format(count)] = {}
                        if current == '/:':
                            s = a[last:i+1]
                            reg_dict['regex{}'.format(count)]['query_field'] = s[2:].split(':')[0]
                            reg_dict['regex{}'.format(count)]['reg_exp'] = \
                                ["{}".format(ss.strip()) for ss in s[2:].split(':[')[1][:-1].split(',')]
                            last = i
                        else:
                            s = a[last:i+1]
                            reg_dict['regex{}'.format(count)]['query_field'] = 'any()'
                            if current == '/r':
                                reg_dict['regex{}'.format(count)]['reg_exp'] = '/r{}'.format(s[2:-1])
                                last = i+1
                            elif current == '$':
                                reg_dict['regex{}'.format(count)]['reg_exp'] = '/r(.*){}(.*)'.format(s[1:-1])
                                last = i
                            elif current == '/[':
                                reg_dict['regex{}'.format(count)]['reg_exp'] = ["{}".format(i.strip()) for i in s[2:-1].split(',')]
                                last = i
                        count += 1
                    else:
                        continue
                    current = None
            new_exp += a[last+1:]
            nl_string = new_exp
            if spell_correct:
                nl_string = self.correct_spelling( nl_string )
                if nl_string == '':
                    return { 'user': user, 'format': format_type }

            # The target and metadata (1st and 3rd returned value) from quepy are ignored
            _, na_query, _ = self.translate( nl_string )

            if count > 0:
                for i, n in enumerate(na_query['query']):
                    try:
                        if 'query' in n['action']['method']:
                            nn = n['action']['method']['query']
                        elif 'has' in n['action']['method']:
                            nn = n['action']['method']['has']
                        else:
                            continue
                        if 'uname' in nn:
                            if nn['uname'].startswith('regex'):
                                regex_number = nn.pop('uname')
                                nn[reg_dict[regex_number]['query_field']] = reg_dict[regex_number]['reg_exp']
                    except KeyError:
                        continue
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
                corr_word = process.extractOne( word.lower(), self.na_unigrams, scorer=fuzz.ratio, score_cutoff=80 )
                if corr_word:
                    corr_words.append( corr_word[0] )  # [0] is the word, [1] is its score
                # NOTE: Original implementation dropped words that are not in our "dictionary"
                else:
                    corr_words.append(word.lower())
        return ' '.join( corr_words )

# Currently included for compatibility with existing FFBO architecture. Likely to change.
Translator = PrototypeBaselineTranslator
