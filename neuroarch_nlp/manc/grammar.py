import re
from refo import Plus, Question, Star, Group, Predicate
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate
import logging
log = logging.getLogger('neuroarch_nlp.manc.grammar')

from .defaults import neuropils as raw_neuropils, arborization_regions as raw_arborization_regions, \
    subregions, neuron_types

from ..data import colors_values, transmitters, localities, synapticities, \
                   ownerinstances, othermods

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
              list(transmitters.items()) + list(neuron_types.items()) + list(localities.items())
            + list(synapticities.items()) + list(ownerinstances.items()) + list(othermods.items()) }

# For the grammar, we format the neuropils as a dict, mapping individual string representations
# to their corresponding DB representation.
neuropils = { string: db_rep
              for db_rep, string_reps in raw_neuropils
              for string in string_reps }

arborization_regions = { string: db_rep
                         for db_rep, string_reps in raw_arborization_regions
                         for string in string_reps }


# "Regions" is used here more generally to apply to neuropils, cartridges, or channels
regions = { k: v for k, v in
            list(neuropils.items()) + list(subregions.items()) }
arbregions = { k: v for k, v in
            list(neuropils.items()) + list(arborization_regions.items()) }

modifiers_and_regions = { k: v for k, v in
                          list(modifiers.items()) + list(regions.items())}

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

# As stated in the README, consider using similarity/distance metrics
# (which could, e.g., be incorporated with Predicate)
action_keywords = {'show', 'list', 'graph', 'visualize', 'display', 'add',
                   'remove', 'hide', 'keep', 'retain', 'pin', 'unpin', 'unhide', 'reveal',
                   'color', 'uncolor', 'varcolor', 'animate', 'unanimate', 'blink', 'unblink'}

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
brainregion_arb = Qu(P('DT')) + R( lowercase_is_in(arbregions) )

in_lem = Qu(L('be')) + (L('in') | L('within') | (L('inside') + Qu(L('of'))) | L('of') | L('from')) + Star(L('both'))

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
                        + brainregion_arb + Star( Qu(P(',')) + (L('and')|L('or'))
                                               + Qu(connections) + brainregion_arb ), 'connections_clause' )

is_connecting = Qu(L('that')) + Qu(L('be')) + Qu(L('have')) + ( L('connect') |  L('connection') | L('accept') | L('project') | L('projection')) + Qu(L('from')) + \
                            G(brainregion_arb + (L('to') | L('and')) + brainregion_arb, 'is_connecting' )
in_quant_conns = P('IN') \
               + G( Qu((L('more') | L('less')) + L('than')) + P('CD') + L('column'), 'conn_quant' )

synapse_type = G( (L('axo-axonic') | L('dendro-dendritic') | L('modulatory') | L('regular')),'synapse_type')
synapse_num_clause = ( Qu( L('with') | (Qu(L('that')) + L('have')) | L( 'connect') ) + \
                G( ((( L('more') | L('less') ) + L('than') ) | L('atleast') | (L('at') + L('least')) | L('atmost') | (L('at') + L('most'))) + P('CD') + \
                Qu(synapse_type) + \
                ( L('synapse') | L('synapsis') | L('connection') | L('synapses') | L('connections') ), 'synapse_num_clause' ))
                # 'synapsis' is to get around with the spacy singular form rule

in_region_list = Star(L('both')) + brainregion2 + Star(
                 (in_lem | (Qu(P(',')) + (L('and') | L('or')) + Qu(L('not')) + Qu(in_lem))) + brainregion2)

clause = expressing_marker | transmitters_clause | connections_clause | is_connecting | synapse_num_clause | synapse_type

clauses = clause + Star(Qu(P(',')) + Qu(L('and') | L('or')) + clause)

