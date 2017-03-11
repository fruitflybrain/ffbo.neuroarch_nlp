from quepy.dsl import FixedType, FixedRelation, FixedDataRelation

class NAType(FixedType):
    fixedtyperelation = "type"

class HasName(FixedDataRelation):
    relation = "name"

class HasClass(FixedDataRelation):
    relation = "class"

class IsAndOp(NAType):
    fixedtype = "and"

class IsOrOp(NAType):
    fixedtype = "or"

class IsBrainRegion(NAType):
    fixedtype = "region"

class IsNeuron(NAType):
    fixedtype = "neuron"

class IsCommand( FixedDataRelation ):
    relation = "command"

class HasFormat( FixedDataRelation ):
    relation = "format"

# For "pin"/"unpin", "blink"/"unblink", etc.
class HasVerb( FixedDataRelation ):
    relation = "verb"

# Used with the "color" verb
class HasColor( FixedDataRelation ):
    relation = "color"

class IsNeuronModifier(NAType):
    fixedtype = "neuronModifier"

class IsAttribute(NAType):
    fixedtype = "attribute"

class IsSynapticConnection(NAType):
    fixedtype = "synapticConnection"

class PresynapticTo(FixedRelation):
    relation = "presynapticTo"

class PostsynapticTo(FixedRelation):
    relation = "postsynapticTo"

class PresynapticToState(FixedDataRelation):
    relation = "presynapticToState"

class PostsynapticToState(FixedDataRelation):
    relation = "postsynapticToState"

class HasKey(FixedDataRelation):
    relation = "key"

class HasValue(FixedDataRelation):
    relation = "value"

class IsGeneticMarker(NAType):
    fixedtype = "geneticMarker"

class IsNumConnections(NAType):
    fixedtype = "numNeuronConnections"

class OwnedBy(FixedRelation):
    relation = "owns"
    reverse = True

class HasSubregion(FixedRelation):
    # This is basically the "owns" relation, but distinguishes "nested" regions,
    # making some computations later a bit easier to interpret (for now).
    relation = "subregion"

class HasPart(FixedRelation):
    relation = "part"

class Has(FixedRelation):
    relation = "has"

class IsConnection(NAType):
    fixedtype = 'connectionTo'

class HasType(FixedDataRelation):
    relation = 'type'

# TODO: This should eventually just be a FixedRelation, allowing, e.g. subqueries
class HasRegion(FixedDataRelation):
    relation = 'region'

# TODO: Support nodes (e.g. subqueries?), rather than just (single) name strings
class FromRegion(FixedDataRelation):
    relation = 'fromRegion'

class ToRegion(FixedDataRelation):
    relation = 'toRegion'

class IsOwnerInstance(NAType):
    fixedtype = 'ownerInstance'

class HasInstance(FixedDataRelation):
    relation = 'instance'

class HasEqualTo(FixedDataRelation):
    relation = "hasEqualTo"

###################################################################################
# NOTE: The following are referenced in code, but full support is not yet provided:
class HasGeneticMarker(FixedRelation):
    relation = "hasGeneticMarker"

class HasMoreThan(FixedDataRelation):
    relation = "hasMoreThan"

class HasLessThan(FixedDataRelation):
    relation = "hasLessThan"

class HasConnectionsTarget(FixedDataRelation):
    relation = "hasConnectionsTarget"

class HasConnections(FixedRelation):
    relation = "hasConnections"
