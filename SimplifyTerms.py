import collections

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def set_repr(x):
    return {frozenset(item) for item in x}

def move_constants_in_front(terms):
    cleared_terms = []

    for term in terms:
        new_term = []
        new_term.append(term[0])
        new_term.append('')

        constants = []
        for i in range(1, len(term)):
            if term[i][0] != 'g':
                constants.append(term[i])
            else:
                new_term.append(term[i])

        if len(constants) == 0:
            cleared_terms.append(term)
        else:
            constant_string = ""
            for i in range(len(constants) - 1):
                constant_string += constants[i] + '.'
            constant_string += constants[-1]
            new_term[1] = constant_string    
        
            cleared_terms.append(new_term)

    return cleared_terms

def get_permutation_parity(permutation):
    swaps = 0
    for i in range(len(permutation) - 1):
        for j in range(i + 1, len(permutation)):
            if permutation[j] < permutation[i]:
                swaps += 1
    return 1 - 2 * (swaps%2)

"""
returns 0 if the terms are different, and +-1 if the terms are equal in value, the minus sign meaning one is the opposite of the other
"""
def does_grassmann_terms_matches(term1, term2):
    indices = []

    for var in term2: #the case where a variable is in term1 but not in term2 is covered in the main loop
        if var[0] == 'g':
            if var not in term1:
                return 0

    for i in range(1, len(term1)):
        if term1[i][0] == 'g':
            j = 1
            while j < len(term2) and term2[j] != term1[i]:
                j += 1
            if j == len(term2):
                return 0
            indices.append(j)

    return get_permutation_parity(indices)



def simplify_terms(terms):
    simplified_terms = []
    cleared_terms = move_constants_in_front(terms)

    while(len(cleared_terms) > 0):
        term = cleared_terms[0]
        similar_terms = [term]
        indexes_to_keep = []
        for i in range(1, len(cleared_terms)):
            other_term = cleared_terms[i]
            terms_equality = does_grassmann_terms_matches(term, other_term)
            match terms_equality:
                case 0:
                    indexes_to_keep.append(i)
                case 1:
                    similar_terms.append(other_term)
                case -1:
                    neg_other_term = other_term
                    if neg_other_term[0] == '+':
                        neg_other_term[0] = '-'
                    else:
                        neg_other_term[0] = '+'
                    similar_terms.append(neg_other_term)
        cleared_terms = [cleared_terms[i] for i in indexes_to_keep]

        constant = ""
        if (len(similar_terms) > 0):
            for i in range(len(similar_terms) - 1):
                constant += similar_terms[i][0] + similar_terms[i][1]
            constant += similar_terms[len(similar_terms) - 1][0] + similar_terms[len(similar_terms) - 1][1]

        simplified_term = [term[0], constant]
        simplified_term += term[2:]
        simplified_terms.append(simplified_term)
    
    return simplified_terms

def sort_grassmann_terms(terms):
    while len(terms) > 0:
        cur_term = terms[0]
        terms_similar_to_cur = [cur_term]
        not_counted_terms = []

        #logs the position of the grassmann variables in the term in order to replace them in the compared term once the parity of the permutation is known
        grassman_indices_of_cur = []
        for n in range(len(cur_term)):
            if cur_term[n][0] == 'g':
                grassman_indices_of_cur.append(n)

        for i in range(1, len(terms)):
            permutation_parity = does_grassmann_terms_matches(cur_term, terms[i])
            if permutation_parity != 0: 
                matching_term = terms[i]

                if permutation_parity == -1:
                    if matching_term[0] == "+":
                        sign = "-"
                    else:
                        sign = "+"
                else:
                    sign = matching_term[0]

                matching_term[0] = sign
                
                #logs the position of the grassmann variables in the compared term, to replace them with the ordered ones 
                grassman_indices_of_match = []
                for n in range(len(matching_term)):
                    if matching_term[n][0] == 'g':
                        grassman_indices_of_match.append(n)

                for n in range(len(grassman_indices_of_cur)):
                    matching_term[grassman_indices_of_match[n]] = cur_term[grassman_indices_of_cur[n]]

                terms_similar_to_cur.append(matching_term)

            else:
                not_counted_terms.append(i)
        terms = [terms[i] for i in not_counted_terms]


"""
Equality of lists without order
"""
def lists_are_equal(l1, l2):
    return collections.Counter(l1) == collections.Counter(l2)

"""
Assumes that the grassmann variables are sorted in terms
"""
def simplify_constants(terms):
    rassembled_numbers_terms = []

    for term in terms:
        symbolsInTerm = [term[0], 0] #0 is the slot where the numeral constant will be 
        numbersInTerm = []
        for i in range(1, len(term)):
            if is_number(term[i]):
                numbersInTerm.append(term[i])
            else:
                symbolsInTerm.append(term[i])
        totNumber = 1
        for number in numbersInTerm:
            totNumber *= float(number)
        symbolsInTerm[1] = str(totNumber)

        rassembled_numbers_terms.append(symbolsInTerm) #Now the first element of a term is its sign and the second is its numeral constant

    simplified_terms = []
    while len(rassembled_numbers_terms) > 0:
        term = rassembled_numbers_terms[0]
        similar_terms = [term]
        indexes_to_keep = []
        for i in range(1, len(rassembled_numbers_terms)):
            if lists_are_equal(term[2:], rassembled_numbers_terms[i][2:]):
                similar_terms.append(rassembled_numbers_terms[i])
            else:
                indexes_to_keep.append(i)
        rassembled_numbers_terms = [rassembled_numbers_terms[i] for i in indexes_to_keep]

        constant = 0
        for similar_term in similar_terms:
            if similar_term[0] == '+':
                constant += float(similar_term[1])
            else:
                constant -= float(similar_term[1])

        if constant != 0.0:
            if constant < 0:
                constant = abs(constant)
                sign = '-'
            else:
                sign = '+'
            similar_terms[0][0] = sign
            similar_terms[0][1] = str(constant)
            simplified_terms.append(similar_terms[0])
    
    return simplified_terms