synaptic_phrase = G( Qu( L('presynaptic') | L('postsynaptic') )
                   + Qu( Qu(P(',')|L('and')|L('or'))
                   + (L('presynaptic') | L('postsynaptic')) )
                   + L('to')
                   + Qu( universal_quantifier ) + Qu(L('of')) + Qu(P('DT'))
                   + ( (Qu( neuron_modifiers ) + neurons) | (neuron_modifiers + Qu(neurons)) )
                   + Qu( clauses )
                   + Qu( Qu(L('and')|L('or'))
                         + in_lem + G( in_region_list, 'region_list' ) ), 'synaptic_phrase' )

color = R(is_color)

###############################################

from .grammar_semantics import interpret_NeuronsQuery_MoreGeneral, interpret_NeuronsQuery_MoreSpecific, \
    interpret_ColorCommand, interpret_VerbCommand, interpret_ClearAllCommand, \
    interpret_ClearSomeCommand

class NeuronsQuery_MoreSpecific(QuestionTemplate):
    weight = 3

    subquery = G(Qu(opener), 'opener') \
               + Qu(universal_quantifier) + Qu(L('of')) \
               + Qu(L('the') | L('a') | L('an')) \
               + ( (Qu( neuron_modifiers ) + neurons) | (neuron_modifiers + Qu(neurons)) ) \
               + (Qu(synaptic_phrase) + Qu(clauses)) \
               + Qu(Qu(L('and') | L('or')) \
                    + in_lem + G(in_region_list, 'region_list')) + \
               Qu(clauses)

    subqueries = subquery + Star(Qu(P(',')) + (L('and') | L('or')) + subquery)

    regex = subqueries \
            + Qu(G(color, 'color') | G(color, 'varcolor')) \
            + Qu(L('as') + Qu(L('a')) + G(noun, 'formatting')) \
            + Qu(P('.'))

    def interpret(self, match):
        return interpret_NeuronsQuery_MoreSpecific( self, match )

'''
class NeuronsQuery_MoreSpecific2(QuestionTemplate):
    #Should be redundant now
    weight = 2

    subquery = G(Qu(opener), 'opener') \
               + Qu(universal_quantifier) + Qu(L('of')) \
               + Qu(L('the') | L('a') | L('an')) \
               + neuron_modifiers + Qu(neurons)\
               + (Qu(synaptic_phrase) + Qu(clauses)) \
               + Qu(Qu(L('and') | L('or')) \
                    + in_lem + G(in_region_list, 'region_list')) + \
               Qu(clauses)
    subqueries = subquery + Star(Qu(P(',')) + (L('and') | L('or')) + subquery)

    regex = subqueries \
            + Qu(G(color, 'color')) \
            + Qu(L('as') + Qu(L('a')) + G(noun, 'formatting')) \
            + Qu(P('.'))

    def interpret(self, match):
        print 'more specific 2'
        return interpret_NeuronsQuery_MoreSpecific( self, match )

class NeuronsQuery_MoreGeneral(QuestionTemplate):
    """
        e.g. "Show all neurons in the Lamina."
        This is an older class which could benefit from some of the "clauses" above.
    """

    neuron_modifier_list = (P('JJ') | P('NN')) \
                           + Star(Qu(L('and') | P(',')) + (P('JJ') | P('NN')))
    # neuron_modifier_list2 is more in line with what we'd like
    # neuron_modifier_list to be (but cannot currently be because of its context).
    # TODO: Review this.
    neuron_modifier_list2 = adjnoun + Star(Qu(L('and') | P(',')) + adjnoun)

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

    in_lem = L('in') | L('within') | L('inside') | Ls('inside of')
    in_region_list = brainregion + Star(
        ((Qu(P(',')) + L('and') + Qu(L('not')) + Qu(in_lem))
         | (Qu(P(',')) + L('or') + Qu(L('not')) + Qu(in_lem))
         | in_lem) + brainregion)

    clause = expressing_marker | transmitters_clause | connections_clause | in_quant_conns | synapse_num_clause
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
'''

class ColorCommand(QuestionTemplate):
    """
        e.g. Color, Color [color]
    """
    regex = (L('color')|L('varcolor')) + Qu( G( R(is_color), 'color' ) ) + Qu(P('.'))

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
