from ComputeNonZeroGrassmanTerms import develop_exponential, termsString_to_termsProduct, develop_product, remove_terms_with_grassman_duplicates, remove_terms_by_integral, remove_ones_from_terms, multiply_two_products, multiply_N_products, remove_ones_from_terms_smart, remove_ones_from_terms_advanced
from IdentifyRecurrence import compare_terms, save_list, load_list, lists_are_equal, print_comparison
from GenerateTerms import gen_string_single_sum, gen_string_double_sum, exponential_power_series_depr, conj
from QuickMatrixLib import string_prod_mat, gen_matrix, grassmann_gen_col_vec, grassmann_gen_row_vec, gen_diagonal_matrix

def gen_string_general_sum(vars, constants, L, sign = '+', two_first_indices_constants = [], two_last_indices_constants = []):
    content_string = "("
    for i in range(1,L+1):
        for j in range(1,L+1):
            for k in range(1,L+1):
                for l in range(1,L+1):
                    content_string += sign
                    for c in constants:
                        content_string += c + str(i) + str(j) + str(k) + str(l) + '.'
                    for c in two_first_indices_constants:
                        content_string += c + str(i) + str(j) + '.'
                    for c in two_last_indices_constants:
                        content_string += c + str(k) + str(l) + '.'

                    indices = [i,j,k,l] #TODO généraliser les boucles intriquées

                    for n in range(len(vars)):
                        content_string += 'g' + str(indices[n]) + '_' + vars[n] + ('.' * (n!=len(vars) - 1))

                    content_string += (i != L or j != L or k != L or l != L) * ' '
    content_string += ')'
    
    return content_string

def gen_string_the_special_sum(vars, constants, L, sign = '+', two_first_indices_constants = [], two_last_indices_constants = []):
    content_string = "("
    for i in range(1,L+1):
        for j in range(1,L+1):
            for k in range(1,L+1):
                for l in range(1,L+1):
                    content_string += sign
                    for c in constants:
                        content_string += c + str(i) + str(j) + str(k) + str(l) + '.'
                    for c in two_first_indices_constants:
                        content_string += c + str(i) + str(j) + '.' + 'F' + str(i) + '.' + 'F' + str(j) + '.'
                    for c in two_last_indices_constants:
                        content_string += c + str(k) + str(l) + '.'

                    indices = [i,j,k,l] #TODO généraliser les boucles intriquées

                    for n in range(len(vars)):
                        content_string += 'g' + str(indices[n]) + '_' + vars[n] + ('.' * (n!=len(vars) - 1))

                    content_string += (i != L or j != L or k != L or l != L) * ' '
    content_string += ')'
    
    return content_string

def generate_int_var(N, var):
    int_vars = []
    for i in range(1, N + 1):
        int_vars.append(["g"+str(i)+"_"+var, "g"+str(i)+"_"+var+"*"])

    return int_vars

L = 3

xi_f = 'xi_f'
chi = 'chi'
xi_i = 'xi_i'

closure = exponential_power_series_depr(gen_string_single_sum(conj(chi), chi, [], L, sign='-'))
onebody_exp = exponential_power_series_depr(gen_string_single_sum(conj(xi_f), chi, ['F'], L)) 
quad_exp = exponential_power_series_depr(gen_string_general_sum([conj(chi), conj(chi), xi_i, xi_i], [], L, two_first_indices_constants=['C'], two_last_indices_constants=['D']), min_power=2)
chi_xif_scal = exponential_power_series_depr(gen_string_single_sum(conj(chi), xi_i, [], L)) #l'autre est pas nécessaire vu qu'on peut faire rentrer la matrice identité dans la matrice des F

terms = multiply_N_products([closure, onebody_exp, quad_exp, chi_xif_scal])

terms = remove_terms_with_grassman_duplicates(terms)
int_vars = generate_int_var(L, chi)
for vars in int_vars:
    terms = remove_terms_by_integral(terms, vars)


#HYPOTHESIS

def string_prod_mats(matrices):
    M = string_prod_mat(matrices[0], matrices[1])
    for i in range(2, len(matrices)):
        M = string_prod_mat(M, matrices[i])
    return M

v_xi_f_T = grassmann_gen_row_vec(conj(xi_f), L)
v_xi_f = grassmann_gen_col_vec(conj(xi_f), L)
F = gen_diagonal_matrix('F', L)
C = gen_matrix('C', L)
D = gen_matrix('D', L)
v_xi_i = grassmann_gen_col_vec(xi_i, L)
v_xi_i_T = grassmann_gen_row_vec(xi_i, L)

M = string_prod_mats([v_xi_f_T, F, C, F, v_xi_f, v_xi_i_T, D, v_xi_i])

hypothesisString = "("
for term in M[0][0]:
    hypothesisString += term[0] + '.'.join(term[1:]) + ' '*(term != M[0][0][-1])
hypothesisString += ")"
print(hypothesisString)


hypothesis2 = exponential_power_series_depr(hypothesisString)

hypothesis1 = exponential_power_series_depr(gen_string_single_sum(conj(xi_f), xi_i, ['F'], L))
hypothesis = multiply_two_products(hypothesis1, hypothesis2)
hypothesis = remove_terms_with_grassman_duplicates(hypothesis)

common, onlyTerms, onlyHypothesis = compare_terms(remove_ones_from_terms_advanced(terms), remove_ones_from_terms_advanced(hypothesis))
print("only in terms:")
print(onlyTerms)
print("only in hypothesis:")
print(onlyHypothesis)
print("in common:")
print(common)
