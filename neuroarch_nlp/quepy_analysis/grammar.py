import re
from refo import Plus, Question, Star, Group, Predicate
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate
import logging
log = logging.getLogger('neuroarch_nlp.quepy_analysis.grammar')

from ..data import neuropils as raw_neuropils, subregions, colors_values, transmitters, neuron_types, \
                   localities, synapticities, ownerinstances, othermods

# NOTE: In general, this code is very much "under construction": there are known bugs,
#       it is incomplete, and it can be more efficient (and easier for a human to interpret).

# We use these aliases in hopes to make the grammar a bit easier on human eyes.
L = Lemma
Ls = Lemmas
P = Pos
Qu = Question
G = Group
R = Predicate

# NOTE: You should add other ("non-transmitter") modifiers to this "modifiers" dict, as necessary.
modifiers = { k: v for k, v in
              transmitters.items() + neuron_types.items() + localities.items()
            + synapticities.items() + ownerinstances.items() + othermods.items() }

# For the grammar, we format the neuropils as a dict, mapping individual string representations
# to their corresponding DB representation.
neuropils = { string: db_rep
              for db_rep, string_reps in raw_neuropils
              for string in string_reps }
# "Regions" is used here more generally to apply to neuropils, cartridges, or channels
regions = { k: v for k, v in
            neuropils.items() + subregions.items() }

modifiers_and_regions = { k: v for k, v in
                          modifiers.items() + regions.items() }

notneurons = Plus( R(lambda token: token is not None
                               and token.lemma not in {'neuron', 'interneuron', 'interneurons'}
                               and token.token.lower() not in modifiers
                               and token.pos in ['JJ', 'NN', 'NNS', 'NNP', 'NNPS']) )

rgb_pattern = re.compile('#?[a-f0-9]{1,6}')  # NOTE: This assumes lower-case only.

def is_color( token ):
    if token is None:
        return False
    else:
        tokenlower = token.token.lower()
        return tokenlower in colors_values or rgb_pattern.match( tokenlower ) is not None

def lowercase_is_in(things):
    return lambda token: token is not None and token.token.lower() in things

def list_of(things):
    thing_seq = Plus(R(lowercase_is_in(things)))
    return thing_seq + Star(Qu(P(',')) + Qu(L('and') | L('or')) + thing_seq)

#################################################################
# The meat of the grammar:

# General notes about the grammar:
# - Some lemma tokens are explicitly used, e.g. in place of POS tokens,
#   because the taggers we've used sometimes incorrectly label POS, etc.
# - The computed lemmas for the raw input may also be incorrect,
#   so multiple lemmas may be listed (e.g. "interneuron" and "interneurons")

noun = P('NN') | P('NNS') | P('NNP') | P('NNPS')
adjnoun = P('JJ') | noun
nouns = Plus(noun)
adjnouns = Plus(adjnoun)

action_keywords = {'show', 'list', 'graph', 'visualize', 'display', 'add',
                   'remove', 'hide', 'keep', 'retain', 'pin', 'unpin', 'unhide',
                   'color', 'uncolor', 'animate', 'unanimate', 'blink', 'unblink'}

# TODO: Consider using a similarity/distance metric (which could, e.g., be incorporated with Predicate)
action_keyword = R( lambda token: token is not None and token.lemma in action_keywords )

opener = Ls('what be') | ((P('VB') | action_keyword) + Qu(Qu(L('for')) + L('me')))

universal_quantifier = L('all') | L('every') | L('each')

neuron_modifiers = G(list_of(modifiers_and_regions), 'neuron_modifiers')

neurons = G( L('neuron') | L('interneuron') | L('interneurons') | L('cell'), 'neurons' )

# NOTE: We don't yet have a (hard-coded, at least) list of supported genetic markers yet,
#       so this is largely unused.
expressing_marker = L('express') + G(nouns, 'expressing_marker')

transmitters_clause = ( ( Qu(L('that')|L('which')) + (L('transmit')|L('release')) )
                        | ( ((Qu(L('that')) + L('have')) | L('with'))
                            + Qu(L('transmitter') | L('neurotransmitter'))) ) \
                    + G( list_of(transmitters), 'transmitters' )

brainregion = Qu(P('DT')) + notneurons
brainregion2 = Qu(P('DT')) + R( lowercase_is_in(regions) )

in_lem = Qu(L('be')) + (L('in') | L('within') | (L('inside') + Qu(L('of'))) | L('of') | L('from'))

