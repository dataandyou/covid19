import PyPDF2
# pdf file object
# you can find find the pdf file with complete code in below
pdfFileObj = open('WB_DHFW_Bulletin_9th_JULY_REPORT_FINAL.pdf', 'rb')
# pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# number of pages in pdf
print(pdfReader.numPages)
# a page object
pageObj = pdfReader.getPage(1)
# extracting text from page.
# this will print the text you can also save that into String
print(pageObj.extractText())

#pageObj = pdfReader.getPage(2)
#print(pageObj.extractText())

