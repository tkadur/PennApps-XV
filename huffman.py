from util import create_array
from util import JPEG_NATURAL_ORDER

class Huffman(object):
    BITS_DC_LUMINANCE   = [0x00, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0x00]
    BITS_DC_CHROMINANCE = [0x01, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0x00]
    BITS_AC_LUMINANCE   = [0x10, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]
    BITS_AC_CHROMINANCE = [0x11, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
    BITS = [BITS_DC_LUMINANCE,   BITS_AC_LUMINANCE, 
            BITS_DC_CHROMINANCE, BITS_AC_CHROMINANCE]

    VAL_DC_LUMINANCE   = range(12)
    VAL_DC_CHROMINANCE = range(12)
    VAL_AC_LUMINANCE  = [
            0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 
            0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07, 0x22, 0x71,
            0x14, 0x32, 0x81, 0x91, 0xa1, 0x08, 0x23, 0x42, 0xb1, 
            0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62, 0x72,
            0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 
            0x26, 0x27, 0x28, 0x29, 0x2a, 0x34, 0x35, 0x36, 0x37,
            0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 
            0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
            0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 
            0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x83,
            0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 
            0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3,
            0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 
            0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3,
            0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 
            0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
            0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf1, 
            0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa
        ]
    VAL_AC_CHROMINANCE = [
            0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 
            0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71, 0x13, 0x22,
            0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xa1, 0xb1, 0xc1, 
            0x09, 0x23, 0x33, 0x52, 0xf0, 0x15, 0x62, 0x72, 0xd1,
            0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 
            0x19, 0x1a, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x35, 0x36,
            0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 
            0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
            0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 
            0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a,
            0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 
            0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a,
            0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 
            0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba,
            0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 
            0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
            0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 
            0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa
        ]
    VAL  = [VAL_DC_LUMINANCE,   VAL_AC_LUMINANCE, 
            VAL_DC_CHROMINANCE, VAL_AC_CHROMINANCE]

    def __init__(self, width, height):
        self.buffer_put_bits = 0
        self.buffer_put_buffer = 0

        self.image_widht = width
        self.image_height = height
        self.init_huf()

    def init_huf(self):
        self.dc_matrix0 = create_array(0, 12, 2)
        self.dc_matrix1 = create_array(0, 12, 2)
        self.ac_matrix0 = create_array(0, 255, 2)
        self.ac_matrix1 = create_array(0, 255, 2)

        huffsize = [0] * 257
        huffcode = [0] * 257

        def cal(bits, val, matrix):
            p = 0
            for l in range(1, 17):
                for i in range(1, bits[l] + 1):
                    huffsize[p] = l
                    p += 1
            huffsize[p] = 0
            lastp = p

            code = 0
            si = huffsize[0]
            p = 0
            while huffsize[p]:
                while huffsize[p] == si:
                    huffcode[p] = code; p += 1
                    code += 1
                code <<= 1
                si += 1
            for p in range(0, lastp):
                matrix[val[p]][0] = huffcode[p]
                matrix[val[p]][1] = huffsize[p]

        cal(self.BITS_DC_LUMINANCE,   self.VAL_DC_LUMINANCE, self.dc_matrix0)
        cal(self.BITS_AC_LUMINANCE,   self.VAL_AC_LUMINANCE, self.ac_matrix0)
        cal(self.BITS_DC_CHROMINANCE, self.VAL_DC_CHROMINANCE, self.dc_matrix1)
        cal(self.BITS_AC_CHROMINANCE, self.VAL_AC_CHROMINANCE, self.ac_matrix1)

        self.dc_matrix = [self.dc_matrix0, self.dc_matrix1]
        self.ac_matrix = [self.ac_matrix0, self.ac_matrix1]

    def write_byte(self, out, byte):
        out.write(bytearray([byte]))

    def buffer_it(self, out, code, size):
        put_buffer = code
        put_bits = self.buffer_put_bits

        put_buffer &= (1 << size) - 1
        put_bits += size
        put_buffer <<= 24 - put_bits
        put_buffer |= self.buffer_put_buffer

        while put_bits >= 8:
            c = put_buffer >> 16 & 0xff
            self.write_byte(out, c)
            if c == 0xff:
                self.write_byte(out, 0)
            put_buffer <<= 8
            put_bits -= 8

        self.buffer_put_buffer = put_buffer
        self.buffer_put_bits = put_bits

    def flush_buffer(self, out):
        put_buffer = self.buffer_put_buffer
        put_bits = self.buffer_put_bits
        while put_bits >= 8:
            c = put_buffer >> 16 & 0xff
            self.write_byte(out, c)
            if c == 0xff:
                self.write_byte(out, 0)
            put_buffer <<= 8
            put_bits -= 8

        if put_bits > 0:
            c = put_buffer >> 16 & 0xff
            self.write_byte(out, c)

    def huffman_block_encoder(self, out, zigzag, prec, dc_code, ac_code):
        self.num_of_dc_tables = 2
        self.num_of_ac_tables = 2

        tmp = tmp2 = zigzag[0] - prec
        if tmp < 0:
            tmp = -tmp
            tmp2 -= 1

        nbits = 0
        while tmp:
            nbits += 1
            tmp >>= 1

        self.buffer_it(out, *self.dc_matrix[dc_code][nbits])
        if nbits:
            self.buffer_it(out, tmp2, nbits)

        r = 0
        for k in range(1, 64):
            tmp = zigzag[JPEG_NATURAL_ORDER[k]]
            if tmp == 0:
                r += 1
            else:
                while r > 15:
                    self.buffer_it(out, *self.ac_matrix[ac_code][0xf0])
                    r -= 16
                tmp2 = tmp
                if tmp < 0:
                    tmp = -tmp
                    tmp2 -= 1
                nbits = 1
                tmp >>= 1
                while tmp:
                    nbits += 1
                    tmp >>= 1
                i = (r << 4) + nbits
                self.buffer_it(out, *self.ac_matrix[ac_code][i])
                self.buffer_it(out, tmp2, nbits)
                r = 0

        if r > 0:
            self.buffer_it(out, *self.ac_matrix[ac_code][0])
