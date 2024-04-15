import boto3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity
from chalicelib import utility
preprecess_service = utility.UtilityService()

class ComprehendService:
    def __init__(self):
       self.client = boto3.client('comprehend')
    
    def extract_entities_and_phrases(self, text):
        # Extract entities and key phrases from the text
        # response = self.client.detect_entities(Text=text, LanguageCode='en')
        # entities = [entity['Text'] for entity in response['Entities']]
        
        response = self.client.detect_key_phrases(Text=text, LanguageCode='en')
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        
        # return entities + key_phrases
        return key_phrases

    
    def calculate_similarity(self, text):
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        similarities = cosine_similarity(count_matrix)[0][1]

        # vectorizer = TfidfVectorizer()
        # X = vectorizer.fit_transform(text)
        # similarities = cosine_similarity(X[0], X[1])[0][0] 
        
        return round(similarities * 100, 2)
        
    def classify_documents(self, response, jd):

        # pre-processing
        jd = preprecess_service.pre_process(jd)
        response = preprecess_service.pre_process(response)

        '''
        # Version-1
        
        # Classify the candidate's response
        respons_entities_key_phrasese = self.extract_entities_and_phrases(response)
        respons_entities_key_phrasese = ' '.join(set(respons_entities_key_phrasese))
        
        print("- - - respons_entities_key_phrasese - - -", respons_entities_key_phrasese)       
        print('------------------------------------------------------------')

        # Classify the job description
        jd_entities_key_phrasese = self.extract_entities_and_phrases(jd)
        jd_entities_key_phrasese = ' '.join(set(jd_entities_key_phrasese))

        print("- - - jd_entities_key - - -", jd_entities_key_phrasese)
        print('------------------------------------------------------------')


        # List of skills form jd
        jd_skills = preprecess_service.get_skills(jd)
        jd_skills = ' '.join(jd_skills)
        # List of skills form response
        response_skills = preprecess_service.get_skills(response)
        response_skills = ' '.join(response_skills)

        # List of skills form jd_entities_key_phrasese
        jd_key_skills = preprecess_service.get_skills(jd_entities_key_phrasese)
        jd_key_skills = ' '.join(jd_key_skills)

        # List of skills form respons_entities_key_phrasese
        response_key_skills = preprecess_service.get_skills(respons_entities_key_phrasese)
        response_key_skills = ' '.join(response_key_skills)


        # calculate similarities
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response, jd]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response, jd]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response, jd_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response, jd_skills] # 0.0 FINAL VERSION
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response, jd_key_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response, jd_key_skills]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response, jd_entities_key_phrasese]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response, jd_entities_key_phrasese]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_skills, jd]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_skills, jd]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_skills, jd_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_skills, jd_skills]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_skills, jd_key_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_skills, jd_key_skills]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_skills, jd_entities_key_phrasese]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_skills, jd_entities_key_phrasese]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_key_skills, jd]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_key_skills, jd]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_key_skills, jd_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_key_skills, jd_skills] # 0.0 FINAL VERSION
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_key_skills, jd_key_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_key_skills, jd_key_skills]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [response_key_skills, jd_entities_key_phrasese]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [response_key_skills, jd_entities_key_phrasese]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [respons_entities_key_phrasese, jd]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [respons_entities_key_phrasese, jd]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [respons_entities_key_phrasese, jd_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [respons_entities_key_phrasese, jd_skills] # 0.0 FINAL VERSION
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [respons_entities_key_phrasese, jd_key_skills]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [respons_entities_key_phrasese, jd_key_skills]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~text = [respons_entities_key_phrasese, jd_entities_key_phrasese]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        text = [respons_entities_key_phrasese, jd_entities_key_phrasese]
        similarities = self.calculate_similarity(text)
        print("- - - similarities - - -", similarities)

        '''

        # Version-2 

        # Classify the candidate's response
        respons_key_phrasese = self.extract_entities_and_phrases(response)
        respons_key_phrasese = ' '.join(respons_key_phrasese)
        print("- - - respons_key_phrasese - - -", respons_key_phrasese)       

        # List of skills form respons_key_phrasese
        response_key_skills = preprecess_service.get_skills(respons_key_phrasese)
        response_key_skills_all = ' '.join(response_key_skills['skills'])
        # print("- - - - - response_key_skills - - - - -", response_key_skills)

        # Classify the job description
        jd_key_phrasese = self.extract_entities_and_phrases(jd)
        jd_key_phrasese = ' '.join(jd_key_phrasese)
        print("- - - jd_key_phrasese - - -", jd_key_phrasese)

        # List of skills form jd_key_phrasese
        jd_key_skills = preprecess_service.get_skills(jd_key_phrasese)
        jd_key_skills_all = ' '.join(jd_key_skills['skills'])
        # print("- - - - - jd_key_skills - - - - -", jd_key_skills)
        

        response_hard_skills = ' '.join(response_key_skills['hard_skills'])
        response_soft_skills = ' '.join(response_key_skills['soft_skills'])
        jd_hard_skills = ' '.join(jd_key_skills['hard_skills'])
        jd_soft_skills = ' '.join(jd_key_skills['soft_skills'])

        text = [response_key_skills_all, jd_key_skills_all]
        combine_skills_similarities = self.calculate_similarity(text)
        
        text = [response_hard_skills, jd_hard_skills]
        hard_skills_similarities = self.calculate_similarity(text)
        
        text = [response_soft_skills, jd_soft_skills]
        soft_skills_similarities = self.calculate_similarity(text)

        similarities = {
            'combine_skills' : combine_skills_similarities,   
            'hard_skills' : hard_skills_similarities,  
            'soft_skills' : soft_skills_similarities  
        }

        return similarities