# template file for 6.02 PS1, Python Task 1
import PS1_tests

# arguments:
#   plist -- sequence of (probability,object) tuples
# return:
#   a dictionary mapping object -> binary encoding
def huffman(pList):
    """
    Example:
    plist: ((0.50,'A'),(0.25,'B'),(0.125,'C'),(0.125,'D'))
    returns: {'A': [0], 'B': [1, 0], 'C': [1, 1, 0], 'D': [1, 1, 1]} 
    """
    sorted_pList = sorted(pList, key=lambda p: p[0], reverse=True)
    codebook = {}
    prefix = []
    # if input is empty
    if len(sorted_pList) == 0:
        return code_book
    while len(sorted_pList) > 1:
        probA, symbolA = sorted_pList.pop()
        probB, symbolB = sorted_pList.pop()
        inserted = False
        for i in xrange(len(sorted_pList) - 1, -1, -1):
            prob, _ = sorted_pList[i]
            if prob > probA + probB:
                sorted_pList.insert(i + 1, (probA + probB, (symbolA, symbolB)))
                inserted = True
                break
        if not inserted:
            sorted_pList.insert(0, (probA + probB, (symbolA, symbolB)))
    codebook = tree_to_codebook(sorted_pList[0][1], codebook, [])
    # special case, if len(pList) == 1
    return codebook

def tree_to_codebook(tree, codebook, prefix):
    left, right = tree
    if type(left) == tuple:
        codebook = tree_to_codebook(left, codebook, prefix + [0])
    else:
        codebook[left] = prefix + [0]
    if type(right) == tuple:
        codebook = tree_to_codebook(right, codebook, prefix + [1])
    else:
        codebook[right] = prefix + [1]
    return codebook
    

if __name__ == '__main__':
    # test case 1: four symbols with equal probability
    PS1_tests.test_huffman(huffman,
                           # symbol probabilities
                           ((0.25,'A'),(0.25,'B'),(0.25,'C'),
                            (0.25,'D')),
                           # expected encoding lengths
                           ((2,'A'),(2,'B'),(2,'C'),(2,'D')))

    # test case 2: example from section 22.3 in notes
    PS1_tests.test_huffman(huffman,
                           # symbol probabilities
                           ((0.34,'A'),(0.5,'B'),(0.08,'C'),
                            (0.08,'D')),
                           # expected encoding lengths
                           ((2,'A'),(1,'B'),(3,'C'),(3,'D')))

    # test case 3: example from Exercise 5 in notes
    PS1_tests.test_huffman(huffman,
                           # symbol probabilities
                           ((0.07,'I'),(0.23,'II'),(0.07,'III'),
                            (0.38,'VI'),(0.13,'X'),(0.12,'XVI')),
                           # expected encoding lengths
                           ((4,'I'),(3,'II'),(4,'III'),
                            (1,'VI'),(3,'X'),(3,'XVI')))

    # test case 4: 3 flips of unfair coin
    phead = 0.9
    plist = []
    for flip1 in ('H','T'):
        p1 = phead if flip1 == 'H' else 1-phead
        for flip2 in ('H','T'):
            p2 = phead if flip2 == 'H' else 1-phead
            for flip3 in ('H','T'):
                p3 = phead if flip3 == 'H' else 1-phead
                plist.append((p1*p2*p3,flip1+flip2+flip3))
    expected_sizes = ((1,'HHH'),(3,'HTH'),(5,'TTT'))
    PS1_tests.test_huffman(huffman,plist,expected_sizes)