connection_cnoun = ( Qu(L('synaptic')) + L('connection') ) \
                 | ( L('dendrite') | L('axon') | L('process') | L('input') | L('output') ) \
                 | ( Qu( L('dendritic') | L('axonic') | L('axon') | L('axonal') )
                     + ( L('arborization') | L('arborizations') | L('innervation') ) )

connections = ( Qu( L('with') | (Qu(L('that')) + L('have')) )
              + connection_cnoun + in_lem ) \
            | ( Qu(L('that') | L('which')) + (L('innervate') | L('arborize')) + Qu(in_lem) )

connections_clause = G( ( ( ( L('with') | (Qu(L('that')) + L('have')) )
                            + connection_cnoun + in_lem )
                          | ( Qu(L('that') | L('which')) + (L('innervate') | L('arborize')) + Qu(in_lem) ) )
                        + brainregion2 + Star( Qu(P(',')) + (L('and')|L('or'))
                                               + Qu(connections) + brainregion2 ), 'connections_clause' )

is_connecting = Qu(L('that')) + Qu(L('be')) + L('connect') + G(
                brainregion2 + (L('to') | L('and')) + brainregion2, 'is_connecting' )

in_quant_conns = P('IN') \
               + G( Qu((L('more') | L('less')) + L('than')) + P('CD') + L('column'), 'conn_quant' )

in_region_list = brainregion2 + Star(
                 (in_lem | (Qu(P(',')) + (L('and') | L('or')) + Qu(L('not')) + Qu(in_lem))) + brainregion2)

clause = expressing_marker | transmitters_clause | connections_clause | is_connecting | in_quant_conns

clauses = clause + Star(Qu(P(',')) + Qu(L('and') | L('or')) + clause)

synaptic_phrase = G( Qu( L('presynaptic') | L('postsynaptic') )
                   + Qu( Qu(P(',')|L('and')|L('or'))
                         + (L('presynaptic') | L('postsynaptic')) )
                   + L('to')
                   + Qu( universal_quantifier ) + Qu(L('of')) + Qu(P('DT'))
                   + Qu( neuron_modifiers )
                   + neurons
                   + Qu( clauses )
                   + Qu( Qu(L('and')|L('or'))
                         + in_lem + G( in_region_list, 'region_list' ) ), 'synaptic_phrase' )

color = R(is_color)

# End grammar work.
###############################################

# Possibilities:
# * Consider using a similarity/distance metric (which could, e.g., be incorporated with Predicate)
#   This could be useful for, e.g. detecting the "(action) verbs" that indicate user imperatives
# * Support conjunctions and disjunctions, in general
# * Support negations
# * Support grouping (e.g. via parentheses) in user input
#   e.g. "Show ((l1 and columnar) or gabaergic) neurons"
# * Support different verbs per subquery
#   e.g. "Add [subquery] and remove [subquery]"
#   Though keep in mind that, for such a query, the 'and' is not a logical 'and'.
#   This could also include
# * Support multiple formats per subquery


from .grammar_semantics import interpret_NeuronsQuery_MoreGeneral, interpret_NeuronsQuery_MoreSpecific, \
    interpret_ColorCommand, interpret_VerbCommand, interpret_ClearAllCommand, \
    interpret_ClearSomeCommand

class NeuronsQuery_MoreSpecific(QuestionTemplate):
    weight = 3

    subquery = G(Qu(opener), 'opener') \
               + Qu(universal_quantifier) + Qu(L('of')) \
               + Qu(L('the') | L('a') | L('an')) \
               + Qu(neuron_modifiers) + neurons \
               + (Qu(synaptic_phrase) + Qu(clauses)) \
               + Qu(Qu(L('and') | L('or')) \
                    + in_lem + G(in_region_list, 'region_list'))

    subqueries = subquery + Star(Qu(P(',')) + (L('and') | L('or')) + subquery)

    regex = subqueries \
            + Qu(G(color, 'color')) \
            + Qu(L('as') + Qu(L('a')) + G(noun, 'formatting')) \
            + Qu(P('.'))

    def interpret(self, match):
        return interpret_NeuronsQuery_MoreSpecific( self, match )

class NeuronsQuery_MoreSpecific2(QuestionTemplate):
    weight = 2

    subquery = G(Qu(opener), 'opener') \
               + Qu(universal_quantifier) + Qu(L('of')) \
               + Qu(L('the') | L('a') | L('an')) \
               + neuron_modifiers \
               + (Qu(synaptic_phrase) + Qu(clauses)) \
               + Qu(Qu(L('and') | L('or')) \
                    + in_lem + G(in_region_list, 'region_list'))

    subqueries = subquery + Star(Qu(P(',')) + (L('and') | L('or')) + subquery)

    regex = subqueries \
            + Qu(G(color, 'color')) \
            + Qu(L('as') + Qu(L('a')) + G(noun, 'formatting')) \
            + Qu(P('.'))

    def interpret(self, match):
        return interpret_NeuronsQuery_MoreSpecific( self, match )

