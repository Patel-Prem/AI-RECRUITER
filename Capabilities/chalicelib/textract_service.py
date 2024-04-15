import boto3
import time

class TextractService:
    def __init__(self, storage_location):
        self.client = boto3.client('textract')
        self.bucket_name = storage_location

    def start_text_detection(self, object_name):
        response = self.client.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': self.bucket_name, 'Name': object_name}}
        )
        job_id = response["JobId"]
        print(f"Started job with id: {job_id}")
        return job_id

    def wait_for_job_completion(self, job_id):
        while True:
            response = self.client.get_document_text_detection(JobId=job_id)
            status = response["JobStatus"]
            print(f"Job status: {status}")
            if status in ["SUCCEEDED", "FAILED"]:
                return status
            time.sleep(5)

    def retrieve_results(self, jobId):
        pages = []
        response = self.client.get_document_text_detection(JobId=jobId)
        pages.append(response)
        print(f"Resultset page received: {len(pages)}")
        
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
            while nextToken:
                response = self.client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
                pages.append(response)
                print(f"Resultset page received: {len(pages)}")
                
                if 'NextToken' in response:
                    nextToken = response['NextToken']
                else:
                    break
        
        return pages

    def extract_text_from_pdf(self, object_name):
        job_id = self.start_text_detection(object_name)
        if self.wait_for_job_completion(job_id) == "SUCCEEDED":
            pages = self.retrieve_results(job_id)
            text = ""
            for page in pages:
                for item in page["Blocks"]:
                    if item["BlockType"] == "LINE":
                        text += item["Text"] + "\n"
            return text
