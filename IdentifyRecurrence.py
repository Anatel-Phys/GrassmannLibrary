from ComputeNonZeroGrassmanTerms import hlp_increment_termChoice_list
import collections
import json

def lists_are_equal(l1, l2):
    return collections.Counter(l1) == collections.Counter(l2)


"""
Function to handle lists of the form [[+a,+b],[+c,-d]] that represents products. The output will be [[+,a,c],[-,a,d],[+,b,c],[-,b,d]]
"""
def multiply_products_in(product):
    if not len(product) > 0:
        return []

    termMax = [len(product[i]) for i in range(len(product))]
    termChoice = [0 for i in range(len(product))]

    terms = []

    while True:
        term = []
        parity = 0
        for i in range(len(termChoice)):
            parity += product[i][termChoice[i]][0] == '-'

        if parity%2 == 0:
            term.append('+')
        else:
            term.append('-')

        for i in range(len(termChoice)):
            if '.' in product[i][termChoice[i]]:
                splittedTerms = product[i][termChoice[i]][1:].split('.')
                term += splittedTerms
            else:
                term.append(product[i][termChoice[i]][1:])
        
        terms.append(term)
        if not hlp_increment_termChoice_list(termChoice, termMax):
            break
    
    return terms

def compare_terms(t1, t2):
    terms1 = t1.copy()
    terms2 = t2.copy()
    terms_in_common = []

    termsFound = True
    #min_i = 0 wip to optimize func

    while termsFound:
        termsFound = False
        for i in range(len(terms1)):
            for j in range(len(terms2)):
                if lists_are_equal(terms1[i][1:], terms2[j][1:]):
                    #min_i = i
                    cur_term1 = terms1[i]
                    cur_term2 = terms2[j]
                    termsFound = True
                    break
            if termsFound:
                break
        
        if termsFound:
            terms_in_common.append(cur_term1)
            terms1.remove(cur_term1)
            terms2.remove(cur_term2)

    return terms_in_common, terms1, terms2

def print_comparison(t1, t2):
    t_common, t_only_1, t_only_2 = compare_terms(t1, t2)

    print("Terms in common : ")
    print(t_common)
    print("\nTerms only in first term : ")
    print(t_only_1)
    print("\nTerms only in second term : ")
    print(t_only_2)

def compare_terms_no_sign(t1, t2):
    terms1 = t1.copy()
    terms2 = t2.copy()
    terms_in_common = []

    termsFound = True
    #min_i = 0 wip to optimize func

    while termsFound:
        termsFound = False
        for i in range(len(terms1)):
            for j in range(len(terms2)):
                if lists_are_equal(terms1[i][1:], terms2[j][1:]):
                    #min_i = i
                    cur_term1 = terms1[i]
                    cur_term2 = terms2[j]
                    termsFound = True
                    break
            if termsFound:
                break
        
        if termsFound:
            terms_in_common.append(cur_term1)
            terms1.remove(cur_term1)
            terms2.remove(cur_term2)

    return terms_in_common, terms1, terms2



def save_list(list, file_name):
    with open(file_name + ".txt", 'w') as f:
        list_string = json.dumps(list)
        f.write(list_string)

def load_list(file_name):
    with open(file_name + ".txt") as f:
        list_string = f.read()
        l = json.loads(list_string)

    return l

