"""
HELLO, I am green_4.py

-------------------------------------------------------------------------------
MIT License Copyright (c) 2017 Larry S. Liebovitch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-------------------------------------------------------------------------------

This program generates the 5 input files needed for the programs data.py, teal.py, and tealclass.py that create the GUI to integrate ordinary differential equations (ODEs), display the results, and change the initial conditions or interactions between variables

Sample files, named below, are included in the folder:sample_files

Instructions:

1. Create a powerpoint as described in the powerpoint file: CLDinstructions.pptx

2. Save that powerpoint as a .pptx file. Let's say that filename is: CLDsample.pptx and the Causal Loop Diagram that you created is in Slide 1.

3. The file CLDsample.pptx is actually NOT a single file, but a compressed .zip file.  Change its extension from .pptx to .zip so that its filename is now CLDsample.zip

4. Unzip (uncompress) the file CLDsample.zip. Depending on the operating system this may require: double clicking on the file, a command from the terminal to: unzip CLDsample.zip, or the use of an App.

5. This will create a folder: CLDsample
   Inside that folder is a folder: ppt
   Inside that folder is a folder: slides
   Inside that folder is a file: slide1.xml

6. Move file slide1.xml into the same folder as green_4.py

7. Run the green_4.py script.
   At the prompt "Enter XML filename: ", type: slide1.xml <return>
   At the prompt"Enter Z #: ", type: a unique number <return>
    for example, type: 401<return>

8. The script green_4.py will create the following 5 input files needed for the GUI of the mathematical model (here with the unique number: 401)
   m401.txt
   b401.txt
   c401.txt
   ic401.txt
   btextbxy401.txt

NOTE: the values in the adjacency matrix cij in file c401.txt (the strength of the connection from variable j to variable i) will depend on the thickness of the lines connecting them in the powerpoint slide.  For some applications, ALL those values may need to be multiplied by a constant factor.

9. Move those 5 input files into the same folder as data.py, teal.py, and tealclass.py.

-------------------------------------------------------------------------------"""

import xml.etree.ElementTree as etree
import numpy as np

# hardcoding the namespace
p = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def get_input():
    input_slide = input("Enter XML filename: ")
    if input_slide.find('.xml') != -1:
        input_slide = input_slide[:input_slide.find('.xml')]
    return input_slide


def get_output_file(i):
    global input_slide
    if i == 1:
        input_slide = input("Enter nodes output filename: ")
    if i == 0:
        input_slide = input("Enter matrix output filename: ")
    if (input_slide.find('.txt') != -1):
        input_slide = input_slide[:input_slide.find('.txt')]
    return input_slide


def get_input_num():
    return input("Enter Z #: ")


def write_to_file(filename, iterations, num):
    file = open(filename + ".txt", "w")
    for i in range(int(iterations)):
        file.write(str(num) + '\n')
    file.close()


# SCALE FACTOR = 12700
SCALE_FACTOR = 12700
MAX_WEIGHT = 0
# DIFFERENT HARDSET VALUES FOR COLORS IN SCHEME
accent1 = "4F81BD"
accent2 = "C0504D"
accent3 = "9BBB59"
accent4 = "8064A2"
accent5 = "4BACC6"
accent6 = "F79646"
nodes_filename = "btextbxy"
matrix_filename = "c"
ic = "ic"
b = "b"
m = "m"

input_slide = get_input()
tree = etree.parse(input_slide + ".xml")
root = tree.getroot()

spTree = tree.find('.//' + p + 'spTree')

shape_list = spTree.findall(p + 'sp')
cxn_list = spTree.findall(p + 'cxnSp')
# debug purpose
o = 0
negative = 0
positive = 0
# counting nodes/rect
nodeNum = 0
z = 0
# MATRIX && RECT/NODE MAP
matrix = [[]]
mapping = {}
print('Running...')
z = get_input_num()


nodes_file = open(nodes_filename + z + ".txt", "w")

# SHAPES LIST
for child in shape_list:
    o = o + 1
    # non-visual properties
    shape = child.find('.//' + p + 'cNvPr')
    # shape properties
    spPr = child.find('' + p + "spPr")

    # PRINTS OUT RECTANGLES WITH ID AND NAME, OFFSET , WIDTH , HEIGHT
    if child[1][1].attrib.get('prst') == "rect" or etree.iselement(spPr.find(a + "custGeom")):

        rectSolidFill = spPr.find(a + "solidFill")
        rectColor = rectSolidFill.find(a + "schemeClr")
        if rectColor == None:
            rectColor = rectSolidFill.find(a + "srgbClr").get('val')
        else:
            rectColor = rectSolidFill.find(a + "schemeClr").get('val')
        # print (rectColor)
        xfrm = spPr.find(a + "xfrm")

        x_offset = xfrm.find(a + 'off').attrib.get('x')
        y_offset = xfrm.find(a + 'off').attrib.get('y')
        width = xfrm.find(a + 'ext').attrib.get('cx')
        height = xfrm.find(a + 'ext').attrib.get('cy')

        full_text = ""
        textBody = child.find('' + p + 'txBody')
        t = textBody.findall('.//' + a + 't')
        for elem in t:
            full_text += "".join(elem.text)

        identifier = str(nodeNum + 1)
        color = "yellow"
        if rectColor == "accent2" or rectColor == "C0504D":
            color = "gray"
        #print(identifier+"\t"+
        #    full_text.rstrip() +  "\t" +"x_offset: "+ x_offset + "\t" + "y_offset: "+ y_offset + "\t" +"width: "+ width + "\t" + "height: "+height)
        nodes_file.write(
            full_text.rstrip() + "\t" + color + "\t" + x_offset + "\t" + y_offset + "\t" + height+ "\t" + width)
        #nodes_file.write(identifier + "\t" + color + "\t" +
        #                 x_offset + "\t" + y_offset + "\t" + height + "\t" + width)
        nodes_file.write('\n')

        # add to map and increment node counter
        mapping[int(shape.get('id'))] = nodeNum
        # print ("Node "+str(r+1)+ ":"+full_text)
        nodeNum = nodeNum + 1

