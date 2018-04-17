# template for 6.02 rectangular parity decoding using error triangulation
import PS2_tests
import numpy

def is_error(row, parity_bit):
    result = reduce(lambda result, bit: result != bit, row, 0)
    return (result != parity_bit) == 1

def rect_parity(codeword,nrows,ncols): 

    corrected = False

    get_parity_bit = lambda codeword, t, idx: codeword[nrows * ncols + nrows + idx] \
        if t == 'col' else codeword[nrows * ncols + idx]
    get_row = lambda codeword, j: codeword[j * ncols: j * ncols + ncols]
    get_col = lambda codeword, i: codeword[i: nrows * ncols: ncols]

    corrected_code = []
    for j in xrange(nrows):
        parity_bit = get_parity_bit(codeword, 'row', j)
        row = get_row(codeword, j)
        if is_error(row, parity_bit):
            corrected_row = []
            for i in xrange(ncols):
                col = get_col(codeword, i)
                parity_bit = get_parity_bit(codeword, 'col', i)
                if is_error(col, parity_bit):
                    if corrected: return codeword[:nrows * ncols];
                    corrected_row.append(int(not row[i]))
                    corrected = True
                else:
                    corrected_row.append(row[i])
            corrected_code.extend(corrected_row)
        else:
            corrected_code.extend(row)
#    for i in xrange(ncols):
#        col = get_col(codeword, i)
#        parity_bit = get_parity_bit(codeword, 'col', i)
#        if is_error(col, parity_bit):
#            corrected_col = []
#            for j in xrange(nrows):
#                row = get_row(codeword, j)
#                parity_bit = get_parity_bit(codeword, 'row', j)
    return corrected_code


if __name__ == '__main__':
    PS2_tests.test_correct_errors(rect_parity)
