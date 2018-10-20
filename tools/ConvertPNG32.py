import SpreStationImage as SSI


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("png_file",  help="Input PNG file",   type=str)
parser.add_argument("rgab_file", help="Output PNG file",  type=str)
parser.add_argument("width",     help="compress width",   type=int)
parser.add_argument("height",    help="compress height",  type=int)

args = parser.parse_args()

f = open(args.png_file, 'rb')
img_data = f.read()
f.close()

img = SSI.resize_img(SSI.convertImage(img_data), (args.width,args.height))
img.save(args.rgab_file, 'PNG')


