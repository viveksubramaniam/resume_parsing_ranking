from preprocessing import textract_processing as txt
from text_processing import tf_idf_cosine_similarity as tf_idf
import os
from pyresparser import ResumeParser
from docx import Document
from pathlib import Path
import re
import numpy as np

cache_file = "C:\\Users\\vivek\\Desktop\\resume_ranking\\cached_files\\" 

def save_file(text, file, skill):
    document = Document()
    text = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', text)
    document.add_paragraph(text)
    
    document.save(cache_file + file + "_" + skill + ".docx")


def process_files(req_document,resume_docs):
    
    # print('The start' * 5)
    # data = ResumeParser(req_document)
    resume_doc_text = []
    flag = 0
    names = []
    fileName = Path(req_document).stem

    job_desc = txt.get_content_as_string(req_document)

    primSkillStart = job_desc.find("primary skills")
    primSkillEnd = job_desc.find("secondary skills")
    primary_skills = job_desc[primSkillStart + len("primary skills") + 1: primSkillEnd]
    save_file(primary_skills, fileName, "primary")

    secondSkillStart = job_desc.find("secondary skills")
    # secondary_skills = job_desc[secondSkillStart + len("secondary skills") + 1:]
    # secondary_skills = job_desc[0 : primSkillStart] + job_desc[secondSkillStart + len("secondary skills") + 1:]
    secondary_skills = job_desc
    save_file(secondary_skills, fileName, "secondary")

    for doct in resume_docs:
        data = ResumeParser(doct).get_extracted_data()
        if data['skills'] is not None:
            resume_doc_text.append(" ".join(data['skills']))
        else:
            resume_doc_text.append(txt.get_content_as_string(doct))
        
        if data['name'] is not None:
            names.append(data['name'])
        else:
            names.append(resume_docs)

    if primSkillStart != -1 and secondSkillStart != -1:
        primaryFile = cache_file + fileName + "_primary.docx"
        secondaryFile = cache_file + fileName + "_secondary.docx"

        prim_data = ResumeParser(primaryFile).get_extracted_data()
        sec_data = ResumeParser(secondaryFile).get_extracted_data()
        if prim_data['skills'] is not None:
            primary_skills = " ".join(prim_data['skills'])

        if sec_data['skills'] is not None:
            secondary_skills = " ".join(prim_data['skills'])

        prim = tf_idf.get_tf_idf_cosine_similarity(primary_skills,resume_doc_text)
        cos_sim_prim = [1.5*ele for ele in prim]

        sec = tf_idf.get_tf_idf_cosine_similarity(secondary_skills,resume_doc_text)
        cos_sim_sec = [ele for ele in sec]
        if len(resume_docs) > 1:
            norm = np.array([cos_sim_prim[i] + sec[i] for i in range(len(prim))])
            cos_sim_arr = (norm - np.min(norm))/ (np.max(norm) - np.min(norm))
            cos_sim_list = cos_sim_arr.tolist()
            if 0 in cos_sim_list:
                flag = 1
        else:
            cos_sim_list = [cos_sim_prim[i] + cos_sim_sec[i] for i in range(len(prim))]
            for i, num in enumerate(cos_sim_list):
                if num >= 0.95 and num < 150:
                    cos_sim_list[i] /= 1.3
                elif num >= 150:
                    cos_sim_list[i] /= 1.8
                
                if num == 0:
                    flag = 1
    
    if primSkillStart == -1 or secondSkillStart == -1 or flag == 1:
        req_doc = ResumeParser(req_document).get_extracted_data()
        if req_doc['skills'] is not None:
            jd_text = " ".join(req_doc['skills'])
        else:
            jd_text = txt.get_content_as_string(req_document)

        cos_sim_list = tf_idf.get_tf_idf_cosine_similarity(jd_text,resume_doc_text)

    final_doc_rating_list = []
    zipped_docs = zip(cos_sim_list,resume_docs,names)
    sorted_doc_list = sorted(zipped_docs, key = lambda x: x[0], reverse=True)
    for element in sorted_doc_list:
        doc_rating_list = []
        doc_rating_list.append(os.path.basename(element[1]))
        doc_rating_list.append("{:.0%}".format(element[0]))
        doc_rating_list.append(element[2])

        if element[0] >= 0.550:
            doc_rating_list.append("Possible Match")
        final_doc_rating_list.append(doc_rating_list)


        
    return (final_doc_rating_list, primaryFile, secondaryFile)
 