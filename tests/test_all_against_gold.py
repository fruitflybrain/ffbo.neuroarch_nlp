#!/usr/bin/env python
# coding: utf-8

import json
from neuroarch_nlp.interface import Translator

outfilename = 'OUTPUT'

import logging
#logging.basicConfig( level=logging.INFO )#,filename=outfilename)

if __name__ == "__main__":
    translator = Translator()

    with open( 'gold_in_out', 'r' ) as f:
        with open( outfilename, 'w' ) as w:
            from datadiff import diff

            # The number of (correct, incorrect) queries of each type, based on test results.
            query_results = { 'SUPPORTED': [0, 0], 'CHECK': [0, 0], 'UNSUPPORTED': [0, 0] }
            # NOTE: This could use cleaning up.
            def add_result( sup, chk, uns, correct ):
                if chk:
                    if correct:
                        query_results['CHECK'][0] += 1
                    else:
                        query_results['CHECK'][1] += 1
                if uns:
                    if correct:
                        query_results['UNSUPPORTED'][0] += 1
                    else:
                        query_results['UNSUPPORTED'][1] += 1
                if sup:
                    if correct:
                        query_results['SUPPORTED'][0] += 1
                    else:
                        query_results['SUPPORTED'][1] += 1

            query_segment = False
            for line in f:
                if query_segment:
                    if '-+-+-+-\n' == line:
                        # We've gone through all of the acceptable queries, and can now test and compare.
                        query_segment = False

                        gold_queries.append( json.loads( gold_query ) )
                        test_query = translator.nlp_query( na_query )
                        #print( "TEST =\n"+ str(test_query) )

                        # Keep track of whether a given query is supported/unsupported/to be checked
                        # (as determined by the gold input/output file).
                        supported = True
                        check = False
                        unsupported = False

                        # If the test_query is incorrect, we'll ouput the diff with the least number of differences.
                        least_diffs = 999999 # NOTE: Could use 'inf' or something, yeah?
                        least_diffs_diff = None
                        for gold_query in gold_queries:
                            check = gold_query.pop( 'CHECK', False )
                            unsupported = gold_query.pop( 'UNSUPPORTED', False ) \
                                       or gold_query.pop( 'TODO', False )
                            if check or unsupported:
                                supported = False

                            if gold_query == test_query:
                                add_result( supported, check, unsupported, True )
                                #print( na_query +" -- OK\n" )
                                # NOTE: It's not currently necessary to set the least_diffs_diff when there's a match.
                                
                                break
                            else:
                                d_diff = diff(gold_query, test_query)
                                diffs = sum([ 1 for x in d_diff.diffs if x[0] != 'equal' ])
                                if diffs < least_diffs:
                                    least_diffs = diffs
                                    least_diffs_diff = d_diff
                        else:
                            # NOTE: We assume any 'CHECK'/'UNSUPPORTED'/not indicators are the same across all gold_queries
                            #       (acceptable JSON) for a given query. (So we just check the last gold_query.)
                            add_result( supported, check, unsupported, False )
                            if supported:
                                print( na_query +" -- FAILED\n" )
                                print( str(least_diffs_diff) +'\n' )
                                print( json.dumps( test_query, indent=3, sort_keys=True ) )
                                #print( "   GOLD =\n"+ str(json.dumps(gold_query,indent=3)) )
                                #print( "   TEST =\n"+ str(json.dumps(test_query,indent=3)) )
                    elif '---O---\n' == line:
                        # We found another acceptable query.
                        gold_queries.append( json.loads( gold_query ) )
                        gold_query = ''
                    else:
                        gold_query = gold_query + line
                else:
                    if '-+-+-+-\n' == line:
                        query_segment = True
                        gold_queries = []
                        gold_query = ''
                    else:
                        na_query = line
            for qtype in query_results:
                correct = query_results[ qtype ][0]
                incorrect = query_results[ qtype ][1]
                total = correct + incorrect
                print( "\n"+ qtype +":" )
                print( "  Correct: "+ str(correct) +" / "+ str(total) +
                    "  ("+ str(float(correct)/total*100) +"% accuracy)" )
