

from chalice import Chalice
from chalicelib import storage_service
from chalicelib import transcribe_service
from chalicelib import comprehend_service
from chalicelib import textract_service


import base64
import json

#####
# chalice app configuration
#####
app = Chalice(app_name='Capabilities')
app.debug = True

#####
# services initialization
#####
storage_location = 'YOUR_BUCKET_NAME'
storage_service = storage_service.StorageService(storage_location)
transcribe_service = transcribe_service.TranscribeService(storage_location)
textract_service = textract_service.TextractService(storage_location)
comprehend_service = comprehend_service.ComprehendService()



#####
# RESTful endpoints
#####
@app.route('/uploadfiles', methods = ['POST'], cors = True)
def upload_video():
    """processes file upload and saves file to storage service"""
    request_data = json.loads(app.current_request.raw_body)

    # print("request_datarequest_data", request_data)
    # file_name = request_data['filenames']

    file_info = []
    # JD, Resume, Video
    for i in range(len(request_data['files'])):
        file_bytes = base64.b64decode(request_data['files'][i]['fileBytes'])
        # print("file_bytesfile_bytes", file_bytes)
        
        # print("request_data['files'][i]['fileType']", request_data['files'][i]['fileType'])
        # request_data['files'][i]['fileType'] application/pdf
        # request_data['files'][i]['fileType'] application/pdf
        # request_data['files'][i]['fileType'] video/mp4
        file_info.append(storage_service.upload_file(file_bytes, request_data['files'][i]['fileName']))

    # print('file_info file_info', file_info)
    # [{'fileId': 'Job Discription.pdf', 'fileUrl': 'http://contentcen301298810.aws.ai.s3.amazonaws.com/Job Discription.pdf'}, {'fileId': 'OHM PATEL Resume.pdf', 'fileUrl': 'http://contentcen301298810.aws.ai.s3.amazonaws.com/OHM PATEL Resume.pdf'}, {'fileId': 'Scenario 1_ Related to Job Description.mp4', 'fileUrl': 'http://contentcen301298810.aws.ai.s3.amazonaws.com/Scenario 1_ Related to Job Description.mp4'}]

    return file_info
  

@app.route('/readfiles', methods = ['POST'], cors = True)
def detect_file_text():
    request_data = json.loads(app.current_request.raw_body)

    # print("request_data['jdResumeURI']['jdURI']", request_data['jdResumeURI']['jdURI'])
    # request_data['jdResumeURI']['jdURI'] http://contentcen301298810.aws.ai.s3.amazonaws.com/Job Discription.pdf
    # 
    # print("request_data['jdResumeURI']['resumeURI']", request_data['jdResumeURI']['resumeURI'])
    # request_data['jdResumeURI']['resumeURI'] http://contentcen301298810.aws.ai.s3.amazonaws.com/OHM PATEL Resume.pdf

    jd_text = textract_service.extract_text_from_pdf(request_data['jdResumeURI']['jdURI'].split('/')[-1])
    resume_text = textract_service.extract_text_from_pdf(request_data['jdResumeURI']['resumeURI'].split('/')[-1])
    video_text = transcribe_service.transcribe_file("Trascribe-job", request_data['jdResumeURI']['videoURI'])

    print("jd_text : ", jd_text)
    print("resume_text : ", resume_text)
    print("video_text : ", video_text)

    video_similarity = comprehend_service.classify_documents(response=video_text, jd=jd_text)  
    resume_similarity = comprehend_service.classify_documents(response=resume_text, jd=jd_text)  

    similarities = {"video_similarity" : video_similarity,  "resume_similarity": resume_similarity}

    print("similarities: ", similarities)


    return similarities

