import SpreStationImage as SSI


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("png_file", help="PNG file", type=str)
parser.add_argument("rgab_file", help="RGAB5515 file", type=str)

args = parser.parse_args()

f = open(args.png_file, 'rb')
img_data = f.read()
f.close()

w, h, rgab5515 = SSI.cmpress5515_png_data(img_data)

import struct
packed_data = struct.pack('<I', w)
packed_data += struct.pack('<I', h)
packed_data += rgab5515

of = open(args.rgab_file, 'wb')
of.write(packed_data)
of.close()

