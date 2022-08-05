from cv2 import threshold
from constants import file_constants as cnst
from processing import resume_matcher
from preprocessing import textract_processing as txt, tf_idf_lemmetizer as tf_idf_lemma
from sklearn.feature_extraction.text import TfidfVectorizer
from text_processing import tf_idf_cosine_similarity as tf_idf
import os 
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

job_types = ['java', 'sre', 'data_science_analyst', 'devops']

jdResults = {}



# resume_files = {}
# for filedir in job_types:
#     profile = os.path.join(cnst.resume_test, filedir)
#     resume_files[filedir] = []
#     for resume in os.listdir(profile):
#         resumeFile = os.path.join(profile, resume)
#         resume_files[filedir].append(resumeFile)
       
# for jobDesc, profile in zip(os.scandir(cnst.jd_test), job_types):
#     jdResults[jobDesc] = []
#     results = resume_matcher.process_files(jobDesc, resume_files[profile])
#     jdResults[jobDesc].append(results[1])

resume_file_path = "C:\\Users\\vivek\\Desktop\\resume_ranking\\samples\\resumes_sample"
jd_file_path = "C:\\Users\\vivek\\Desktop\\resume_ranking\\samples\\job_descriptions"



# thresholdValues = {}
# thresholdValues['job_types'] = job_types
# thresholdValues['matching_jd'] = []
# thresholdValues['unmatching_jd'] = []


for resume_type in job_types:

    matching_jd = []
    unmatching_jd = []

    resume_directory = os.path.join(resume_file_path, resume_type)
    resume = ""
    for file in os.listdir(resume_directory):
        # resumes.append(resume_file_path + "\\" + file)
        resume = resume_directory + "\\" + file
        for jd in os.listdir(jd_file_path):
            # results[jd] = []
            # jd_text = txt.get_content_as_string(jd)
            jd_path = jd_file_path + "\\" + jd
            result = resume_matcher.process_files(jd_path, [resume])
            
            if resume_type == os.path.splitext(jd)[0]:
                matching_jd.append(float(result[0][1].replace("%", ""))/100)
                
            else:
                unmatching_jd.append(float(result[0][1].replace("%", ""))/100)
    print("debug")
    match = np.asarray(matching_jd)
    noMatch = np.asarray(unmatching_jd)
    print("The mean for {} on a matching jd is: {}".format(resume_type, np.mean(match)))
    print("The mean for {} on a unmatching jd is: {}".format(resume_type, np.mean(noMatch)))



