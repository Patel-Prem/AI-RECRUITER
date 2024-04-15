import time
import boto3
import json

class TranscribeService:
    def __init__(self, bucketName):
        self.client = boto3.client('transcribe')
        self.bucketName = bucketName
        self.jsonFile = 'transcribe.json'
        self.txtFile = 'transcribe.txt'

    def transcribe_file(self, job_name, file_uri):
        try:
            self.client.start_transcription_job(
                TranscriptionJobName = job_name,
                Media = {
                    'MediaFileUri': file_uri
                },
                MediaFormat = 'mp4',
                LanguageCode = 'en-US',
                OutputBucketName= self.bucketName,
                OutputKey= self.jsonFile
            )

            max_tries = 60
            while max_tries > 0:
                max_tries -= 1
                job = self.client.get_transcription_job(TranscriptionJobName = job_name)
                job_status = job['TranscriptionJob']['TranscriptionJobStatus']
                if job_status in ['COMPLETED', 'FAILED']:
                    print(f'- - - Job {job_name} is {job_status} - - -')
                    if job_status == 'COMPLETED':
                        transcription_url = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                        print(f'- - - Download the transcript from - - - {transcription_url}')

                        # Read the job object from the S3 bucket
                        s3_client = boto3.client('s3')
                        response = s3_client.get_object(Bucket=self.bucketName, Key=self.jsonFile)
                        json_content = response['Body'].read().decode('utf-8')

                        # Parse the JSON content
                        json_object = json.loads(json_content)

                        # Now, 'json_object' contains the parsed JSON data and print the text
                        response = json_object['results']['transcripts'][0]['transcript']

                        # Return the transcription response
                        return response
                    break
                else:
                    print(f"Waiting for {job_name}. Current status is {job_status}.")
                time.sleep(10)
        except Exception as e:
            # Error occurred, delete the transcription job
            print(f"Error occurred: {str(e)}")
        finally:
            # Delete the job regardless of completion status
            self.client.delete_transcription_job(TranscriptionJobName=job_name)
            print('- - - Job deleted - - -')
