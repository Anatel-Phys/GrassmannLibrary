######################
# SCRIPT DESCRIPTION #
######################
#
# This script was written in order to simplify expressions containing several Grassmann variables in the context of fermionic coherent states in the Feynman Path Integral formalism.
# The system of interest is a periodic well potential containing fermions described by Grassmann variables
# The main structure of the usage of the script is as following : 
# - express your product of terms in a string following the conventions written below, e.g (+1 -g1*.g1)(+1 +g1.g2)
# - convert it into a list of terms using the termsString_to_termsProduct function. The product is now encoded under the form of a list as described in the conventions section
# - develop the product using the develop_product function, producing a new list
# - in this new list, eliminate every term containing more than one of some Grassmann variables, using remove_terms_with_grassman_duplicates
# - if you also want to keep terms that will be non-zero after integrating on some of the variables, use the remove_terms_by_integral function
#
#
################
# SCRIPT RULES #
################
#
# 1) TERMS STRINGS
# In the string form, each character counts, and all the rules for encoding the product must be followed.
# - The sign of every number/variable is specified, attached to the number/variable. 
#           Ex: phi_1 is denoted +phi_1
# - Spaces are used TO SEPARATE NUMBERS/VARIABLES ONLY.
# - every term is the product is enclosed by some parenthesis, even if it is alone. 
#           Ex: 2*(1 + phi_1) is denoted (+2)(+1 +phi_1)
#           Note that the spaces are used only to separate numbers/variables and for nothing else. Misused spaces might result in incorrect results
# - Grassmann variables are treated as such in the script only when beginning by a g
#           Ex: a variable denoted phi_1 could be encoded by g_phi_1 or simply g_1
# - Product of variables inside the terms are denoted by the character '.'
#           Ex: (1 + phi_1 * phi_2) is denoted (+1 +phi_1.phi_2)
#
# 2) TERMS LISTS
# There is two different types of term lists: a list representing the product of the terms and a list representing the sum of the terms.
# - The list representing product of terms is obtained by translating the termsString into a list
#           It is of the form [term1, term2, ...] where term1 might itself be a sum of terms, e.g [['+', '1'], ['-', 'g_1', 'g_2']] (meaning 1 - g_1*g_2)
# - Coming right after, the list containing a sum of terms is obtained by developing the product list above using the develop_product function
#           It is of the form [term1, term2, ...] where term1 is a product of number and variables, e.g ['+', '1', 'g_1', g_2'] (meaning +1*g_1*g_2)
#
#
######################
# SCRIPT CONVENTIONS #
######################
# - the Grassmann Variables are often considered as 1-D vectors in the examples, the reason being that in the context of periodic wells, quadrature states are used. Those states contain 1 variable per well, and those variables are packed together in a vector.
#   The naming convention used is the following: 1st, 'g' to indicate a Grassmann Variable. Then, the vector index. Then, an underscore '_', and finally the variable's name.
#   Ex: the i'th variable of the vector phi_1* would be denoted 'gi_phi_1*
#   However, this is only a naming convention and one can use the script without ever using this notation
# - the name termsString denotes the string containing the user's product of numbers, variables and Grassmann Variables. 
# - the name termsProduct denotes the list of all the terms that represents the product and that will be developed
# - the name developedProducts represent the list obtained after using the develop_product function
# - the star symbol '*' denotes Grassmann conjugate variables

from SimplifyTerms import is_number

"""
Increments the list used to generate every possible combination of terms in the product considered. It is basically like incrementing a binary number represented by a list, but here some digits can take more than two values

termChoice : a list of the format e.g [0,1,0,2,...] that expresses the term you get by combining the 1st element of term one, the 2nd of term two, then the 1st of term three, than the 3rd of term four etc Careful that it is indexed from 0 to termMax - 1

termMax : a list of the form [2,2,3,1,2,...] the number of element per term so that termChoice doesn't give out of range indices (e.g taking the 3rd element of a 2-element term). Note that elements with number 
"""
def hlp_increment_termChoice_list(termChoice, termMax):
    i = 0 #index of the first not max digit
    while i < len(termMax) and termChoice[i] == termMax[i] - 1:
        i += 1
    if i >= len(termMax):
        return False
    else:
        termChoice[i] += 1
        for j in range(i): #set all the terms before the one incremented to be 0 (as in increment of binary number)
            termChoice[j] = 0
        return True