class NeuronsQuery_MoreGeneral(QuestionTemplate):
    """
        e.g. "Show all neurons in the Lamina."
    """

    neuron_modifier_list = (P('JJ') | P('NN')) \
                           + Star(Qu(L('and') | P(',')) + (P('JJ') | P('NN')))
    # neuron_modifier_list2 is named as such because it's more in line with what we'd like
    # neuron_modifier_list to be (but cannot currently be because of its context).
    neuron_modifier_list2 = adjnoun + Star(Qu(L('and') | P(',')) + adjnoun)

    # TODO: Use this
    neuron_name_list = (P('NNP') | P('NN')) \
                       + Star(Qu(L('and') | P(',')) + (P('NNP') | P('NN')))

    expressing_marker = L('express') + G(nouns, 'expressing_marker')

    transmitters_clause = \
        ((Qu(L('that') | L('which')) + (L('transmit') | L('release'))) |
         (L('have') + Qu(L('transmitter') | L('neurotransmitter')))) + \
        G(neuron_modifier_list2, 'transmitters')

    connections_clause = \
        ((L('with') | L('have'))
         + ((Qu(L('synaptic')) + L('connection'))
            | L('dendrite') | L('axon') | L('arborization') | L('arborizations')
            | L('process'))) \
        | L('arborize')

    in_quant_conns = P('IN') + G(Qu((L('more') | L('less'))
                                    + L('than')) + P('CD') + L('column'), 'conn_quant')

    brainregion = Qu(P('DT')) + notneurons

    in_lem = L('in') | L('within') | L('inside') | Ls('inside of')
    in_region_list = brainregion + Star(
        ((Qu(P(',')) + L('and') + Qu(L('not')) + Qu(in_lem))
         | (Qu(P(',')) + L('or') + Qu(L('not')) + Qu(in_lem))
         | in_lem) + brainregion)

    clause = expressing_marker | transmitters_clause | connections_clause | in_quant_conns
    clauses = clause + Star(Qu(P(',')) + Qu(L('and') | L('or')) + clause)

    subquery = G(Qu(opener), 'opener') \
               + Qu(universal_quantifier) + Qu(P('DT')) \
               + G(Qu(neuron_modifier_list), 'neuron_modifiers') \
               + G(Qu(P('NNP')), 'neuron_name') \
               + neurons \
               + Qu(clauses) \
               + Qu(in_lem + G(in_region_list, 'region_list'))

    subqueries = subquery + Star(Qu(P(',')) + (L('and') | L('or')) + subquery)
    subqueries = G(subqueries, 'subqueries')
    regex = subqueries \
          + G(Qu(L('as') + Qu(L('a')) + noun), 'formatting') + Qu(P('.'))

    def interpret(self, match):
        return interpret_NeuronsQuery_MoreGeneral( self, match )


class ColorCommand(QuestionTemplate):
    """
        e.g. Color, Color [color]
    """

    regex = L('color') + Qu( G( R(is_color), 'color' ) ) + Qu(P('.'))

    def interpret( self, match ):
        return interpret_ColorCommand( self, match )


class VerbCommand(QuestionTemplate):
    """ For other "(action) verbs" when no parameters are specified.
    """
    regex = G( L('pin') | L('unpin') | L('blink') | L('unblink')
                   | L('animate') | L('unanimate'), 'verb' ) + Qu(P('.'))

    def interpret( self, match ):
        return interpret_VerbCommand( self, match )


class ClearAllCommand(QuestionTemplate):
    """
        e.g. Restart, Clear, Clear all
    """

    regex = (L('restart') | L('clear')) + Qu( L('all') ) + \
            Qu( P('.') )

    def interpret( self, match ):
        return interpret_ClearAllCommand( self, match )


class ClearSomeCommand(QuestionTemplate):
    """
        e.g.
        Undo (previous|last)? [AMOUNT]?
        Clear (previous|last) [AMOUNT]?
    """

    prev_or_last = L('previous') | L('last')

    regex = ( (L('undo') + Qu(prev_or_last))
              | (L('clear') + prev_or_last) ) \
            + G( Qu( P('CD') ), 'clear_quant' ) \
            + Qu( P('.') )

    def interpret( self, match ):
        return interpret_ClearSomeCommand( self, match )
