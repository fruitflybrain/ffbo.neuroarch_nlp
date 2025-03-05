from neuroarch_nlp.interface import PrototypeBaselineTranslator
from neuroarch_nlp.hemibrain.codegen import generate_json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('neuroarch_nlp.hemibrain')

# Initialize the translator
translator = PrototypeBaselineTranslator('hemibrain')

# Test queries covering all patterns
test_queries = [

    # Single direction queries (onto/from)
    # "Show synapses",
    # "Show cholinergic neurons"
    # "Show synapses to L1 neurons",
    # "Show synapses onto Mi1 neurons",
    # "Show synapses from T4 neurons",
    # "Show synapses from L2 neurons",
    
    # # Bidirectional queries
    # "Show neurons from EB",
    "Show synapses from L1 neurons",
    # "Show synapses from Mi1 neurons to Tm3 neurons",
    
    # # Region-specific queries
    # "Show synapses in medulla",
    # "Show synapses in M10",
    # "Show synapses from L1 to T4 in medulla",
    
    # # Neuron type queries
    # "Show synapses from GABAergic neurons",
    # "Show synapses from cholinergic neurons to GABAergic neurons"
]

# Test each query
for query in test_queries:
    print(f"\n{'='*50}")
    print(f"Testing query: {query}")
    print('='*50)
    try:
        result = translator.nlp_query(query)
        head, json_output = generate_json(result)
        print("\nParsed successfully!")
        print("Result:", json_output)
    except Exception as e:
        print("\nError parsing query:", str(e))