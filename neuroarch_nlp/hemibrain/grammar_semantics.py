from refo import Question, finditer, Predicate
from quepy.parsing import Lemma, Lemmas, Pos
import logging
log = logging.getLogger('neuroarch_nlp.hemibrain.grammar_semantics')

#from .dsl import *
from .dsl import IsAttribute, HasKey, HasValue, IsSynapticConnection, PresynapticTo, PresynapticToState, \
    PostsynapticTo, PostsynapticToState, IsOwnerInstance, HasInstance, IsBrainRegion, \
    HasClass, HasName, IsNeuronModifier, IsNeuron, IsOrOp, IsAndOp, HasPart, \
    OwnedBy, HasSubregion, IsGeneticMarker, HasGeneticMarker, IsNumConnections, \
    HasMoreThan, HasLessThan, HasEqualTo, HasConnectionsTarget, HasType, HasRegion, \
    FromRegion, ToRegion, IsConnection, Has, HasConnections, HasVerb, HasColor, HasFormat, \
    IsCommand, IsNumSynapses, HasAtLeast, HasAtMost
from .grammar import neuron_types, synapticities, localities, transmitters, modifiers, \
                     neuropils, regions, lowercase_is_in, adjnoun, notneurons, modifiers_and_regions, colors_values, \
                     subregions, arborization_regions, arbregions#,ownerinstances

syn_num = None

def get_name_expression( name, syn_to=None ):
    """ Map a given string (`name`) to a particular "semantic abstract syntax tree" (SAST) element.
        The SAST element is given as a Quepy Expression.
    """
    #print name
    if name in transmitters:  # TODO: self.transmitters?
        # TODO: Consider using "IsNeurotransmitter" as a class (in the DSL).
        expr = IsAttribute() + HasKey('Transmitters') + HasValue( modifiers[name] )
    elif name in neuron_types:
        expr = IsAttribute() + HasKey('name') + HasValue( modifiers[name] )
    elif name in synapticities:
        expr = IsSynapticConnection()
        #print "syn_num", syn_num
        if name == 'presynaptic':
            if syn_to is None:
                expr += PresynapticToState('0')
            else:
                expr += PresynapticTo(syn_to)
        elif name == 'postsynaptic':
            if syn_to is None:
                expr += PostsynapticToState('0')
            else:
                expr += PostsynapticTo(syn_to)
        if syn_num: expr+=syn_num
    elif name in localities:
        expr = IsAttribute() + HasKey('locality') + HasValue( modifiers[name] )
        '''elif name in ownerinstances:
        # TODO: This is a pretty hokey representation. Change it.
        expr = IsOwnerInstance() + HasInstance( ownerinstances[name] )'''
    elif name in neuropils:
        expr = IsBrainRegion() + HasClass('Neuropil') + HasName(neuropils[name])
        '''#Specific Subregions
        elif name in ['single cartridge', 'home cartridge']:
        expr = IsBrainRegion() + HasClass('Cartridge') + HasName('home')
        elif name == 'channel':
        expr = IsBrainRegion() + HasClass('Neuropil') + HasName('channel')'''
    #Subregions
    elif name in subregions:
        expr = IsBrainRegion()
        if subregions[name][0]:
            expr+=HasClass(subregions[name][0])
        if subregions[name][1]:
            expr+=HasInstance(subregions[name][1])
        if subregions[name][2]:
            expr+=HasName(subregions[name][2])
    elif name in arborization_regions:
        expr = IsBrainRegion()
        expr += HasName(arborization_regions[name])
    else:
        # NOTE: This is basically a catch-all, and the generated expression
        #       is unlikely to be useful. Raise an exception, and/or log this?
        expr = IsNeuronModifier() + HasName(name)
    return expr

