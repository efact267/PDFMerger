from glob import glob
import re
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import os

def pdf_merge(filename_merged_pdf):
    ''' Merge all the pdf files in the current directory '''
    merger = PdfFileMerger()
    pdf_files = [i for i in glob("*.pdf")]
    [merger.append(pdf) for pdf in pdf_files]
    temp_pdf = "TEMP" + filename_merged_pdf
    with open(temp_pdf, "wb") as new_file:    # save merged pdf as temporary file for further processing
        merger.write(new_file)


def parse_filenames_for_bookmarks():
    ''' Parse the filenames for chapters in order to use them for the bookmarks '''
    file_pages = []
    filename_contents=[]
    for pdf_files in glob("*.pdf"):   
        # save the number of pages from each file
        reader = PdfFileReader(open(pdf_files, 'rb'))
        file_pages.append(reader.getNumPages())              # number of pages from file that gets bookmarked
        # parse filenames for bookmarks 
        pdf_files = pdf_files[:-4]                          # remove file extensions 
        filename_contents.append(re.split('_', pdf_files))  # split filenames at underscores and save list of contents for each filename in lists
    # return the bookmarks and the page number of each file
    return filename_contents, file_pages 


def pdf_add_bookmarks(filename_merged_pdf, filename_contents, file_pages): 
    ''' Adds bookmarks to merged pdf based on the filenames '''
    # filenames must be of the following type:
    # 001_ParentBookmark_Child1Bookmark_Child2Bookmark.pdf
    # The leading numbers determin the order of the files in the folder and thus the order in the merged pdf, other from that they are not used
    # After the numbers the Chapters must be encoded in the filename
    # Following the Chapters, SubChapters and SubSubChapters can be defined
    # The filename contents must be seperated by underscores

    page_counter = 0
    writer = PdfFileWriter()                                # open output
    temp_pdf = "TEMP" + filename_merged_pdf
    temp_input_file = open(temp_pdf, "rb")
    reader = PdfFileReader(temp_input_file, "rb")            # open input
    
    # add all pages from temporary merged pdf to final pdf file that gets bookmarked
    num_pages = reader.getNumPages()                         # get total number of pages from the temporary merged pdf
    pages = list(range(0, num_pages))
    for page in pages:
        writer.addPage(reader.getPage(page)) # insert all pages

    # Begin of the bookmark loop for each file in the folder
    for files in range(len(filename_contents)):
        print("######################\n","----- File No. ", files, " -----", "######################\n")

#---------------------------------------------------------------------------------------------------------------------------

        # def parse_chapter(index, filename_contents, files, page_counter, level_1, level_2):
        #     if (0 <= index < len(filename_contents[files])):  
        #         if files==0:
        #             level_2 = writer.addBookmark(filename_contents[files][1], page_counter, parent=level_1)    # add bookmark for Chapter
        #             print("Chapter ", filename_contents[files][1], " added.")
        #         elif filename_contents[files][1] != filename_contents[files-1][1]:
        #             level_2 = writer.addBookmark(filename_contents[files][1], page_counter, parent=level_1)    # add bookmark for Chapter
        #             print("Chapter ", filename_contents[files][1], " added.")
        #         else:
        #             print("No (new) chapter found in ", filename_contents[files])
        #     return level_2

        # index = 1
        # level_1 = None
        # level_2 = "chapter"
        # level_1 = parse_chapter(index, filename_contents, files, page_counter, level_1, level_2)

        # index = 2
        # level_2 = "sub_chapter"
        # level_1 = parse_chapter(index, filename_contents, files, page_counter, level_1, level_2)

        # index = 3
        # level_2 = "sub_sub_chapter"
        # level_1 = parse_chapter(index, filename_contents, files, page_counter, level_1, level_2)

#---------------------------------------------------------------------------------------------------------------------------

        index = 1
        if (0 <= index < len(filename_contents[files])):  
            if files==0:
                chapter = writer.addBookmark(filename_contents[files][1], page_counter, parent=None)    # add bookmark for Chapter
                print("Chapter ", filename_contents[files][1], " added.")
            elif filename_contents[files][1] != filename_contents[files-1][1]:
                chapter = writer.addBookmark(filename_contents[files][1], page_counter, parent=None)    # add bookmark for Chapter
                print("Chapter ", filename_contents[files][1], " added.")
            else:
                print("No (new) chapter found in ", filename_contents[files])
        
        index = 2
        if (0 <= index < len(filename_contents[files])):
            if files==0:
                sub_chapter = writer.addBookmark(filename_contents[files][index], page_counter, parent=chapter)    # add bookmark for SubChapter
                print("SubChapter ", filename_contents[files][index], " added.")
            elif (0 <= index < len(filename_contents[files-1])):
                if filename_contents[files][index] != filename_contents[files-1][index]:
                    sub_chapter = writer.addBookmark(filename_contents[files][index], page_counter, parent=chapter)    # add bookmark for SubChapter
                    print("SubChapter ", filename_contents[files][index], " added.")
            else:
                sub_chapter = writer.addBookmark(filename_contents[files][index], page_counter, parent=chapter)    # add bookmark for SubChapter
                print("SubChapter ", filename_contents[files][index], " added.")
        else:
            print("No SubChapter found in ", filename_contents[files])

        index = 3
        if (0 <= index < len(filename_contents[files])):
            if files==0:
                writer.addBookmark(filename_contents[files][index], page_counter, parent=sub_chapter)    # add bookmark for SubSubChapter
                print("SubSubChapter ", filename_contents[files][index], " added.")
            elif (0 <= index < len(filename_contents[files-1])):
                if filename_contents[files][index] != filename_contents[files-1][index]:
                    writer.addBookmark(filename_contents[files][index], page_counter, parent=sub_chapter)    # add bookmark for SubSubChapter
                    print("SubSubChapter ", filename_contents[files][index], " added.")
            else:
                writer.addBookmark(filename_contents[files][index], page_counter, parent=sub_chapter)    # add bookmark for SubSubChapter
                print("SubSubChapter ", filename_contents[files][index], " added.")
        else:
            print("No SubSubChapter found in ", filename_contents[files])
        
        page_counter = page_counter + file_pages[files]
  
    
    # open bookmarks tab and save merged and bookmarked pdf
    writer.setPageMode("/UseOutlines")                  # tells the PDF to open to bookmarks
    outputStream = open(filename_merged_pdf,'wb')       # creating final result pdf
    writer.write(outputStream)                          # writing to final result pdf
    outputStream.close()                                # closing result

    # close and delete temporary merged pdf without bookmarks
    temp_input_file.close()
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
    else:
        print("Could not delete temporary file")



if __name__ == "__main__":
    FILE_EXTENSION = ".pdf"
    filename_merged_pdf = "final_merged_pdf_with_bookmarks"
       
    filename_merged_pdf = filename_merged_pdf + FILE_EXTENSION
    filename_contents, file_pages = parse_filenames_for_bookmarks()
    pdf_merge(filename_merged_pdf)
    pdf_add_bookmarks(filename_merged_pdf, filename_contents, file_pages)

    print('\n', filename_merged_pdf, " successfully created.\n")



