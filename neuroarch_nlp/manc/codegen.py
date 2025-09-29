"""
NeuroArch JSON generation--from a "semantic abstract syntax tree" (as a quepy Expression)
"""

# TODO: In general, this code could still use some refactoring/cleaning.

from copy import deepcopy
import logging
logging.basicConfig()
log = logging.getLogger( 'neuroarch_nlp.manc.codegen' )
log.setLevel('DEBUG')
from .dsl import HasEqualTo, HasVerb, HasColor, HasFormat

class EfficiencyException( BaseException ):
    pass

codegen_optimization = True

def generate_json( sast ):
    """ Given a "semantic abstract syntax tree" (SAST) (e.g. quepy expression),
        return a dictionary with structure according to the expected NeuroArch JSON format.
    """
    # `node_edge_val` stores, for each node, the other nodes to which it's related.
    node_edge_val = {}
    for node in sast.iter_nodes():
        node_edge_val[ node ] = {}
        for rel, dest in sast.iter_edges( node ):
            if rel == 'part':
                if rel not in node_edge_val[ node ]:
                    node_edge_val[ node ][ rel ] = [ dest ]
                else:
                    node_edge_val[ node ][ rel ].append( dest )
            else:
                # NOTE: We assume all other rels appear at most once.
                node_edge_val[ node ][ rel ] = dest

    # For each subquery, find the "root" node, based on the "owns" relation.
    # NOTE: This assumes there's at most 1 such root for each subquery.
    def get_owner( target ):
        for node in node_edge_val:
            for rel in node_edge_val[ node ]:
                if rel == 'owns' and node_edge_val[ node ][ rel ] == target:
                    return node
        return target  # If no owner, consider the target as owning itself

    # Update references (relation values) from an old node ID to a new one. Used for optimizations.
    def update_refs( old_id, new_id ):
        for node in node_edge_val:
            for rel in node_edge_val[ node ]:
                # TODO: Clean this up.
                if rel == 'part':
                    for i, nid in enumerate( node_edge_val[node]['part'] ):
                        if nid == old_id:
                            node_edge_val[node]['part'][i] = new_id
                else:
                    if node_edge_val[ node ][ rel ] == old_id:
                        node_edge_val[ node ][ rel ] = new_id

    # Perform some "optimizations" for the code generation

    # Starting with "pushing down" neurons beyond the connectives of their 'has' relations
    # TODO: Clean this up.
    def pushdown_neuron( nid, neuron=None ):
        # NOTE: We assume pushdown_neuron was initially called with sast.head as the `nid`
        if neuron is None:
            # We're (still) looking for a neuron (e.g. if the sast.head was a conjunction/disjunction)
            # Continue pushdown_neuron until A neuron is found
            if 'type' not in node_edge_val[nid]:
                return

            nodetype = node_edge_val[nid]['type']
            if nodetype == 'and' or nodetype == 'or':
                for part in node_edge_val[nid]['part']:
                    pushdown_neuron( part )

            elif nodetype == 'neuron':
                if get_owner( nid ) == nid and 'has' in node_edge_val[nid]:
                    # If the node has an owner, we won't "move" the node, since we assume it's "filtered"
                    has_conn_id = node_edge_val[nid]['has']
                    has_conn = node_edge_val[ has_conn_id ]
                    if has_conn['type'] == 'or' or has_conn['type'] == 'and':
                        for i, part_id in enumerate( has_conn['part'] ):
                            if 'type' in node_edge_val[part_id] and (node_edge_val[part_id]['type'] == 'and'
                              or node_edge_val[part_id]['type'] == 'or'):
                                # Continue "pushing" the neuron down until we're not at a connective.
                                pushdown_neuron( part_id, neuron=node_edge_val[nid] )
                            else:
                                # Effectively create a new node
                                new_neuron_id = len( node_edge_val )
                                has_conn['part'][i] = new_neuron_id
                                node_edge_val[new_neuron_id] = deepcopy( node_edge_val[nid] )
                                # Copy everything from the original (neuron) node
                                # NOTE: This currently includes any "update_state" rel/val.
                                node_edge_val[new_neuron_id]['has'] = part_id
                            # If we reach a 'synapticConnection'-type node, check its subquery.
                            if 'type' in node_edge_val[part_id] \
                              and node_edge_val[part_id]['type'] == 'synapticConnection':
                                # We assume a 'synapticConnection' node only has 1 other rel/val.
                                if 'presynapticTo' in node_edge_val[part_id]:
                                    pushdown_neuron( node_edge_val[part_id]['presynapticTo'], None )
                                elif 'postsynapticTo' in node_edge_val[part_id]:
                                    pushdown_neuron( node_edge_val[part_id]['postsynapticTo'], None )

                        # Update references of the original neuron and connective
                        update_refs( nid, has_conn_id )
                        if sast.head == nid:
                            sast.head = has_conn_id

                if 'presynapticTo' in node_edge_val[nid]:
                    pushdown_neuron( node_edge_val[nid]['presynapticTo'], None )
                if 'postsynapticTo' in node_edge_val[nid]:
                    pushdown_neuron( node_edge_val[nid]['postsynapticTo'], None )
        else:
            # We found a neuron and are checking its 'has' conjunction/disjunction's children
            # NOTE: We assume this node has a 'type' and it's 'and' or 'or'
            # TODO: There's some redundancy that could be cleaned up.
            for i, part_id in enumerate( node_edge_val[nid]['part'] ):
                if 'type' in node_edge_val[part_id] and (node_edge_val[part_id]['type'] == 'and'
                  or node_edge_val[part_id]['type'] == 'or'):
                    # Continue "pushing" the neuron down until we're not at a connective.
                    pushdown_neuron( part_id, neuron=neuron )
                else:
                    # Effectively create a new node
                    new_neuron_id = len( node_edge_val )
                    node_edge_val[nid]['part'][i] = new_neuron_id
                    node_edge_val[new_neuron_id] = deepcopy( neuron )
                    # Copy everything from the original (neuron) node
                    # NOTE: This currently includes any "update_state" rel/val.
                    node_edge_val[new_neuron_id]['has'] = part_id
                # If we reach a 'synapticConnection'-type node, check its subquery.
                if 'type' in node_edge_val[part_id] \
                  and node_edge_val[part_id]['type'] == 'synapticConnection':
                    # We assume a 'synapticConnection' node only has 1 other rel/val.
                    if 'presynapticTo' in node_edge_val[part_id]:
                        pushdown_neuron( node_edge_val[part_id]['presynapticTo'], None )
                    elif 'postsynapticTo' in node_edge_val[part_id]:
                        pushdown_neuron( node_edge_val[part_id]['postsynapticTo'], None )

    def merge_neuronhasnode():
        # Go through all of the 'neuron' type nodes in the graph
        # For the neuron nodes that have specific relations not targeting an 'and'/'or' type node:
        #   Try to "merge" the nodes according to some rules:
        #   - type=neuron -> has -> type=attribute + key=name
        #     => type=neuron + name=[value]
        #   - type=neuron -> has -> type=attribute + key=Transmitters
        #     => type=neuron + Transmitters=[value]
        #   If a merge occurs, copy any additional relations/values that might still be useful
        #       (e.g. reference another node (relation's value type == int) in the graph)
        # (We could call this "merging (neuron) attributes".)
        # Rather than iterating over the structure as we're (potentially) changing it
        # or copying the structure before we iterate over it, we'll just maintain a list
        # of elements to remove after we're done iterating.
        nodes_to_delete = []
        for nid in node_edge_val:
            if node_edge_val[nid].get('type',None) == 'neuron' and 'has' in node_edge_val[nid]:
              #and get_owner( nid ) == nid: # And/or handle neuron 'attrs' via 'owns' (as currently)
                has_nid = node_edge_val[nid]['has']
                if node_edge_val[has_nid].get('type',None) == 'attribute':
                    # NOTE: We assume "attribute" types have a "key" and a "value"
                    key = node_edge_val[has_nid]['key']
                    if key in ['uname', 'name', 'Transmitters', 'locality']:
                        node_edge_val[nid][ key ] = node_edge_val[has_nid]['value']

                        # Now delete the 'attribute' node and the 'has' relation to it
                        #node_edge_val.pop( has_nid, None )
                        nodes_to_delete.append( has_nid )
                        node_edge_val[nid].pop( 'has', None )

                elif node_edge_val[has_nid].get('type',None) == 'synapticConnection':
                    for rel in node_edge_val[has_nid]:
                        if rel != 'type':
                            node_edge_val[ nid ][ rel ] = node_edge_val[ has_nid ][ rel ]

                    # Now delete the 'attribute' node and the 'has' relation to it
                    #node_edge_val.pop( has_nid, None )
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                elif node_edge_val[has_nid].get('type',None) == 'arbors':
                    node_edge_val[nid]['arbors'] = node_edge_val[has_nid]['region']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                elif node_edge_val[has_nid].get('type',None) == 'dendriteArbors':
                    node_edge_val[nid]['dendriteArbors'] = node_edge_val[has_nid]['region']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                elif node_edge_val[has_nid].get('type',None) == 'axonArbors':
                    node_edge_val[nid]['axonArbors'] = node_edge_val[has_nid]['region']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                elif node_edge_val[has_nid].get('type',None) == 'connectionTo':
                    node_edge_val[nid]['fromRegion'] = node_edge_val[has_nid]['fromRegion']
                    node_edge_val[nid]['toRegion'] = node_edge_val[has_nid]['toRegion']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                # TODO: We might want a more permanent solution (for regions as "modifiers")
                elif node_edge_val[has_nid].get('type',None) == 'region':
                    node_edge_val[nid]['region'] = {}
                    if 'name' in node_edge_val[has_nid]:
                        node_edge_val[nid]['region']['name'] = node_edge_val[has_nid]['name']
                    if 'class' in node_edge_val[has_nid]:
                        node_edge_val[nid]['region']['class'] = node_edge_val[has_nid]['class']
                    if 'instance' in node_edge_val[has_nid]:
                        node_edge_val[nid]['region']['instance'] = node_edge_val[has_nid]['instance']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )
                elif node_edge_val[has_nid].get('type',None) == 'ownerInstance':
                    node_edge_val[nid]['ownerInstance'] = node_edge_val[has_nid]['instance']
                    nodes_to_delete.append( has_nid )
                    node_edge_val[nid].pop( 'has', None )

        for nid in nodes_to_delete:
            node_edge_val.pop( nid, None )

    if codegen_optimization:
        pushdown_neuron( sast.head )
        merge_neuronhasnode()

    '''
    # Check the updates from optimization
    for node in node_edge_val:
        log.info( node )
        for rel in node_edge_val[ node ]:
            log.info( "\t"+ rel +"\t"+ str(node_edge_val[node][rel]) )
    log.info( "sast.head = "+ str(sast.head) )
    '''

    def set_owners( subq_conn ):
        if 'type' in node_edge_val[ subq_conn ] \
          and (node_edge_val[subq_conn]['type'] == 'and' or node_edge_val[subq_conn]['type'] == 'or'):
            for i, part_id in enumerate( node_edge_val[ subq_conn ]['part'] ):
                # Update each part ID to the owner of that node ID
                node_edge_val[ subq_conn ]['part'][i] = get_owner( part_id )
                set_owners( part_id )
                # NOTE: We could probably be more efficient about this whole process
                #       e.g. at least by only bothering to set_owners() if get_owner() changed the ID.

    root = get_owner( sast.head )
    set_owners( sast.head )

    def get_node_najson( memory, op, node_id, parent_type = None):
        """ Given a node in the SAST,
            output a corresponding list of NeuroArch (JSON) calls.

            `op` indicates the operation to perform on this node,
            but also indicates, if None, that this node starts a "memory chain".
        """
        node = node_edge_val[ node_id ]
        retlist = []

        if 'type' not in node:
            log.warning( "'type' not found in a node!" )
            return []
        ntype = node['type']

        # So, we can do this one of at least two ways:
        # - Get the type of the node first, and then see what relations work with it; or
        # - Get the relation (`op`erator/tion), and then get the type of the node
        # NOTE: Depending on how things evolve, we may want to change methods

        if ntype == 'and':
            lastlen = None
            for part in node['part']:
                retlist += get_node_najson( memory + len(retlist), op, part, parent_type = parent_type)
                if lastlen: # TODO: Make sure this is okay if lastlen == 0

                    retlist.append(
                        {"action":{ "op":{ "__and__":{ "memory": len(retlist) - lastlen}}}, "object":{"memory": 0}})
                lastlen = len( retlist )
        elif ntype == 'or':
            lastlen = None
            for part in node['part']:
                retlist += get_node_najson( memory + len(retlist), op, part, parent_type = parent_type)
                if lastlen:
                    retlist.append(
                        {"action":{ "op":{ "__or__":{ "memory": len(retlist) - lastlen}}}, "object":{"memory": 0}})
                lastlen = len( retlist )

        if op == 'owns' or op == 'subregion':
            if ntype == 'region':
                # NOTE: We consider "class" (in our SAST) to refer to "node_class" (in NA)
                if 'class' in node:
                    # outdict = { 'object': {'memory': memory + len(retlist)}, 'action': \
                    #     {'method': {'traverse_owns': {'cls': node['class']} } } }

                    outdict = { 'object': {'memory':  memory + len(retlist)},
                        'action': {'method': {'gen_traversal_in': \
                              {"min_depth": 1, \
                               "pass_through": ["ArborizesIn", node['class']]} } }}
                    retlist.append( outdict )
                elif 'instance' in node:
                    outdict = { 'object': {'memory': memory + len(retlist)}, 'action': \
                        {'method': {'traverse_owns': {'instanceof': node['instance']} } } }
                    retlist.append( outdict )
                else:
                    log.warning( "Region has no '(node_)class or instance'!" )
                if 'uname' in node: # TODO: This is identical to below. Remove redundancy.
                    outdict = { 'object': {'memory': 0}, 'action': \
                                    {'method': {'has': {'uname': node['uname']}} } }
                    retlist.append( outdict )
            elif ntype == 'neuron':
                if 'region' in node:
                    if isinstance(node['region'],dict):
                        if 'class' in node['region']:
                            # retlist.append({ 'object': {'memory': 0},
                            #                  'action': {'method': {'traverse_owns': {'cls': node['region']['class']}} } } )
                            retlist.append( { 'object': {'memory':  0},
                                'action': {'method': {'gen_traversal_in': \
                                      {"min_depth": 1, \
                                       "pass_through": ["ArborizesIn", node['region']['class']]} } }} )
                        if 'instance' in node['region']:
                            retlist.append({ 'object': {'memory': 0},
                                             'action': {'method': {'traverse_owns': {'instanceof': node['region']['instance']}} } } )
                        if 'name' in node['region']:
                            retlist.append({ 'object': {'memory': 0},
                                             'action': {'method': {'has': {'name': node['region']['name']}} } } )
                    else:
                        retlist.append( { 'object': {'class': 'Neuropil'},
                                          'action': {'method': {'query': {'name': node['region']}}} } )
                        # retlist.append( { 'object': {'memory': 0},
                        #                   'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                        retlist.append( { 'object': {'memory':  0},
                            'action': {'method': {'gen_traversal_in': \
                                  {"min_depth": 1, \
                                   "pass_through": ["ArborizesIn", node['class']]} } }})
                        retlist.append( { 'object': {'memory': 0},
                                          'action': {'op': {'__and__': {'memory': 2}}} } )
                if 'class' in node:
                    #outdict = { 'object': {'memory': memory + len(retlist)}, 'action': \
                    #    {'method': {'traverse_owns': {'cls': node['class']} } } }
                    # outdict = { 'object': {'memory': 0}, 'action': \
                    #     {'method': {'traverse_owns': {'cls': node['class']} } } }

                    # SHOW NEURONS IN [NEUROPIL] ends here
                    locality = False
                    if 'locality' in node:
                        locality = True
                    else:
                        parts = []
                        if 'has' in node and node['has'] > 0:
                            for n in range(node_id + 1, max(list(node_edge_val.keys()))):
                                peek_node = node_edge_val[n]
                                if 'part' in peek_node:
                                    parts = peek_node['part']
                                    break
                        for part in parts:
                            peek_node = node_edge_val[part]
                            if peek_node.get('key', None) == 'locality':
                                if peek_node['value'] == 'True':
                                    locality = True
                    if locality:
                        outdict = { 'object': {'memory': 0},
                            'action': {'method': {'owns': {'cls': node['class']}}}}
                    else:
                        if node['class'] == 'Neuron' and 'uname' in node:
                            outdict = { 'object': {'memory': 0},
                                        'action': {'method': {'gen_traversal_in': \
                                            {"pass_through": ["ArborizesIn", node['class'], 'instanceof',
                                                              {"uname": node["uname"]}],\
                                            "min_depth": 1}}}}
                            retlist.append(outdict)
                            return retlist    
                        else:
                            outdict = { 'object': {'memory': 0},
                                'action': {'method': {'gen_traversal_in': \
                                    {"pass_through": ["ArborizesIn", node['class']],\
                                    "min_depth": 1}}}}

                    retlist.append( outdict )
                else:
                    log.warning( "Neuron has no '(node_)class'!" )
                    return []
                # NOTE: We assume that, if any of these checks pass (e.g. "name" is in this node),
                #       then they are NOT (also) in a separate node (e.g. via "has").
                #       This means our analysis must generate the SAST without duplication.
                if 'uname' in node:
                    retlist.append( { 'object': {'memory': 0}, 'action':
                        {'method': {'has': {'uname': node['uname']}} } } )
                if 'Transmitters' in node:
                    retlist.append( { 'object': {'memory': 0}, 'action':
                        {'method': {'has': {'Transmitters': [ node['Transmitters'] ]}} } } )
                # if 'locality' in node:
                #     retlist.append( {'object': {'memory': 0}, 'action':
                #         {'method': {'has': {'locality': node['locality']}} } } )
                if 'ownerInstance' in node:
                    retlist.append( { 'object': {'class': 'Neuropil'},
                        'action': {'method': {'query': {}}} } )
                    retlist.append( { 'object': {'memory': 0},
                        'action': {'method': {'owns': {'instanceof': node['ownerInstance']}}} } )
                    retlist.append( { 'object': {'memory': 0},
                        'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                    retlist.append( { 'object': {'memory': 0},
                        'action': {'op': {'__and__': {'memory': 3}}} } )
            elif ntype == 'and' or ntype == 'or':
                pass
            else:
                log.warning( "Unsupported type for 'owns' relation!" )
        elif op == 'has':
            if ntype == 'attribute':
                params = {}
                # NOTE: We assume that there's exactly 1 key and value in a node, if any
                if 'key' in node:
                    if 'value' not in node:
                        log.warning( "'key' present, but 'value' not present!" )
                    elif node['key'] == 'class':
                        #       e.g. just as the relation "class" itself?
                        params[ 'cls' ] = node['value']
                    elif node['key'] == 'Transmitters':
                        # NeuroArch expects Transmitters as a list
                        params[ 'Transmitters' ] = [ node['value'] ]
                    elif node['key'] == 'locality':
                        # Taken care of by the in neuronpil query
                        pass
                    elif node['key'] in ['uname', 'name']:
                        if parent_type == 'neuron':
                            params[ 'uname' ] = node['value']
                        else:
                            params[ node['key'] ] = node['value']
                    else:
                        if node['value'] == 'True':
                            params[ node['key'] ] = True
                        elif node['value'] == 'False':
                            params[ node['key'] ] = False
                        else:
                            params[ node['key'] ] = node['value']
                if len( params ) > 0:
                    outdict = { 'object': {'memory': memory + len(retlist)}, 'action': \
                        {'method': {'has': params} } }
                    retlist.append( outdict )
            elif ntype == 'synapticConnection':
                pass
            elif ntype == 'region':
                if 'class' in node:
                    if 'name' in node:
                        retlist.append( { 'object': {'class': node['class']},
                                          'action': {'method': {'query': {'name': node['name']}}} } )
                    else:
                        retlist.append( { 'object': {'class': node['class']},
                                          'action': {'method': {'query': {}}} } )
                elif 'instance' in node:
                    retlist.append( { 'object': {'class': 'Neuropil'},
                                      'action': {'method': {'query': {}}} } )
                    retlist.append( {'object': {'memory': 0},
                                     'action': {'method': {'traverse_owns': {'instanceof': node['instance']}} } } )
                    if 'name' in node:
                        retlist.append( {'object': {'memory': 0},
                                         'action': {'method': {'has': {'name': node['name']}} } } )
                else:
                    return retlist
                # NOTE: We assume we're looking for Neurons
                # retlist.append( { 'object': {'memory': 0},
                #     'action': {'method': {'traverse_owns': {'cls': 'Neuron'}} } } )
                retlist.append( { 'object': {'memory': 0},
                    'action': {'method': {'gen_traversal_in': \
                          {"min_depth": 1, \
                           "pass_through": ["ArborizesIn", "Neuron"]} } }})
                # retlist.append( { 'object': {'memory': 0},
                #     'action': {'op': {'__and__': {'memory': memory + len(retlist)}}} } )
                # TODO: Or just 'memory': 2 ?
            elif ntype == 'ownerInstance':
                retlist.append( { 'object': {'class': 'Neuropil'},
                    'action': {'method': {'query': {}}} } )
                retlist.append( { 'object': {'memory': 0},
                    'action': {'method': {'owns': {'instanceof': node['instance']}}} } )
                # NOTE: We assume we're looking for Neurons
                retlist.append( { 'object': {'memory': 0},
                    'action': {'method': {'traverse_owns': {'cls': 'Neuron'}} } } )
                retlist.append( { 'object': {'memory': 0},
                    'action': {'op': {'__and__': {'memory': memory + len(retlist)}}} } )
            elif ntype == 'and' or ntype == 'or':
                pass
            else:
                log.warning( "Unsupported type for 'has' relation!: %s" % ntype )
        elif op is None:
            if ntype == 'region':
                if 'name' not in node:
                    log.warning( "'name' not in region node!" )
                if 'class' not in node:
                    if 'instance' in node:
                        retlist.append( { 'object': {'class': 'Neuropil'},
                                'action': {'method': {'query': {}}} } )
                        retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'traverse_owns': {'instanceof': node['instance']}}} } )
                else:
                    retlist.append( { 'object': {'class': node['class']},
                                'action': {'method': {'query': {}}} } )
                if 'name' in node:
                    retlist.append( { 'object': {'memory': 0},
                            'action': {'method': {'has': {'name': node['name']}}} } )
            elif ntype == 'neuron':
                if 'class' not in node:
                    log.warning( "'class' not in neuron node!" )
                    return []
                params = {}
                if 'name' in node:
                    params['name'] = node['name']
                if 'uname' in node:
                    params['uname'] = node['uname']
                if 'Transmitters' in node:
                    params['Transmitters'] = [ node['Transmitters'] ]
                if 'locality' in node:
                    params['locality'] = node['locality']
                if 'region' in node:
                    params['region'] = node['region']
                if 'ownerInstance' in node:
                    params['ownerInstance'] = node['ownerInstance']

                def add_attributes():
                    attrlist = []
                    for att in params:
                        if att == 'region':
                            retlist.append( { 'object': {'class': 'Neuropil'},
                                'action': {'method': {'query': {'name': params['region']}}} } )
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'op': {'__and__': {'memory': 2}}} } )
                        elif att == 'ownerInstance':
                            retlist.append( { 'object': {'class': 'Neuropil'},
                                'action': {'method': {'query': {}}} } )
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'owns': {'instanceof': params['ownerInstance']}}} } )
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'op': {'__and__': {'memory': 3}}} } )
                        else:
                            attrlist.append( { 'object': {'memory': 0}, 'action':
                                {'method': {'has': {att: params[att]}}} } )
                    return attrlist

                # TODO: Clean all of this up.
                # NOTE: We assume a node can either be pre- or post-synaptic--not both.
                # NOTE: We assume there's at most 1 subquery that the (other) node is pre/postsynaptic to.
                if 'presynapticTo' in node:
                    retlist += get_node_najson( 0, None, get_owner( node['presynapticTo'] ) )
                    if 'hasMoreThan' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                    elif 'hasLessThan' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                    elif 'hasAtLeast' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                    elif 'hasAtMost' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                    elif 'hasEqualTo' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                    else:
                        retlist.append(
                            {"action": {"method": {"pre_synaptic_neurons": {}}}, "object": {"memory": 0}})
                    retlist += add_attributes()
                elif 'presynapticToState' in node:
                    if 'hasMoreThan' in node:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                    elif 'hasLessThan' in node:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                    elif 'hasAtLeast' in node:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                    elif 'hasAtMost' in node:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                    elif 'hasEqualTo' in node:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                    else:
                        retlist.append( {'object': {'state': int(node['presynapticToState'])},
                                         "action": {"method": {"pre_synaptic_neurons": {}}} } )
                    retlist += add_attributes()
                elif 'postsynapticTo' in node:
                    retlist += get_node_najson( 0, None, get_owner( node['postsynapticTo'] ) )
                    if 'hasMoreThan' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                    elif 'hasLessThan' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                    elif 'hasAtLeast' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                    elif 'hasAtMost' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                    elif 'hasEqualTo' in node:
                        retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                    else:
                        retlist.append(
                            {"action": {"method": {"post_synaptic_neurons": {}}}, "object": {"memory": 0}})
                    retlist += add_attributes()
                elif 'postsynapticToState' in node:
                    if 'hasMoreThan' in node:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                    elif 'hasLessThan' in node:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                    elif 'hasAtLeast' in node:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                    elif 'hasAtMost' in node:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                    elif 'hasEqualTo' in node:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                    else:
                        retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {}}} } )
                    retlist += add_attributes()
                # NOTE: Right now we assume no more than 1 of these relations would be in a neuron
                elif 'dendriteArbors' in node:
                    retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                        {'method': {'query': {'dendrites':node['dendriteArbors']}} } } )
                    retlist.append( { 'object': {'memory': 0}, 'action':
                        {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                                                         'min_depth': 1}} } } )
                    # NOTE: This list is currently guaranteed to be empty,
                    #       but we'll add it as a check for our future selves.
                    retlist += add_attributes()
                elif 'axonArbors' in node:
                    retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                        {'method': {'query': {'axons':node['axonArbors']}} } } )
                    retlist.append( { 'object': {'memory': 0}, 'action': \
                        {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                                                         'min_depth': 1}} } } )
                    retlist += add_attributes()
                elif 'arbors' in node:
                    retlist.append( { 'object': {'class': ['Neuropil', 'Subregion']},
                                      'action': {'method': {'query': {'name': node['arbors']}}} } )
                    retlist.append( { 'object': {'memory': 0},
                        'action': {'method': {'gen_traversal_in': \
                              {"min_depth": 1, \
                               "pass_through": ["ArborizesIn", "Neuron"]} } }})
                    # retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                    #     {'method': {'query': {'dendrites':node['arbors']}} } } )
                    # retlist.append( { 'object': {'memory': 0}, 'action':
                    #     {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                    #                                      'min_depth': 1}} } } )
                    # retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                    #     {'method': {'query': {'axons':node['arbors']}} } } )
                    # retlist.append( { 'object': {'memory': 0}, 'action':
                    #     {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                    #                                      'min_depth': 1}} } } )
                    # retlist.append( { 'object': {'memory': 0}, 'action':
                    #     {'op': {'__or__': {'memory': 2} } } } )
                    retlist += add_attributes()
                elif 'fromRegion' in node:
                    # NOTE: We assume 'toRegion' is also in node.
                    retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                        {'method': {'query': {'dendrites':node['fromRegion']}} } } )
                    retlist.append( { 'object': {'memory': 0}, 'action': \
                        {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                                                         'min_depth': 1}} } } )
                    retlist.append( { 'object': {'class': 'ArborizationData'}, 'action':
                        {'method': {'query': {'axons':node['toRegion']}} } } )
                    retlist.append( { 'object': {'memory': 0}, 'action': \
                        {'method': {'gen_traversal_in': {'pass_through':['HasData','Neuron'],
                                                         'min_depth': 1}} } } )
                    retlist.append( { 'object': {'memory': 0}, 'action':
                        {'op': {'__and__': {'memory': 2} } } } )
                    retlist += add_attributes()
                else:
                    if len( params ) == 0:
                        logging.error( "graph.Neuron.query() was about to be output!" )
                        # NOTE: We consider this (intermediate) query as "un-outputable"
                        #       because it currently takes too long for the system to process it.
                        raise EfficiencyException

                        retlist.append( { 'object': {'class': node['class']},
                            'action': {'method': {'query': {}}} } )
                    # TODO: There's considerable redundancy. Clean this up.
                    elif 'region' in params:
                        if isinstance(params['region'],dict):
                            if 'class' in params['region']:
                                retlist.append( { 'object': {'class': 'Neuropil'},
                                                  'action': {'method': {'query': {}}} } )
                                # retlist.append({ 'object': {'memory': 0},
                                #                  'action': {'method': {'traverse_owns': {'cls': params['region']['class']}} } } )
                            if 'instance' in params['region']:
                                retlist.append( { 'object': {'class': 'Neuropil'},
                                                  'action': {'method': {'query': {}}} } )
                                retlist.append({ 'object': {'memory': 0},
                                                 'action': {'method': {'traverse_owns': {'instanceof': params['region']['instance']}} } } )
                            if 'name' in params['region']:
                                retlist.append({ 'object': {'memory': 0},
                                                 'action': {'method': {'has': {'name': params['region']['name']}} } } )
                        else:
                            retlist.append( { 'object': {'class': 'Neuropil'},
                                              'action': {'method': {'query': {'name': params['region']}}} } )
                        # retlist.append( { 'object': {'memory': 0},
                        #                   'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                        # SHOW NEUROPIL ENDS HERE
                        if 'locality' in params:
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'owns': \
                                      {"cls": node['class']} } }})
                            params.pop('locality')
                        else:
                            retlist.append( { 'object': {'memory': 0},
                                'action': {'method': {'gen_traversal_in': \
                                      {"min_depth": 1, \
                                       "pass_through": ["ArborizesIn", node['class']]} } }})
                        params.pop( 'region' )  # Make it clear it's being removed.
                        retlist += add_attributes()
                    elif 'ownerInstance' in params:
                        retlist.append( { 'object': {'class': 'Neuropil'},
                            'action': {'method': {'query': {}}} } )
                        retlist.append( { 'object': {'memory': 0},
                            'action': {'method': {'owns': {'instanceof': params['ownerInstance']}}} } )
                        retlist.append( { 'object': {'memory': 0},
                            'action': {'method': {'traverse_owns': {'cls': node['class']}} } } )
                        params.pop( 'ownerInstance' )  # Make it clear it's being removed.
                        retlist += add_attributes()
                    elif 'name' in params:
                        retlist.append( { 'object': {'class': node['class']}, \
                            'action': {'method': {'query': {'uname' if node['class'] == 'Neuron' else 'name':params['name']}}} } )
                        params.pop( 'name' )  # Make it clear it's being removed.
                        retlist += add_attributes()
                    elif 'uname' in params:
                        retlist.append( { 'object': {'class': node['class']}, \
                            'action': {'method': {'query': {'uname': params['uname']}}} } )
                        params.pop( 'uname' )  # Make it clear it's being removed.
                        retlist += add_attributes()
                    elif 'Transmitters' in params:
                        retlist.append( { 'object': {'class': 'NeurotransmitterData'}, 'action': \
                            {'method': {'query': {'Transmitters':params['Transmitters']}} } } )
                        # TODO: Check that how we generate JSON for gen_traversal_in is acceptable.
                        retlist.append( { 'object': {'memory': 0}, 'action': \
                            {'method': {'gen_traversal_in': {'pass_through': ['HasData','Neuron'], \
                                                             'min_depth': 1}} } } )
                        params.pop( 'Transmitters' )  # Make it clear it's being removed.
                        retlist += add_attributes()
                    elif 'locality' in params:
                        params.pop( 'locality' )
                        # retlist.append( { 'object': {'class': node['class']}, \
                        #     'action': {'method': {'query': {'locality':params['locality']}}} } )
                        # params.pop( 'locality' )  # Make it clear it's being removed.
                        # retlist += add_attributes()
            elif ntype == 'and' or ntype == 'or':
                pass
            else:
                log.warning( 'Unsupported type to be at "start" of query!' )
        else:
            pass

        if 'has' in node:
            retlist += get_node_najson( 0, 'has', node['has'], parent_type = ntype)

        # TODO: Clean this up. Is it even necessary (with codegen_optimization, at least)?
        if not (op is None and ntype == 'neuron'):
            # We'll have any pre/postsynaptic neurons apply to the node after its 'has' properties are done.
            lastlen = len(retlist)

            # NOTE: We assume a node can either be pre- or post-synaptic--not both.
            # NOTE: We assume there's at most 1 subquery that the (other) node is pre/postsynaptic to.
            # TODO: Clean up use of relations. And this whole segment in general.
            if 'presynapticTo' in node:
                retlist += get_node_najson( 0, None, get_owner( node['presynapticTo'] ) )
                if 'hasMoreThan' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                elif 'hasLessThan' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                elif 'hasAtLeast' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                elif 'hasAtMost' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                elif 'hasEqualTo' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                else:
                    retlist.append(
                        {"action": {"method": {"pre_synaptic_neurons": {}}}, "object": {"memory": 0}})
                retlist.append(
                    {"action": {"op": {"__and__": {'memory': len(retlist) - lastlen}}}, "object": {"memory": 0}})
            elif 'presynapticToState' in node:
                if 'hasMoreThan' in node:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                elif 'hasLessThan' in node:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                elif 'hasAtLeast' in node:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                elif 'hasAtMost' in node:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                elif 'hasEqualTo' in node:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                        "action": {"method": {"pre_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                else:
                    retlist.append( {'object': {'state': int(node['presynapticToState'])},
                                         "action": {"method": {"pre_synaptic_neurons": {}}} } )
                retlist.append(
                    {"action": {"op": {"__and__": {'memory': len(retlist) - lastlen}}}, "object": {"memory": 0}})
            elif 'postsynapticTo' in node:
                retlist += get_node_najson( 0, None, get_owner( node['postsynapticTo'] ) )
                if 'hasMoreThan' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                elif 'hasLessThan' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                elif 'hasAtLeast' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                elif 'hasAtMost' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                elif 'hasEqualTo' in node:
                    retlist.append( {"object": {"memory": 0},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                else:
                    retlist.append(
                        {"action": {"method": {"post_synaptic_neurons": {}}}, "object": {"memory": 0}})
                retlist.append(
                    {"action": {"op": {"__and__": {'memory': len(retlist) - lastlen}}}, "object": {"memory": 0}})
            elif 'postsynapticToState' in node:
                if 'hasMoreThan' in node:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasMoreThan'],'rel':'>'}}} } )
                elif 'hasLessThan' in node:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasLessThan'],'rel':'<'}}} } )
                elif 'hasAtLeast' in node:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtLeast'],'rel':'>='}}} } )
                elif 'hasAtMost' in node:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasAtMost'],'rel':'<='}}} } )
                elif 'hasEqualTo' in node:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {'N':node['hasEqualTo'],'rel':'='}}} } )
                else:
                    retlist.append( {'object': {'state': int(node['postsynapticToState'])},
                        "action": {"method": {"post_synaptic_neurons": {}}} } )
                retlist.append(
                    {"action": {"op": {"__and__": {'memory': len(retlist) - lastlen}}}, "object": {"memory": 0}})

        # NOTE: "Subregions" currently cannot be grouped with and/or operators--at the parse stage
        if 'subregion' in node:
            retlist += get_node_najson( 0, 'subregion', node['subregion'] )

        if 'owns' in node:
            retlist += get_node_najson( 0, 'owns', node['owns'] )

        return retlist

    if 'command' in node_edge_val[ root ]:
        # This is a command.
        node = node_edge_val[ root ]
        comm_type = node[ 'command' ]
        command = {}
        if comm_type == 'clear':
            if HasEqualTo.relation in node:
                command = { 'undo' : { 'states' : node[ HasEqualTo.relation ] } }
            else:
                command = { 'restart': {} }
        output = { 'command': command }
    else:
        # This is a query.
        # NOTE: We assume the 0th node has formatting information, if it's present at all.
        node0 = node_edge_val[0]
        try:
            querylist = get_node_najson( 0, None, root )
        except EfficiencyException:
            # If, anywhere in the output, we were about to query for all neurons,
            # we currently ignore the whole query.
            querylist = []

        output = { 'query': querylist }
        if HasFormat.relation in node0:
            output[ 'format' ] = node0[ HasFormat.relation ]
        else:
            output[ 'format' ] = 'morphology'

        if HasVerb.relation in node0:
            output[ 'verb' ] = node0[ HasVerb.relation ]
        if HasColor.relation in node0:
            output[ 'color' ] = node0[ HasColor.relation ]

    #log.info(output)
    return sast.get_head(), output
