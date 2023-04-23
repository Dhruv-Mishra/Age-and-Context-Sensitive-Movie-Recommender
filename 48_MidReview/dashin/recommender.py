
import pandas as pd
import numpy as np
import tensorflow_hub as hub
import math
from sklearn.metrics.pairwise import linear_kernel
import difflib
import pickle

# def cosine_sim(a,b):
#     a = a.numpy()
#     b = b.numpy()
#     return a.dot(b)/((math.sqrt(sum(pow(element, 2) for element in a))) * ((math.sqrt(sum(pow(element, 2) for element in b)))))

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

class Recommender():
    dataset = -1
    cosine_sim = -1
    indices = -1
    movies = -1
    #embed = -1

    def __init__(self):
        self.read_data()
        self.initialize_recommender()
        #self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    
    def read_data(self):
        #df = pd.read_csv('unclean_dataset.csv')
        df = pd.read_csv('D:\\Desktop\\Proj_Git\\Information-Retrival-Project\\48_MidReview\\Datasets\\unclean_dataset.csv')
        df = df.dropna()
        df = df.drop_duplicates(subset='Movie Title', keep='first')
        df = df.reset_index(drop=True)
        self.dataset = df

    def initialize_recommender(self):
        self.movies = self.dataset['Movie Title'].unique()
        #print("Embed",self.embed)
        encodings = embed(self.dataset['Plot'])
        matrix = np.vstack(encodings)
        cosine_sim = linear_kernel(matrix, matrix)
        indices = pd.Series(self.dataset.index, index=self.dataset['Movie Title'])
        self.cosine_sim = cosine_sim
        self.indices = indices

    def get_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        return sim_scores

    def combine_recommendations(self,titles):
        out = []
        for i in range(len(self.dataset)):
            out.append([i,0])
        for org_title in titles:            #### Titles may or may not be present in the dataset, finds the closest title matching in the dataset
            title = difflib.get_close_matches(org_title, self.movies, cutoff= 0.0000001, n = 1)[0]  #Searching the closest match in the dataset 
            cur_out = self.get_recommendations(title)
            for score in range(len(cur_out)):
                out[score][1] += cur_out[score][1]
        final_score = sorted(out, key=lambda x: x[1], reverse=True)
        movie_indices = [i[0] for i in final_score][1:10]
        result = self.dataset.iloc[movie_indices]
        return result

def start(args):
    try:
        #r = pickle.load(open("/Users/cloud9xpress/Desktop/codeCloud/dashin_front-end/48_MidReview/recom_savefile.pickle", "rb"))
        r = pickle.load(open("D:\\Desktop\\Proj_Git\\Information-Retrival-Project\\48_MidReview\\recom_savefile.pickle", "rb"))
    except:
        r = Recommender()
        #pickle.dump(r,open("/Users/cloud9xpress/Desktop/codeCloud/dashin_front-end/48_MidReview/recom_savefile.pickle", "wb"))
        pickle.dump(r,open("D:\\Desktop\\Proj_Git\\Information-Retrival-Project\\48_MidReview\\recom_savefile.pickle", "wb"))
    # r = Recommender() #initializing it takes time 10+ s, but runs only once 
    res = r.combine_recommendations(args) # runs in under 0.2 s 
    return res