"""
Parse a string of the form 
    productString : "(+1 +phi)(-1 -phi2xphi3 +2)(...)
to produce a list of the form [[['+', '1'], ['+','phi1']], [['-', '1'], ['-', 'phi2', 'phi3'], ['+', '2']]]
"""
def termsString_to_termsProduct(productString):
    termsInProduct = [] #Final result
    unSplittedTerms = [] #terms of the form '+1', '-phi1xphi2'
    
    for i in range(len(productString)):
        if productString[i] == '(':
            termStartIdx = i + 1
            while (productString[i] != ')'):
                i += 1
            termEndIdx = i
            termString = productString[termStartIdx:termEndIdx]
            newTerm =  termString.split(' ')
            unSplittedTerms.append(newTerm)

    for term in unSplittedTerms:
        splittedTerm = []
        for number in term:
            numberRepr = []
            numberRepr.append(number[0]) #appends the sign
            numberWithoutSign = number[1:]
            numberRepr = numberRepr + numberWithoutSign.split('.') #splits the string if there is some .'s representing products
            splittedTerm.append(numberRepr)
        termsInProduct.append(splittedTerm)

    return termsInProduct

"""
Develop all the terms in a product generated by termsString_to_termsProduct
"""
def develop_product(termsInProduct):
    combinations = []
    termChoice = [0 for term in termsInProduct]
    termMax = [len(term) for term in termsInProduct]

    while (True):
        #newCombination = [termsInProduct[i][termChoice[i]] for i in range(len(termChoice))] #creates a new combination using the index in termChoice for each term of the initial term list

        newCombination = []
        sign = 1
        for i in range(len(termChoice)):
            if termsInProduct[i][termChoice[i]][0] == '-':
                sign *= -1
            #print(termsInProduct[i][termChoice[i]])
            newCombination = newCombination + termsInProduct[i][termChoice[i]][1:]
        combinationSign = []
        if sign == 1:
            combinationSign = ['+']
        else:
            combinationSign = ['-']

        combinations.append(combinationSign + newCombination)

        if not hlp_increment_termChoice_list(termChoice, termMax):
            break

    return combinations

def string_to_terms(string):
    prod_string = termsString_to_termsProduct(string)
    return develop_product(string)


"""
Eliminate all the duplicate variables assuming all the non-1 terms are grassmann variables
"""
def remove_terms_with_grassman_duplicates(termsInProduct):
    nonZeroTerms = []

    for term in termsInProduct:
        termContainsDuplicate = False
        for i in range(1,len(term) - 1):
            if term[i][0] == 'g':
                for j in range(i + 1, len(term)):
                    if term[j][0] == 'g':
                        if term[j] == term[i]:
                            termContainsDuplicate = True
                            break
        if not termContainsDuplicate:
            nonZeroTerms.append(term)

    return nonZeroTerms

