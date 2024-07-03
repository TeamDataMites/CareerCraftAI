import numpy as np
import pandas as pd
import json


df = pd.read_csv('job_data.csv')



def recommender(indexesfound):
    found_records = {}  
    for index in indexesfound:
        record = df.iloc[index]
        job_data = {
            "Job Title": record['Job Title'],
            "Company": record['Company'],
            "Job Link": record['Job Link'],
            "Extracted Text": record['Extracted Text'],
            "index": index
        }
        found_records[index] = job_data
    
    return found_records