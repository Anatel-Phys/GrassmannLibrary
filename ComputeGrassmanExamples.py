from ComputeNonZeroGrassmanTerms import develop_exponential, termsString_to_termsProduct, develop_product, remove_terms_with_grassman_duplicates, remove_terms_by_integral, remove_ones_from_terms, string_to_terms

# Note : a first-time reader might find useful to read the script description and rules in the ComputeNonZeroGrassmanTerms script before reading throught the example. A look at the conventions section might also prove itself worth during the reading of the example.
# It is the hope of the author that the example will clear out doubts and uncertainties left in the reader's mind from the reading of the two sections mentionned above
#
# First, let's find ourselves a Grassman product term. let's imagine we have two quadrature Grassman variables, phi_i* and phi_f, describing a two-site system. Each variable thus have two components. 
# Following the conventions described in the script, we denote those components g1_phi_i*, g2_phi_i*, and g1_phi_f, g2_phi_f. 
# Note that the g indicates a Grassmann variables. Thus, we might as well forget about the greek letter naming convnetion and denote those variables g1_i*, g2_i*, and g1_f, g2_f to unclutter things. 
# To be sure we're at the same page, g1_i* is now representing the 1st component of the Grassmann variable phi_i* This convention will now be adopted throughout this example code, as it particularly simplifies the index notation
#
# Now begins the hard part : translating a grassmann product into a string that can be understood and used by the script.
# Let's supose those two variables appear in a closure relation. The fermionic coherent state closure relations come with terms of the form exp(- Sum g_i* g_i)
# For a reader not familiar with those quadrature states/closure relations, Sum g_1* g_1 represents the sum over all components of g_i* g_i, i.e the sum (g1_i* g1_i) + (g2_i* g2_i) + ...
# Be careful to what represents the name of the variable and what represents the index. in g2_i*, we have : 
#                                                                                                       - the Grassmann Prefix (see rules) : 'g'
#                                                                                                       - the index 2, followed by an underscore
#                                                                                                       - the variable name, '1*'
#
# If we describe a two-site system, there are two components to each variable. We thus write the exponentials as

expString_i = "(+1 -g1_i*.g1_i)(+1 -g2_i*.g2_i)"
expString_f = "(+1 -g1_f*.g1_f)(+1 -g2_f*.g2_f)"

# Alternatively, we could have used the develop_exponential function (yielding the exact same result) :

expStringByFunc_i = develop_exponential(vars=['i*', 'i'], N=2, sign='-')
expStringByFunc_f = develop_exponential(vars=['f*', 'f'], N=2, sign='-')

# However, all the terms in the above products are non-zero and the script is not yet useful. To spice up things, let's create another termString that we will add to the first, representing for instance a product of exponentials
# Besides, it is a good practice to split up the distinct terms into different strings in order to facilitate the error-checking phase.
# This new term will contain the scalar product between a state vector g_i and another vector g_o. it is of the form exp(+ Sum g_i* g_o). We thus write it, for two sites

otherExpString = "(+1 +g1_i*.g1_o)(+1 +g2_i*.g2_o)"

# Or, alternatively,

otherExpStringByFunc = develop_exponential(vars=['i*', 'o'], N=2, sign='+')

# We can now combine all of our terms into one string : 

termsString = expString_i + expString_f + otherExpString

# We now have a proper term string that could already cause a (small) headache to a physicist, dealing with signs and the high number of term choices.
# Let's take a look at how to handle the computations using the script.
#
# First step : translate the string into a termsProduct (a list, cfr script rules)

termsProduct = termsString_to_termsProduct(termsString)

print("Terms Product (following the rules stated in the script) :")
print(termsProduct)

# Second step : develop the product

developedProduct = develop_product(termsProduct)

print("\n\n")
print("Terms in the developed product (a lot of them are zero and need to be removed as we will do shortly) :")
print(developedProduct)

# Those steps can be performed at once if one do not need to access the intermediate step

developedProduct =  string_to_terms(termsString)

# Third step : clear all the terms containing duplicates of Grassmann variables

noDuplicates = remove_terms_with_grassman_duplicates(developedProduct)

print("\n\n")
print("Non-zero terms :")
print(noDuplicates)

# An optionnal step to unclutter things is to remove ones from the terms, using the remove_ones_from_terms function

noDuplicatesOrOnes = remove_ones_from_terms(noDuplicates)

print("\n\n")
print("Non-zero terms without annoying ones")
print(noDuplicatesOrOnes)

# Last (optionnal) step : perform the eventual Grassmann integration needed. The remaining terms are integrated, the null terms are gone. 
# For instance, let's integrate over g1_i*, g2_i*, g1_f and g2_f. This will integrate over those variables in left to right order
# Note that even if you kept the ones until now, the remove_terms_by_integral function will remove them as it is required for it's algorithm

nonZeroTerms = remove_terms_by_integral(noDuplicates, integratedVariables=['g1_i*', 'g2_i*', 'g1_f', 'g2_f'])

print("\n\n")
print("Non-zero terms after integration over g1_i*, g2_i*, g1_f and g2_f :")
print(nonZeroTerms)