"""
Eliminates integrated variables from the provided terms and change the sign depending on the permutations needed to integrate. NOTE THAT THE ONES NEED TO BE REMOVED WITH remove_ones_from_terms. THIS IS FORCED IN THE BEGINNING OF THE FUNCTION
    integratedVariables : list of the names of variables to integrate, starting from the leftmost.
                            ex : ['g1_1', 'g2_1'] will first compute the integral over g1_1
"""
def remove_terms_by_integral(developedTerms, integratedVariables):
    nonZeroTerms = []

    developedTerms = remove_ones_from_terms(developedTerms)

    for term in developedTerms:
        variableInTerm = True
        for variable in integratedVariables:
            if variable not in term:
                variableInTerm = False
                break
        if variableInTerm:
            nonZeroTerms.append(term)

    for term in nonZeroTerms: #handcrafted algorithm to compute the swaps required to bring the integrated variable in front of the term
        termWithonlyGrassmannianVars = [var for var in term if var[0] == 'g'] #To remove the constants from the computation, as they are not grassmann variables and should not contribute to the amount of permutation required to bring the variable in front

        termPositions = []
        for i in range(len(integratedVariables)):
            j = 0
            while termWithonlyGrassmannianVars[j] != integratedVariables[i]:
                j += 1
            termPositions.append(j + 1) #need for + 1 as the + 1 was in the fact that the first index is dedicated to the sign but now I changed the method and I create a duplicate with only the grassmannian terms

        for i in range(len(termPositions)):
            numberOfSmallerIndices = 0
            for j in range(i):
                if termPositions[j] < termPositions[i]:
                    numberOfSmallerIndices += 1
            termPositions[i] -= numberOfSmallerIndices

        parity = 0
        for index in termPositions:
            parity += index
        parity -= len(termPositions) #step equivalent to removing one from each index as they are summed over
        parity = parity%2

        if parity == 1:
            if term[0] == '+':
                term[0] = '-'
            else:
                term[0] = '+'
            
        for variable in integratedVariables:
            term.remove(variable)

    return nonZeroTerms

"""
Removes all the ones in the terms of the developed product developedTerms
"""
def remove_ones_from_terms(developedTerms):
    cleanedTerms = []

    for term in developedTerms:
        cleanedTerm = []
        for variable in term:
            if variable != '1':
                cleanedTerm.append(variable)
        cleanedTerms.append(cleanedTerm)

    return cleanedTerms   

"""
Removes all the ones in the terms of the developed product developedTerms EXCEPT the ones that are only only 1 without other variables or constants. Works best when the ones have been reassembled in front of the term
"""
def remove_ones_from_terms_smart(developedTerms):
    cleanedTerms = []

    for term in developedTerms:
        cleanedTerm = []
        for i in range(len(term)):
            if (term[i] != '1' and term[i] != '1.0'):
                cleanedTerm.append(term[i])
        cleanedTerms.append(cleanedTerm)

    return cleanedTerms

def remove_ones_from_terms_advanced(developedTerms):
    cleanedTerms = []

    for term in developedTerms:
        cleanedTerm = []
        for i in range(len(term)):
            if is_number(term[i]):
                if abs(float(term[i]) - 1) > 1e-8:
                    cleanedTerm.append(term[i])
            else:
                cleanedTerm.append(term[i])
        cleanedTerms.append(cleanedTerm)

    return cleanedTerms

"""
Develops an exponential of Grassmann variables of the form exp(sign * Sum over N of (var1n * var2n * ...)). This function's main purpose is to accelerate typing of terms containing lots of closure relation/scalar product between fermionic coherent states
    vars : a list containing the terms in the exponential
    N : the max index of the sum in the exponential
    sign : the sign in front of the term in the exponential
For instance, vars = [1*,2,f], N = 2 and sign = '-' will produce the following : 
(+1 -g1_1*.g1_2.g1_f)(+1 -g2_1*.g2_2.g2_f)
"""
def develop_exponential(vars, N, sign):
    result = ""
    for i in range(N):
        result += "(" + "+1" + " " + sign
        for j in range(len(vars) - 1):
            result += 'g' + str(i + 1) + '_' + vars[j] + '.'
        result += 'g' + str(i + 1) + '_' + vars[len(vars) - 1]
        result += ')'
    return result


"""
Function to combine products as produced by the develop_product function
"""
def multiply_two_products(product_1, product_2):
    terms = []
    for term_1 in product_1:
        for term_2 in product_2:
            new_term = []

            if term_1[0] == term_2[0]:
                new_term.append('+')
            else:
                new_term.append('-')

            for i in range(1, len(term_1)):
                new_term.append(term_1[i])
            for i in range(1, len(term_2)):
                new_term.append(term_2[i])

            terms.append(new_term)
    
    return terms

"""
Function to combine products as produced by the develop_product function
"""
def multiply_N_products(products):
    result = products[0]

    for i in range(1, len(products)):
        result = multiply_two_products(result, products[i])
    
    return result
