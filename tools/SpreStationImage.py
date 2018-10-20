import re
import cStringIO
from PIL import Image
import xml.etree.ElementTree as ET

import numpy as np

import base64
import struct

def convertImage(str_data):
    return Image.open(cStringIO.StringIO(str_data)).convert('RGBA')

def resize_img(img, xy=None):
    if xy is not None and len(xy) == 2:
        ## Resising image with keeping aspect.
        if int(img.width) > int(xy[0]) or int(img.height) > int(xy[1]):
            resize_w = xy[0]
            resize_h = xy[1]
            w_range = float(img.width) / float(resize_w)
            h_range = float(img.height) / float(resize_h)
            if w_range > h_range:
                resize_h = round(float(resize_w) * float(img.height) / float(img.width))
            elif h_range > w_range:
                resize_w = round(float(resize_h) * float(img.width) / float(img.height))
            img = img.resize((int(resize_w), int(resize_h)), Image.LANCZOS)
    return img


def cmpress5515_png_data(image_data, xy=None):
    img = convertImage(image_data)
    img = resize_img(img, xy)

    image = np.asarray(img)

    height, width, pixlen = image.shape
    if pixlen is not 4:
        print "Error Error Error pix size is not 4(", pixlen, ")"
        return None, None, None

    R, G, B, A = np.split(image, [1,2,3], axis=2)
    R5 = R >> 3
    G5 = G >> 3
    B5 = B >> 3
    packed_data = None
    for lineR, lineG, lineB, lineA in zip(R5, G5, B5, A):
        for pixR, pixG, pixB, pixA in zip(lineR, lineG, lineB, lineA):
            mask = 1 if pixA[0] > 128 else 0
            tmp5515 = ((pixR[0] & 0x1F) << 11) | ((pixG[0] & 0x1F)<< 6) | ((mask & 1) << 5) | (pixB[0] & 0x1F)
            rgab5515 = np.uint16(tmp5515)
            if packed_data is None:
                packed_data = struct.pack('<H', rgab5515)
            else:
                packed_data += struct.pack('<H', rgab5515)

    return width, height, packed_data


def getImageDataFromXml(xml_data):
    return re.sub('^data:image/.+;base64,', '', xml_data.attrib['image']).decode('base64')


#======================================================

if __name__ == '__main__':
    f = open('copter.xml', 'r')
    XmlData = f.read()
    f.close()

    xml_root = ET.fromstring(XmlData)

    def show_node(node):
        if 'image' in node.attrib:
            img_xml = getImageDataFromXml(node)
            w, h, packed_img = cmpress5515_png_data(img_xml)
            of = open('rgb5515_data.dat', 'wb')
            of.write(packed_img)
            of.close()
            exit()
        print (node.tag, node.attrib)
        for child in node:
            show_node(child)

    show_node(xml_root)




