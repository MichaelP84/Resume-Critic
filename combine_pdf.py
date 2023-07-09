import aspose.words as aw
import os
import PyPDF2

pdfiles = []
folder_path = './separate_resumes/tutorials'
file_name = 'tutorials.pdf'
for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
                if filename != file_name:
                        pdfiles.append(os.path.join(folder_path, filename))
                        
pdfiles.sort(key = str.lower)

pdfMerge = PyPDF2.PdfMerger()
for filename in pdfiles:
        pdfFile = open(filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFile)
        pdfMerge.append(pdfReader)
pdfFile.close()
pdfMerge.write(file_name)