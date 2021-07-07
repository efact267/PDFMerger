# PDFMerger
Merges all PDF files in the directory and adds bookmarks based on the filenames.

To parse the bookmarks from the filenames they must be of the following type:
100_Section_Subsection_SubSubsection 
The leading numbers get ignored by the program. They are used to sort the files and determine the order of the files in the merged pdf.
After that the labels of the sections (up to 3 levels) are seperated by underscores. 