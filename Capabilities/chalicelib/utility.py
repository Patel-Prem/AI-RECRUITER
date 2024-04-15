import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import contractions

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
                
import os
import json

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

class UtilityService:
    nlp = spacy.load('en_core_web_lg')
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    def pre_process(self, text):
        text = text.lower()

        text = text.replace("\n", " ")
        
        # Expand contractions
        text = contractions.fix(text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize text
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        
        # Lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        # Join tokens back into a string
        preprocessed_text = ' '.join(tokens)
        
        return preprocessed_text
    
    def get_skills(self, text):
        skills = []
        annotations = UtilityService.skill_extractor.annotate(text)

        # Path to the JSON file
        json_file_path = './skill_db_relax_20.json'
        skills_data = None
        # Check if the file exists
        if os.path.exists(json_file_path):
            # Open the JSON file in read mode
            with open(json_file_path, 'r') as file:
                # Load JSON data into a dictionary
                skills_data = json.load(file)
            # Print the loaded JSON data
            print("JSON data loaded successfully:")
        else:
            print("The JSON file does not exist.")


        hard_skills = []
        soft_skills = []
        if 'full_matches' in annotations['results']:
            for item in annotations['results']['full_matches']:
                print("Hard Skills : ", item['doc_node_value'])
                if skills_data.get(item["skill_id"]) is not None:
                    if skills_data.get(item["skill_id"]).get("skill_type") == "Hard Skill":
                        hard_skills.append(item['doc_node_value'])
                    elif skills_data.get(item["skill_id"]).get("skill_type") == "Soft Skill":
                        soft_skills.append(item['doc_node_value'])
                doc_node_value = item['doc_node_value']
                skills.append(doc_node_value)

        if 'ngram_scored' in annotations['results']:
            for item in annotations['results']['ngram_scored']:
                print("Soft Skills : ", item['doc_node_value'])
                if skills_data.get(item["skill_id"]) is not None:
                    if skills_data.get(item["skill_id"]).get("skill_type") == "Hard Skill":
                        hard_skills.append(item['doc_node_value'])
                    elif skills_data.get(item["skill_id"]).get("skill_type") == "Soft Skill":
                        soft_skills.append(item['doc_node_value'])
                doc_node_value = item['doc_node_value']
                skills.append(doc_node_value)

        return {"skills" : skills, "hard_skills": hard_skills, "soft_skills": soft_skills}