# close nodes_file
nodes_file.close()
write_to_file(ic + z, nodeNum, 0.1)
write_to_file(b + z, nodeNum, 0)
write_to_file(m + z, nodeNum, -0.9)
# initialize the matrix
matrix = np.matrix([[0] * nodeNum] * nodeNum)

# CONNECTORS LIST consisting of connector shapes <cxnSp>
for child in cxn_list:
    o = o + 1
    CxnSpPr = child.find('.//' + p + 'nvCxnSpPr')
    cNvPr = CxnSpPr.find('.//' + p + 'cNvPr')
    spPr = child.find('' + p + "spPr")
    xfrm = spPr.find(a + "xfrm")
    aln = spPr.find(a + "ln")

    # DEFAULT as Positive
    RGB = "+"
    asolidFill = aln.find(a + "solidFill")
    if asolidFill != None:
        aRGB = asolidFill.find(a + "srgbClr")
        if (aRGB != None):
            RGB = aRGB.get('val')
            if RGB == "FF0000":
                RGB = "-"
                negative = negative + 1
        else:
            positive = positive + 1
    else:
        RGB = "+"
        positive = positive + 1

    # DEAFULT IS SCALE_FACTOR if not grab value
    # 3 defaulted values, 9525(0.75) , 25400(2), 38100(3)
    line_width = aln.get('w')
    if line_width == None:
        pStyle = child.find(p + "style")
        lnRef = pStyle.find(a + "lnRef").get('idx')
        # print (lnRef)
        if lnRef == '1':
            line_width = float('12700') * 0.75
        elif (lnRef == '2'):
            line_width = float('12700') * 2
        elif (lnRef == '3'):
            line_width = float('12700') * 3

    if float(line_width) > MAX_WEIGHT:
        MAX_WEIGHT = float(line_width)
    # print(line_width)
    cNvCxnSpPr = CxnSpPr.find(p + 'cNvCxnSpPr')
    start_Cxn = cNvCxnSpPr.find(a + 'stCxn')
    if etree.iselement(start_Cxn):
        start_Cxn = start_Cxn.attrib.get('id')
    else:
        start_Cxn = '0'

    end_Cxn = cNvCxnSpPr.find(a + 'endCxn')
    if etree.iselement(end_Cxn):
        end_Cxn = end_Cxn.attrib.get('id')
    else:
        end_Cxn = '0'

    x_offset = xfrm.find(a + 'off').attrib.get('x')
    y_offset = xfrm.find(a + 'off').attrib.get('y')
    width = xfrm.find(a + 'ext').attrib.get('cx')
    height = xfrm.find(a + 'ext').attrib.get('cy')
    # change to mapping and input to matrix

    if start_Cxn == '0' or end_Cxn == '0':
        continue
    start = mapping.get(int(start_Cxn))
    end = mapping.get(int(end_Cxn))

    if RGB == '-':
        line_width = float(line_width) * -1.0

    matrix[end].put(start, (float(line_width) * 1.0))

matrix = np.multiply(1.0 / SCALE_FACTOR, matrix)
matrix = np.matrix(np.round(matrix, 3))

output = open(matrix_filename + z + ".txt", "w")
lists = matrix.tolist()
for i in range(nodeNum):
    output.write((str(lists[i])[1:-1]).replace(', ', '\t'))
    output.write('\n')
output.close()

print('Finished.')



def debug():
    print()
    print("Objects: " + str(o))
    print("Nodes: " + str(nodeNum))
    print("Negative Connects: " + str(negative))
    print("Positive Connects: " + str(positive))
    print("Node Mapping to ID: " + str(sorted(((v, k)
                                               for k, v in mapping.items()), reverse=False)))
    print("--------------------------")
    print("Directed In-Graph")
    print(matrix)
    print("MAX_WEIGHT:" + str(MAX_WEIGHT))
    print("-------------------------")
    print("Directed Out-Graph(Transpose)")

    print(matrix.getT())
    print()

#debug()
