from preprocessing import textract_processing as txt
from text_processing import tf_idf_cosine_similarity as tf_idf
import os
from pyresparser import ResumeParser

def process_files(req_document,resume_docs):
    req_doc_text = txt.get_content_as_string(req_document)
    # print('The start' * 5)
    # data = ResumeParser(req_document)
    resume_doc_text = []
    names = []
    for doct in resume_docs:
        resume_doc_text.append(txt.get_content_as_string(doct))
        data = ResumeParser(doct).get_extracted_data()
        if data['name'] is not None:
            names.append(data['name'])
        else:
            names.append(resume_docs)
    cos_sim_list = tf_idf.get_tf_idf_cosine_similarity(req_doc_text,resume_doc_text)
    final_doc_rating_list = []
    zipped_docs = zip(cos_sim_list,resume_docs,names)
    sorted_doc_list = sorted(zipped_docs, key = lambda x: x[0], reverse=True)
    for element in sorted_doc_list:
        doc_rating_list = []
        doc_rating_list.append(os.path.basename(element[1]))
        doc_rating_list.append("{:.0%}".format(element[0]))
        doc_rating_list.append(element[2])

        if element[0] >= 0.442:
            doc_rating_list.append("Possible Match")
        final_doc_rating_list.append(doc_rating_list)
    return final_doc_rating_list
 