def get_region_owner(wordlist, region_indicator):
    """ Given a list of tokens (as Quepy Words), return a SAST (sub-)tree
        representing the containment relations (and any connectives)
        between the regions in the list (as identified by region_indicator).
    """
    #print "get_region_owner wordlist", wordlist
    #print "get_region_owner region_indicator", region_indicator

    # NOTE: This treats ands/ors as binary operators.
    tokenlist = [x.token.lower() for x in wordlist]
    if 'and' in tokenlist:
        andidx = tokenlist.index('and')
        # NOTE: We currently treat 'and's as disjunctions
        return IsOrOp() \
             + HasPart( get_region_owner(wordlist[0:andidx], region_indicator) ) \
             + HasPart( get_region_owner(wordlist[andidx + 1:], region_indicator) )
    elif 'or' in tokenlist:
        oridx = tokenlist.index('or')
        return IsOrOp() \
             + HasPart( get_region_owner(wordlist[0:oridx], region_indicator) ) \
             + HasPart( get_region_owner(wordlist[oridx + 1:], region_indicator) )
    else:
        if tokenlist[0] == 'in':
            wordlist = wordlist[1:]
        previous_region = None
        for n in finditer(Question(Lemma('not')) + region_indicator, wordlist):
            r, s = n.span()
            region_name = ' '.join([comp.token for comp in wordlist[r:s]]).lower()
            current_region = get_name_expression(region_name)

            if previous_region:
                current_region = current_region + HasSubregion(previous_region)
            previous_region = current_region
        return previous_region

def build_mod_tree(wordlist, synaptic_to):
    """ Given a list of tokens (as Quepy Words), return a SAST (sub-)tree
        representing the detected neuron attributes ("modifiers")
        and any connectives.
        synaptic_to represents the phrase which this sequence is "(pre-/post-)synaptic to".
    """
    #print "build_mod_tree wordlist", wordlist
    #print "build_mod_tree synaptic_to", synaptic_to
    tokenlist = [x.token.lower() for x in wordlist]
    # We make multiple passes, but "hopefully" the modifier list is not that long.
    for idx, token in enumerate(tokenlist):
        if (token == 'and' or token == 'or') and len(tokenlist) > idx + 2:
            # NOTE: We assume something would come after the following 'and'/'or'.
            if tokenlist[idx + 2] == 'and':
                # NOTE: We currently treat 'and's as disjunctions
                return IsOrOp() \
                     + HasPart( build_mod_tree(wordlist[0:idx + 2], synaptic_to) ) \
                     + HasPart( build_mod_tree(wordlist[idx + 3:], synaptic_to) )
            elif tokenlist[idx + 2] == 'or':
                return IsOrOp() \
                     + HasPart( build_mod_tree(wordlist[0:idx + 2], synaptic_to) ) \
                     + HasPart( build_mod_tree(wordlist[idx + 3:], synaptic_to) )
    # If no such ("explicit") 'and'/'or' nodes are found, look for "silent and" nodes.
    for idx, token in enumerate(tokenlist):
        if (token == 'and' or token == 'or') and len(tokenlist) > idx + 2:
            # Based on the scan above, we can assume the idx+2 is not 'and'/'or'.
            # So we treat it as a "silent and".
            return IsAndOp() \
                 + HasPart( build_mod_tree(wordlist[0:idx + 2], synaptic_to) ) \
                 + HasPart( build_mod_tree(wordlist[idx + 2:], synaptic_to) )
    # If we've made it this far, we can assume there's zero or one 'and'/'or's.
    mods = []
    for n in finditer(Predicate(lowercase_is_in(modifiers_and_regions)), wordlist):
        r, s = n.span()
        mod_name = tokenlist[r:s][0]
        mods.append(mod_name)
    if len(mods) == 1:
        return get_name_expression(mods[0], synaptic_to)
    # NOTE: (A reminder..:) We assume 'and'/'or' are not biologically relevant terms...
    # NOTE: We currently treat 'and's as disjunctions
    if 'or' in tokenlist or 'and' in tokenlist:
        op = IsOrOp()
    else:
        # NOTE: We assume juxtaposition of modifiers signifies logical 'and'
        op = IsAndOp()
    for mod in mods:
        op += HasPart(get_name_expression(mod, synaptic_to))
    return op

