from ComputeNonZeroGrassmanTerms import multiply_two_products

def string_prod_mat(A, B):
    assert len(A[0]) == len(B)
    
    AB = [[[] for j in range(len(B[0]))] for i in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            result = []
            for k in range(len(A[0])):
                terms = multiply_two_products(A[i][k], B[k][j])
                #if 0 dans un terme, on le vire
                terms = [term for term in terms if '0' not in term]
                result += terms
            AB[i][j] = result

    return AB

def gen_matrix(letter, L):
    matrix = []
    for i in range(L):
        matrix.append([])
        for j in range(L):
            matrix[i].append([['+', letter + str(i+1) + str(j+1)]])

    return matrix

def gen_diagonal_matrix(letter, L): 
    matrix = []
    for i in range(L):
        matrix.append([])
        for j in range(L):
            if i == j:
                matrix[i].append([['+', letter + str(i+1)]])
            else:
                matrix[i].append([['+', '0']])

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

