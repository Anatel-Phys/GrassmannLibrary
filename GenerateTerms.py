from ComputeNonZeroGrassmanTerms import develop_product, termsString_to_termsProduct, remove_terms_with_grassman_duplicates, remove_ones_from_terms_smart, multiply_two_products
import SimplifyTerms

def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def conj(var):
    return var + '*'

def gen_string_single_sum(var1, var2, constants, L, sign = '+'):
    content_string = "("
    for i in range(1,L+1):
        content_string += sign
        for c in constants:
            content_string += c + str(i) + '.'
        content_string += 'g' + str(i) + '_' + var1 + '.'
        content_string += 'g' + str(i) + '_' + var2 + (i != L)*' '
    content_string += ')'

    return content_string

def gen_string_double_sum(var1, var2, double_idx_constants, L, sign = '+', idx1_constants = [], idx2_constants = [], idx_reversed_constants=[]):
    content_string = "("
    for i in range(1,L+1):
        for j in range(1,L+1):
            content_string += sign
            for cij in double_idx_constants:
                content_string += cij + str(i) + str(j) + '.'
            for cji in idx_reversed_constants:
                content_string += cji + str(j) + str(i) + '.'
            for ci in idx1_constants:
                content_string += ci + str(i) + '.'
            for cj in idx2_constants:
                content_string += cj + str(j) + '.'
            
            content_string += 'g' + str(i) + '_' + var1 + '.'
            content_string += 'g' + str(j) + '_' + var2 + (i != L or j != L)*' '
    content_string += ')'
    
    return content_string


"""
A faire, calcule le terme de puissance N en utilisant le terme de puissance N-1 gardé dans un buffer
"""
def exponential_power_series(contentString):
    terms = [['+']]
    power = 1

    last_power_term = [['+']]

    contentTerm = develop_product(termsString_to_termsProduct(contentString))

    while True:
        powerTerms = multiply_two_products(last_power_term, powerTerms)
        last_power_term = powerTerms

        if len(powerTerms) == 0:
            break

        for term in powerTerms:
            terms.append(term + [str(1/factorial(power))])
        power += 1

    SimplifyTerms.sort_grassmann_terms(terms)
    return remove_ones_from_terms_smart(SimplifyTerms.simplify_constants(terms))

def exponential_power_series_depr(contentString, min_power=0):
    terms = [['+']]
    power = 1
    while True:
        powerString = power * contentString
        powerTerms = develop_product(termsString_to_termsProduct(powerString))
        powerTerms = remove_terms_with_grassman_duplicates(powerTerms)

        if len(powerTerms) == 0 and power > min_power:
            break

        for term in powerTerms:
            terms.append(term + [str(1/factorial(power))])
        power += 1

    SimplifyTerms.sort_grassmann_terms(terms)
    return remove_ones_from_terms_smart(SimplifyTerms.simplify_constants(terms))

