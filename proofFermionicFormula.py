from ComputeNonZeroGrassmanTerms import remove_terms_with_grassman_duplicates, remove_terms_by_integral, multiply_two_products, remove_ones_from_terms_advanced, remove_ones_from_terms_smart
from IdentifyRecurrence import print_comparison
from GenerateTerms import gen_string_single_sum, gen_string_double_sum, exponential_power_series, conj, exponential_power_series_depr

def generate_int_var(N, var):
    int_vars = []
    for i in range(1, N + 1):
        int_vars.append(["g"+str(i)+"_"+var, "g"+str(i)+"_"+var+"*"])

    return int_vars

def string_prod_mat(A, B):
    assert len(A[0]) == len(B)
    
    AB = [[[] for j in range(len(B[0]))] for i in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            result = []
            for k in range(len(A[0])):
                result += multiply_two_products(A[i][k], B[k][j])
            AB[i][j] = result

    return AB

def gen_matrix(letter, L):
    matrix = []
    for i in range(L):
        matrix.append([])
        for j in range(L):
            matrix[i].append([['+', letter + str(i+1) + str(j+1)]])

    return matrix

def grassmann_gen_row_vec(letter, L):
    vec = [[]]
    for i in range(L):
        vec[0].append([['+', 'g' + str(i+1) + '_' + letter]])

    return vec

def grassmann_gen_col_vec(letter, L):
    vec = []
    for i in range(L):
        vec.append([[['+', 'g' + str(i+1) + '_' + letter]]])

    return vec

L = 3

###################################
# COMPUTATION DONE BY INTEGRATION #
###################################

xi = 'xi'
chi = 'chi'
phi = 'phi'

closureTerm = exponential_power_series_depr(gen_string_single_sum(conj(xi), xi, [], L, '-'))
CdoubleSum = exponential_power_series_depr(gen_string_double_sum(conj(chi), xi, ['C'], L))
DdoubleSum = exponential_power_series_depr(gen_string_double_sum(conj(xi), phi, ['D'], L))

totalTerm = multiply_two_products(closureTerm, CdoubleSum)
totalTerm = multiply_two_products(totalTerm, DdoubleSum)


totalTerm = remove_terms_with_grassman_duplicates(totalTerm)

int_vars = generate_int_var(L, xi)
for int_var in int_vars:
    totalTerm = remove_terms_by_integral(totalTerm, int_var)

############################
# USING THE MATRIX FORMULA #
############################

chi = grassmann_gen_row_vec('chi*', L)
C = gen_matrix('C', L)
D = gen_matrix('D', L)
phi = grassmann_gen_col_vec('phi', L)

M = string_prod_mat(chi, C)
M = string_prod_mat(M, D)
M = string_prod_mat(M, phi)


hypothesisString = "("
for term in M[0][0]:
    hypothesisString += term[0] + '.'.join(term[1:]) + ' '*(term != M[0][0][-1])
hypothesisString += ")"

hypothesis = exponential_power_series_depr(hypothesisString)
#Simplify.print_similars(hypothesis)



print_comparison(remove_ones_from_terms_advanced(hypothesis), remove_ones_from_terms_advanced(totalTerm))
