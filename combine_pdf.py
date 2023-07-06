import aspose.words as aw
import os
import PyPDF2

pdfiles = []
file_name = 'all_resources.pdf'
for filename in os.listdir('./resources'):
        if filename.endswith('.pdf'):
                if filename != file_name:
                        pdfiles.append(os.path.join('./resources', filename))
                        
pdfiles.sort(key = str.lower)

pdfMerge = PyPDF2.PdfMerger()
for filename in pdfiles:
        pdfFile = open(filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFile)
        pdfMerge.append(pdfReader)
pdfFile.close()
pdfMerge.write(file_name)