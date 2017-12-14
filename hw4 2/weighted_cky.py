from pprint import pprint

grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}


def populate_grammar_rules():

    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    
    file = open("pcfg_grammar_modified", 'rb')
    text = file.readlines()
    for line in text:
        #if not line.strip(): continue
        line = line.strip()
        #print(line)
        left, right = line.split("->")
        left = left.strip()
        children = right.split()
        #grammar_rules.append([left, right])
        rule = (left, tuple(children))
        grammar_rules.append(rule)

        if len(children) > 2:
            if tuple(children)[:-1] in possible_parents_for_children:
                possible_parents_for_children[tuple(children)[:-1]].append(left)
            else:
                possible_parents_for_children[tuple(children)[:-1]] = [left]
        else:
            if left in lexicon:
                lexicon[left].append(children[0])
            else:
                lexicon[left] = [children[0]]
        #l = [left] + [child for child in tuple(children)[:-1]]
        
        probabilities[tuple([left]) + tuple(children[:-1])] = float(children[-1])
    print("\n" + "*"*60)
    print "Grammar rules in tuple form:"
    print("*"*60 + "\n")
    pprint(grammar_rules)
    print("\n" + "*"*60)
    print "Rule parents indexed by children:"
    print("*"*60 + "\n")
    pprint(possible_parents_for_children)
    print("\n" + "*"*60)
    print("probabilities")
    print("*"*60 + "\n")
    pprint(probabilities)
    print("\n" + "*"*60)
    print "Lexicon"
    print("*"*60 + "\n")
    pprint(lexicon)

def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    #sentence = ['""'] + sentence
    
    
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    for i in range(len(sentence)):
        for l in lexicon:
            if sentence[i] in lexicon[l]:

                #print(probabilities[tuple([sentence[i]])])
                #print(lexicon[l], l)
                cells[i, i + 1].append([[l, sentence[i]], probabilities[(l, sentence[i])]])
    for j in range(2, len(sentence) + 1):
        for i in range(len(sentence) - j + 1):
                m = i + j 
                while m  - 1 > i:
                    #print(cells[i, m - 1], cells[m - 1, i + j])
                    for r,rule in enumerate(cells[i, m - 1]):
                        for o_r, other_rule in enumerate(cells[m - 1, i + j]):
                            #print("Printing rule and other_rule")
                            #print(rule[0][0], other_rule[0][0])
                            if (rule[0][0], other_rule[0][0]) in possible_parents_for_children:
                                new_rule = possible_parents_for_children[rule[0][0], other_rule[0][0]]
                                
                                for new_ru in new_rule:
                                    pr = probabilities[new_ru, rule[0][0], other_rule[0][0]]
                                    #print(rule[1],other_rule[1])

                                    updated_pr = pr*rule[1]*other_rule[1]
                                    #print(updated_pr)
                                    cells[i, i + j].append([[new_ru, [rule[0], other_rule[0]]], updated_pr])
                    m = m - 1

    #pprint(cells[0, len(sentence)])
    max_prob = 0.0
    best_rule = [None]
    for rule in cells[0, len(sentence)]:
        if 'S' == rule[0][0] and rule[1] > max_prob:
            best_rule = rule[0]
            max_prob = rule[1]
    return best_rule