def interpret_NeuronsQuery_MoreSpecific(self, match):
    # NOTE: If a subquery has a prepositional phrase attached (e.g. "in [regions]"),
    #       then we should see if the preceding subqueries lack a prepositional phrase.
    #       By default, attach the prep. phrase to the preceding subqueries as well.
    #       But we'd prefer to alert the user and have them check this.
    # subquery_list is a list of tuples, where the first element is the Expression tree (SAST)
    # and the second element contains the sub-tree corresponding to any owned_by region(s)
    #print "interpret_NeuronsQuery_MoreSpecific", match._words, match.words, match._particles
    global syn_num
    syn_num = None
    subquery_list = []
    for mtch in finditer(self.subquery, match.words):
        i, j = mtch.span()
        #for x in mtch.state:
        #    print x, mtch.state[x]
        def get_subquery(m, matchwords):
            neuron = IsNeuron() + HasClass('Neuron')
            owned_region = None
            global syn_num
            #print matchwords
            #print m.state
            if 'synapse_num_clause' in m:
                p, q = m['synapse_num_clause']
                conn_quant_words = matchwords[p:q]
                # TODO: Perform a search instead of finditer
                for n in finditer(Pos("CD"), conn_quant_words):
                    r, s = n.span()
                    conn_num = ' '.join([c.token for c in conn_quant_words[r:s]])
                    moreorless = False  # See above...
                    for o in finditer(Lemmas("more than"), conn_quant_words):
                        syn_num = HasMoreThan(conn_num)
                        moreorless = True
                    for o in finditer(Lemmas("less than"), conn_quant_words):
                        syn_num =  HasLessThan(conn_num)
                        moreorless = True
                    for o in finditer(Lemma("atleast"), conn_quant_words):
                        syn_num = HasAtLeast(conn_num)
                        moreorless = True
                    for o in finditer(Lemma("atmost"), conn_quant_words):
                        syn_num =  HasAtMost(conn_num)
                        moreorless = True
                    for o in finditer(Lemmas("at least"), conn_quant_words):
                        syn_num = HasAtLeast(conn_num)
                        moreorless = True
                    for o in finditer(Lemmas("at most"), conn_quant_words):
                        syn_num = HasAtMost(conn_num)
                        moreorless = True

                    if not moreorless:
                        syn_num = HasEqualTo(conn_num)
                #print "syn_num", syn_num
            # The (sub-)subquery which this subquery is "(pre-/post-)synaptic to".
            synaptic_to = None
            if 'synaptic_phrase' in m:
                p, q = m['synaptic_phrase']
                synaptic_phrase = matchwords[p:q]

                # TODO: Clean this up.
                spl = [w.lemma.lower() for w in synaptic_phrase]
                to_idx = spl.index('to')
                syn_type = set()
                or_syns = False
                if 'presynaptic' in spl[:to_idx]:
                    syn_type.add('presynaptic')
                if 'postsynaptic' in spl[:to_idx]:
                    syn_type.add('postsynaptic')
                if 'or' in spl[:to_idx]:
                    or_syns = True

                # NOTE: We currently only support one subquery here, anyway.
                for n in finditer(self.subquery, synaptic_phrase[to_idx + 1:]):
                    r, s = n.span()
                    synaptic_to, _ = get_subquery(n, synaptic_phrase[to_idx + 1:])
                if 'presynaptic' in syn_type:
                    neuron += PresynapticTo(synaptic_to)
                elif 'postsynaptic' in syn_type:
                    neuron += PostsynapticTo(synaptic_to)
                if syn_num: neuron += syn_num
                # This is basically just a trick to update the existing ("parent") subquery.
                # TODO: Clean this up.
                for m in finditer(self.subquery, matchwords[:p]):
                    break

            if 'region_list' in m:
                p, q = m['region_list']
                owned_region = get_region_owner( matchwords[p:q], Predicate(lowercase_is_in(regions)) )
                neuron = neuron + OwnedBy(owned_region)

            # We identify transmitters and neuron types with the "has" relation (e.g. in the SAST)
            # so to support conjunctions/disjunctions of these modifiers, while also keeping the SAST
            # "simple" with at most one "has" relation per node, we calculate the "has" relations later
            has_modifiers = []
            if 'neuron_modifiers' in m:
                p, q = m['neuron_modifiers']
                modifiers_words = [x for x in matchwords[p:q] if x.pos != ',']

                has_modifiers.append( build_mod_tree(modifiers_words, synaptic_to) )
            if 'transmitters' in m:
                p, q = m['transmitters']
                modifiers_words = [x for x in matchwords[p:q] if x.pos != ',']

                has_modifiers.append( build_mod_tree(modifiers_words, synaptic_to) )
            if 'neurons' in m:
                p, q = m['neurons']
                # NOTE: We assume that this can only be "interneuron(s)" or "neuron(s)"
                if 'interneuron' in ''.join([x.lemma for x in matchwords[p:q]]):
                    has_modifiers.append(IsAttribute() + HasKey('locality') + HasValue('True'))
            else:
                # NOTE: For now, we assume that a neuron 'name/type' (and not "neuron") is present
                # for n in finditer( Pos("CD"), conn_quant_words ):
                pass
            if 'expressing_marker' in m:
                p, q = m['expressing_marker']
                expressing_lemmas = [x.lemma for x in matchwords[p:q]]

                # This is just a temporary solution--before support for genetic markers is added.
                marker = IsGeneticMarker() + HasName(' '.join(expressing_lemmas))
                neuron = neuron + HasGeneticMarker(marker)
                # TODO: Include this as a 'has' relation (as above)?
            if 'conn_quant' in m:
                # NOTE: This is currently unused by the code generator
                p, q = m['conn_quant']
                conn_quant_words = matchwords[p:q]

                quantdir = IsNumConnections()
                # TODO: Perform a search instead of finditer
                for n in finditer(Pos("CD"), conn_quant_words):
                    r, s = n.span()
                    conn_num = ' '.join([c.token for c in conn_quant_words[r:s]])
                    moreorless = False  # See above...
                    for o in finditer(Lemmas("more than"), conn_quant_words):
                        quantdir = quantdir + HasMoreThan(conn_num)
                        moreorless = True
                    for o in finditer(Lemmas("less than"), conn_quant_words):
                        quantdir = quantdir + HasLessThan(conn_num)
                        moreorless = True
                    if not moreorless:
                        quantdir = quantdir + HasEqualTo(conn_num)
                for n in finditer(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"), conn_quant_words):
                    r, s = n.span()
                    conn_target = ' '.join([c.token for c in conn_quant_words[r:s]])
                    # TODO: Make conn_target.lower() ?
                    quantdir = quantdir + HasConnectionsTarget(conn_target)
                neuron = neuron + HasConnections(quantdir)
            if 'connections_clause' in m:
                p, q = m['connections_clause']
                connections_words = [x for x in matchwords[p:q] if x.pos != ',']
                connectives = []
                segments = [[]]
                seg_idx = 0
                for word in connections_words:
                    if word.lemma.lower() == 'and':
                        connectives.append('and')
                        segments.append([])
                        seg_idx += 1
                        continue
                    if word.lemma.lower() == 'or':
                        connectives.append('or')
                        segments.append([])
                        seg_idx += 1
                        continue
                    segments[seg_idx].append(word)
                # NOTE: We assume that no "segment" list is empty--based on our grammar
                # Scan from left to right in 'connections_clause'
                last_conn_type = None
                region_name = None
                connection_nodes = []
                for segment in segments:
                    # NOTE: The order of these loops (which shouldn't be loops) currently matters.
                    # NOTE: We assume no region has these terms in their name/synonyms.
                    # TODO: Clean this up.
                    for n in finditer(Lemma('connection') | Lemma('process')
                                              | Lemma('arborization') | Lemma('arborizations')
                                              | Lemma('arborize') | Lemma('innervate')
                                              | Lemma('innervation'), segment):
                        last_conn_type = 'arbors'
                        break
                    for n in finditer(Lemma('dendrite') | Lemma('input')
                                              | Lemma('dendritic'), segment):
                        last_conn_type = 'dendriteArbors'
                        break
                    for n in finditer(Lemma('axon') | Lemma('axonal') | Lemma('axonic')
                                              | Lemma('output'), segment):
                        last_conn_type = 'axonArbors'
                        break

                    for n in finditer(Predicate(lowercase_is_in(arbregions)), segment):
                        r, s = n.span()
                        region_name = ' '.join([comp.token for comp in segment[r:s]]).lower()
                        if region_name not in arbregions:
                            log.error('Unknown region name: ' + region_name)
                            # TODO: Handle gracefully.
                        else:
                            region_name = arbregions[region_name]
                            # NOTE: We assume there's exactly one region per segment
                    # NOTE: We assume last_conn_type was set at least initially--based on our grammar
                    conn_region = HasType(last_conn_type)
                    conn_region += HasRegion(region_name)

                    connection_nodes.append(conn_region)

                # NOTE: We assume there is at least one element in connection_nodes
                # NOTE: We assume the number of connectives is one less than len(connection_nodes)
                if len(connection_nodes) == 1:
                    has_modifiers.append(connection_nodes[0])
                else:
                    connective = None
                    if connectives.pop(0) == 'and':
                        connective = IsAndOp() + HasPart(connection_nodes.pop(0)) \
                                     + HasPart(connection_nodes.pop(0))
                    else:
                        connective = IsOrOp() + HasPart(connection_nodes.pop(0)) \
                                     + HasPart(connection_nodes.pop(0))

                    while len(connectives) > 0:
                        if connectives.pop(0) == 'and':
                            connective = IsAndOp() + HasPart(connective) \
                                         + HasPart(connection_nodes.pop(0))
                        else:
                            connective = IsOrOp() + HasPart(connective) \
                                         + HasPart(connection_nodes.pop(0))
                    has_modifiers.append(connective)
            if 'is_connecting' in m:
                p, q = m['is_connecting']
                region_pair = []
                for n in finditer(Predicate(lowercase_is_in(arbregions)), matchwords[p:q]):
                    r, s = n.span()
                    r, s = r + p, s + p  # Get the offset from matchwords
                    region_name = ' '.join([comp.token for comp in matchwords[r:s]]).lower()
                    if region_name not in arbregions:
                        log.error('Unknown region name: ' + region_name)
                        # TODO: Handle gracefully
                    else:
                        region_pair.append(arbregions[region_name])
                # Check that there were exactly two regions. NOTE: This could be enforced by the grammar.
                if len(region_pair) == 2:
                    # NOTE: We assume the first region we parse is the "from" region.
                    if 'and' in [x.lemma for x in matchwords[p:q]]:
                        conn1 = IsConnection() + FromRegion(region_pair[0]) + ToRegion(region_pair[1])
                        conn2 = IsConnection() + FromRegion(region_pair[1]) + ToRegion(region_pair[0])
                        connecting_node = IsOrOp() + HasPart(conn1) + HasPart(conn2)
                    else:
                        # NOTE: We assume 'to' is present
                        connecting_node = IsConnection() + FromRegion(region_pair[0]) + ToRegion(region_pair[1])
                    # NOTE: At least for now, we'll put connections in with the 'has' relations
                    #       but NOTE that this only works if codegen_optimization to true.
                    # neuron += Connecting( connecting_node )
                    has_modifiers.append(connecting_node)
            # Now create a single "has node" for this subquery's neuron.
            if len(has_modifiers) > 1:
                # NOTE: We assume all 'has' objects are "conjuncted together".
                has_node = IsAndOp()
                for mod in has_modifiers:
                    has_node += HasPart(mod)
                neuron += Has(has_node)
            elif len(has_modifiers) == 1:
                neuron += Has(has_modifiers[0])

            return neuron, owned_region

        subquery_list.append(get_subquery(mtch, match.words))

    # We could attach the prep. phrases (e.g. "in [regions]") to previous subqueries
    # only if they don't already have their own prep. phrase.
    """
    subquery_list = subquery_list[::-1]
    prev_ownedby = subquery_list[0][1]
    for i, (subq, ownedby) in enumerate( subquery_list ):
        if prev_ownedby is not None:
            if ownedby is None:
                # TODO: Check that Python is okay with these 'is's and 'not's.
                subquery_list[i][0] += OwnedBy( prev_ownedby )
        else:
            prev_ownedby = ownedby
    """

    if len(subquery_list) == 1:
        final_query = subquery_list[0][0]
    else:
        # NOTE: We currently assume set union across subqueries
        final_query = IsOrOp()
        # NOTE: If prep. phrase attaching, ownedby data should be considered stale at this point;
        #       queries themselves would have been updated with "owned_by" relation info.
        for subq, ownedby in subquery_list:
            final_query += HasPart(subq)

    formatting = None
    # NOTE: We parse queries with an opener for each subquery, but currently only use the last
    if getattr(match, 'opener', None):
        form_lems = match.opener.lemmas
        if 'add' in form_lems:
            final_query += HasVerb('add')
        elif 'remove' in form_lems:
            final_query += HasVerb('remove')
        elif 'keep' in form_lems or 'retain' in form_lems:
            final_query += HasVerb('keep')
        elif 'list' in form_lems:
            formatting = 'information'
        elif 'graph' in form_lems:
            formatting = 'network'
        elif 'unpin' in form_lems:
            final_query += HasVerb('unpin')
        elif 'pin' in form_lems:
            final_query += HasVerb('pin')
        elif 'uncolor' in form_lems:
            final_query += HasVerb('uncolor')
        elif 'color' in form_lems:
            final_query += HasVerb('color')
            # NOTE: We only check for colors if 'color' is the verb
            if getattr(match, 'color', None):
                hue = match.color.lemmas
                if hue in colors_values:
                    hue = colors_values[hue]
                else:
                    # It's hex for a color
                    if hue.startswith('#'):
                        hue = hue[1:]
                    # NOTE: We assume right-most bit of given hex is LSB
                    hue = '0' * (6 - len(hue)) + hue
                final_query += HasColor(hue)
        # Not exactly natural language...
        elif 'unanimate' in form_lems or 'unblink' in form_lems:
            final_query += HasVerb('unblink')
        elif 'animate' in form_lems or 'blink' in form_lems:
            final_query += HasVerb('blink')
        elif 'unhide' in form_lems:
            final_query += HasVerb('unhide')
        elif 'hide' in form_lems:
            final_query += HasVerb('hide')
    # NOTE: "format" group overrides any "opener" group--for formatting
    #       e.g. "List neurons in Lamina as morphology" will use morphology formatting.
    # TODO: What about 'show gabaergic neurons as? [color]' or 'as? [blinking]' ?
    if getattr(match, 'formatting', None):
        form_lems = match.formatting.lemmas
        if 'list' in form_lems or 'information' in form_lems:
            formatting = 'information'
        elif 'network' in form_lems:
            formatting = 'network'
        elif 'morphology' in form_lems:
            formatting = 'morphology'

    if formatting:
        final_query += HasFormat(formatting)

    return final_query, "enum"

def interpret_NeuronsQuery_MoreGeneral(self, match):
    #print "interpret_NeuronsQuery_MoreGeneral", match._words, match.words, match._particles
    neuron = IsNeuron() + HasClass('Neuron')

    # NOTE: "format" group overrides any "opener" group--for formatting
    #       e.g. "List neurons in Lamina as morphology" will use morphology formatting.
    if getattr(match, 'formatting', None):
        form_lems = match.formatting.lemmas.lower()
        if 'list' in form_lems or 'information' in form_lems:
            neuron = neuron + HasFormat('information')
        elif 'network' in form_lems:
            neuron = neuron + HasFormat('network')
            # NOTE: We don't even bother checking for "morphology", since that's assumed default.
    elif getattr(match, 'opener', None):
        form_lems = match.opener.lemmas.lower()
        if 'list' in form_lems:
            neuron = neuron + HasFormat('information')
        elif 'graph' in form_lems:
            neuron = neuron + HasFormat('network')

    if getattr(match, 'region_list', None):
        neuron = neuron + OwnedBy( get_region_owner(match.region_list, notneurons) )
    if getattr(match, 'neuron_modifiers', None):
        mods = []
        # NOTE: The following assumes whitespace separates JJs / NNs:
        for m in finditer((Pos("JJ") | Pos("NN")), match.neuron_modifiers):
            i, j = m.span()
            mod_name = match.neuron_modifiers[i:j][0].token.lower()
            mods.append(mod_name)
        if len(mods) == 1:
            modifier = get_name_expression(mods[0])
            neuron = neuron + Has(modifier)
        elif len(mods) > 1:
            # NOTE: We assume this is a disjunction of modifiers for now
            andop = IsOrOp()
            for mod in mods:
                modifier = get_name_expression(mod)
                andop += HasPart(modifier)
            neuron += Has(andop)
    if getattr(match, "transmitters", None):
        mods = []
        # NOTE: The following assumes whitespace separates adjnouns:
        for m in finditer(adjnoun, match.transmitters):
            i, j = m.span()
            mod_name = match.transmitters[i:j][0].token.lower()
            mods.append(mod_name)
        if len(mods) == 1:
            modifier = get_name_expression(mods[0])
            neuron = neuron + Has(modifier)
        elif len(mods) > 1:
            # NOTE: We assume this is a disjunction of modifiers for now
            andop = IsOrOp()
            for mod in modifiers:
                modifier = get_name_expression(mod)
                andop += HasPart(modifier)
            neuron += Has(andop)
    if getattr(match, "neuron_name", None):
        # In keeping with the "spirit of the tree" (as described in the codegen file),
        # we put the neuron name in the neuron node if there's only 1 name;
        # We only need to create a 'has' node if there's more than 1 name (e.g. and, or).
        # For now, we only support one name to begin with.
        neuron = neuron + HasName(match.neuron_name.tokens)
    if getattr(match, "expressing_marker", None):
        marker = IsGeneticMarker() + HasName(match.expressing_marker.lemmas)
        neuron = neuron + HasGeneticMarker(marker)
    if getattr(match, "conn_quant", None):
        quantdir = IsNumConnections()
        # TODO: Don't use finditer; just do a search. Clean this up.
        for n in finditer(Pos("CD"), match.conn_quant):
            r, s = n.span()
            conn_num = ' '.join([c.token for c in match.conn_quant[r:s]])
            moreorless = False
            for o in finditer(Lemmas("more than"), match.conn_quant):
                quantdir = quantdir + HasMoreThan(conn_num)
                moreorless = True
            for o in finditer(Lemmas("less than"), match.conn_quant):
                quantdir = quantdir + HasLessThan(conn_num)
                moreorless = True
            if not moreorless:
                quantdir = quantdir + HasEqualTo(conn_num)
        for n in finditer(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"), match.conn_quant):
            r, s = n.span()
            conn_target = ' '.join([c.token for c in match.conn_quant[r:s]])
            # TODO: Make conn_target.lower() ?
            quantdir = quantdir + HasConnectionsTarget(conn_target)
        neuron = neuron + HasConnections(quantdir)
    # neuron_label = NameOf( neuron )
    # return neuron_label, "enum"
    return neuron, "enum"

def interpret_ColorCommand( self, match ):
    # TODO: Clean this up. This is only to reduce other needed changes elsewhere.
    command = IsNeuron() + HasClass('Neuron')
    command += HasVerb( "color" )
    if getattr( match, 'color', None ):
        # TODO: Clean this up. It's redundant.
        hue = match.color.lemmas
        if hue in colors_values:
            hue = colors_values[ hue ]
        else:
            if hue.startswith('#'):
                hue = hue[1:]
            hue = '0' * (6 - len(hue)) + hue
        command += HasColor( hue )
    # TODO: Able to make use of this second return value (at least for commands)?
    return command, "enum"

def interpret_VerbCommand( self, match ):
    # TODO: Again, clean this up (as above).
    command = IsNeuron() + HasClass('Neuron')
    command += HasVerb( str(match.verb.lemmas) )  # Because unicode can appear

    return command, 'enum'

def interpret_ClearAllCommand( self, match ):
    command = IsCommand( "clear" )
    # TODO: Able to make use of this second return value (at least for commands)?
    return command, "enum"

def interpret_ClearSomeCommand( self, match ):
    command = IsCommand( "clear" )
    if getattr( match, "clear_quant", None ):
        # TODO: Don't use finditer; just do a search
        for m in finditer( Pos("CD"), match.clear_quant ):
            i, j = m.span()
            # TODO: Join with a space? Is the list ever longer than 1, anyway?
            num = ' '.join( [ c.token for c in match.clear_quant[i:j] ] )
            command = command + HasEqualTo( num )
    else:
        command = command + HasEqualTo( "1" )
    return command, "enum"
