# template file for 6.02 PS1, Python Task 4 (LZW Compression/Decompression)
import sys
from optparse import OptionParser
import struct
import array

def compress(filename):
    """
    Compresses a file using the LZW algorithm and saves output in another file.
    Arguments: 
        filename: filename of file to compress.
    Returns:
        None.
    """
    table = {chr(i): i for i in xrange(256)}
    next_i = 256
    string = None
    try:
        f = open(filename, 'r')
        out = open(filename + '.zl', 'wb')
    except Exception as e:
        print e
        return
    for line in f:
        for c in line:
            if string is None:
                string = c
                continue
            next_string = string + c
            if next_string not in table:
                code = table[string]
                table[next_string] = next_i
                next_i += 1
                out.write(struct.pack('h', code))
                sys.stdout.write(string)
                string = c
            else:
                string = next_string
    out.write(struct.pack('h', table[string]))
    out.close()
    f.close()
        
def uncompress(filename):
    """
    Decompresses a file using the LZW algorithm and saves output in another file.
    Arguments: 
        filename: filename of file to decompress.
    Returns:
        None.
    """
    table = {i: chr(i) for i in xrange(256)}
    string = None
    next_i = 256
    with open(filename, 'rb') as f, open(filename + '.out', 'w') as out:
        bytestring = f.read(2)
        while len(bytestring) > 0:
            code = struct.unpack('h', bytestring)[0]
            if string is None:
                string = table[code]
                out.write(string)
                bytestring = f.read(2)
                continue
            if code in table:
                entry = table[code]
            else:
                entry = string + string[0]
            out.write(entry)
            table[next_i] = string + entry[0]
            next_i += 1
            string = entry
            bytestring = f.read(2)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", type="string", dest="fname", 
                      default="test", help="file to compress or uncompress")
    parser.add_option("-c", "--compress", action="store_true", dest="uncomp", 
                      default=True, help="compress file")
    parser.add_option("-u", "--uncompress", action="store_true", dest="uncomp", 
                      default=False, help="uncompress file")

    (opt, args) = parser.parse_args()
    
    if opt.uncomp == True:
        uncompress(opt.fname)
    else:
        compress(opt.fname)
