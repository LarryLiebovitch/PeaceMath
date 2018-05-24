#
**green_4.py**

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
