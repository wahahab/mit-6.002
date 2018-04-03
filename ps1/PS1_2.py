# template file for 6.02 PS1, Python Task 2
import numpy,random
import PS1_tests
import pprint
from PS1_1 import huffman

# arguments:
#   encoding_dict -- dictionary mapping characters to binary encodings,
#                    as provided by your huffman procedure from PS1_1
#   encoded_message -- a numpy array of 0's and 1's representing the encoded message
# return:
#   a list of decoded symbols
def decode(encoding_dict,encoded_message):
    """
    Example:
    encoding_dict: {'A': [1, 1], 'C': [1, 0, 0], 'B': [0], 'D': [1, 0, 1]}
    encoded_msg: [1, 1, 0, 1, 0, 0, 1, 0, 1]
    returns 'ABCD'
    """
    msg = []
    tree = to_tree(encoding_dict)
    pprint.pprint(tree)
    pointer = tree
    for code in encoded_message:
        if pointer[code] is not None:
            pointer = pointer[code]
        else:
            msg.append(pointer['symbol'])
            pointer = tree[code]
    if pointer['symbol'] is not None:
        msg.append(pointer['symbol'])
    return msg

def to_tree(encoding_dict):
    left_dict = {}
    right_dict = {}
    symbol = None
    for key, val in encoding_dict.items():
        if len(val) == 0:
            symbol = key  
            continue
        if val[0] == 0:
            left_dict[key] = val[1:]
        else:
            right_dict[key] = val[1:]
    return {
        0: to_tree(left_dict) if left_dict else None,
        1: to_tree(right_dict) if right_dict else None,
        'symbol': symbol,
    }



if __name__ == '__main__':
    # start by building Huffman tree from probabilities
    plist = ((0.34,'A'),(0.5,'B'),(0.08,'C'),(0.08,'D'))
    cdict = huffman(plist)

    # test case 1: decode a simple message
    message = ['A', 'B', 'C', 'D']
    encoded_message = PS1_tests.encode(cdict,message)
    decoded_message = decode(cdict,encoded_message)
    assert message == decoded_message, \
           "Decoding failed: expected %s, got %s" % \
           (message,decoded_message)

    # test case 2: construct a random message and encode it
    message = [random.choice('ABCD') for i in xrange(100)]
    encoded_message = PS1_tests.encode(cdict,message)
    decoded_message = decode(cdict,encoded_message)
    assert message == decoded_message, \
           "Decoding failed: expected %s, got %s" % \
           (message,decoded_message)

    print "Tests passed!"
