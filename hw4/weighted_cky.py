from pprint import pprint

grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}


def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    pass
    print "Grammar rules in tuple form:"
    pprint(grammar_rules)
    print "Rule parents indexed by children:"
    pprint(possible_parents_for_children)
    print "probabilities"
    pprint(probabilities)
    print "Lexicon"
    pprint(lexicon)


def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    return None

