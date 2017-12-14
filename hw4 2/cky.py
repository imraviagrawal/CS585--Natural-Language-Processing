from pprint import pprint

# The productions rules have to be binarized.

grammar_text = """
S -> NPZ VP
S -> NP VBZ
NP -> Det Noun
NPZ -> Det Nouns
VP -> Verb NP
VBZ -> Verbs NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP
"""

lexicon = {
    'Nouns': set(['cats', 'dogs']),
    'Verbs': set(['attacked','attacks']),
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'Verb': set([ 'saw', 'loved', 'hated', 'attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)

# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

#print "Grammar rules in tuple form:"
#pprint(grammar_rules)
#print "Rule parents indexed by children:"
#pprint(possible_parents_for_children)


def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    # First working on the Dialonal cells
    for i in range(len(sentence)):
        for l in lexicon:
            if sentence[i] in lexicon[l]:
                cells[i, i + 1].append(l)
    
    for j in range(2, len(sentence) + 1):
        for i in range(len(sentence) - j + 1):
                m = i + j 
                while m  - 1 > i:
                    for rule in cells[i, m - 1]:
                        for other_rule in cells[m - 1, i + j]:
                            if (rule, other_rule) in possible_parents_for_children:
                                new_rule = possible_parents_for_children[(rule, other_rule)]
                                cells[i, i + j].append(new_rule[0])
                    m = m - 1

    pprint(cells)
    return 'S' in cells[0, len(sentence)]


def cky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon

    N = len(sentence)
    cells = {}
    back_trace = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    for i in range(len(sentence)):
        for l in lexicon:
            if sentence[i] in lexicon[l]:
                cells[i, i + 1].append([l, sentence[i]])
    
    for j in range(2, len(sentence) + 1):
        for i in range(len(sentence) - j + 1):
                m = i + j 
                while m  - 1 > i:
                    for r,rule in enumerate(cells[i, m - 1]):
                        for o_r, other_rule in enumerate(cells[m - 1, i + j]):
                            #print(rule[0], other_rule[0])
                            if (rule[0], other_rule[0]) in possible_parents_for_children:
                                new_rule = possible_parents_for_children[rule[0], other_rule[0]]
                                cells[i, i + j].append([new_rule[0], [rule, other_rule]])
                    m = m - 1

    #pprint(cells)
    for rule in cells[0, len(sentence)]:
        if 'S' == rule[0]:
            return rule
    return "Rejected"

## some examples of calling these things...
## you probably want to call only one sentence at a time to help debug more easily.

# print cky_acceptance(['the','cat','attacked','the','food'])
# pprint( cky_parse(['the','cat','attacked','the','food']))
# pprint( cky_acceptance(['the','the']))
# pprint( cky_parse(['the','the']))
# print cky_acceptance(['the','cat','attacked','the','food','with','a','dog'])
# pprint( cky_parse(['the','cat','attacked','the','food','with','a','dog']) )
# pprint( cky_parse(['the','cat','with','a','table','attacked','the','food']) )
#
