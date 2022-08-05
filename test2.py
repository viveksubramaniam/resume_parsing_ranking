import textract

path = "C:\\Users\\vivek\\Desktop\\resume_ranking\\samples\\resumes_sample\\"
file = "Cloud Architect Dummy.doc"

import os, docx2txt
def get_doc_text(filepath, file):
    if file.endswith('.docx'):
       text = docx2txt.process(file)
       return text
    elif file.endswith('.doc'):
       # converting .doc to .docx
       doc_file = filepath + file
       docx_file = filepath + file + 'x'
       if not os.path.exists(docx_file):
          os.system('antiword ' + doc_file + ' > ' + docx_file)
          with open(docx_file) as f:
             text = f.read()
          os.remove(docx_file) #docx_file was just to read, so deleting
       else:
          # already a file with same name as doc exists having docx extension, 
          # which means it is a different file, so we cant read it
          print('Info : file with same name of doc exists having docx extension, so we cant read it')
          text = ''
       return text

# text = get_doc_text(path, file)
text = textract.process(path + file)
print(text)