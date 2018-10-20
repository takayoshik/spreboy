import re
import cStringIO
import xml.etree.ElementTree as ET

import base64
import struct

class SnapNode:

    def __init__(self, tag_name):
        self.attrib_name_list = []
        self.child_tag_list = []
        self.tag_name = ""
        self.tag_name = tag_name

    def add_list_item(self, tgt_list, child):
        if child in tgt_list:
            pass
        else:
            tgt_list.append(child)

    def add_child_tag(self, child):
        self.add_list_item(self.child_tag_list, child)

    def add_attrib(self, attrib):
        self.add_list_item(self.attrib_name_list, attrib)

    def show_list(self, lst, name):
        if len(lst) > 0:
            print "    -", name, "-"
            for item in lst:
                print "         * ", item

    def print_all(self):
        print "[", self.tag_name, "]"
        self.show_list(self.attrib_name_list, "Attribute")
        self.show_list(self.child_tag_list, "Child tag")

all_nodes = {}

def set_node(nodes, tgt_xmlnode):
    if tgt_xmlnode.tag not in nodes:
        # print "Create new tag", tgt_xmlnode.tag
        nodes[tgt_xmlnode.tag] = SnapNode(tgt_xmlnode.tag)

    snap = nodes[tgt_xmlnode.tag]

    show_detail = False
    # if snap.tag_name == 'comment':
    #     show_detail = True

    for child in tgt_xmlnode:
        if show_detail:
            print child.tag
        snap.add_child_tag(child.tag)

    if show_detail:
        print "   ", tgt_xmlnode.attrib

    for attrib in tgt_xmlnode.attrib:
        if show_detail:
            print "     AAA ", attrib
        snap.add_attrib(attrib)


def analize_attrib_child(node):
    set_node(all_nodes, node)
    for child in node:
        analize_attrib_child(child)


#======================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", help="Snap exported xml file", type=str)

    args = parser.parse_args()

    f = open(args.xml_file, 'r')
    XmlData = f.read()
    f.close()

    xml_root = ET.fromstring(XmlData)

    analize_attrib_child(xml_root)

    # all_nodes['comment'].print_all()
    for node in all_nodes:
        all_nodes[node].print_all()

"""
image_data = re.sub('^data:image/.+;base64,', '', data['img']).decode('base64')
image = Image.open(cStringIO.StringIO(image_data))
"""

