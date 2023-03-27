from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np
import warnings
from sklearn.decomposition import PCA
warnings.filterwarnings("ignore")

warnings.filterwarnings("ignore")

class Recommender:
    myData = 0
    tfidf2 = 0
    df = 0
    tfidf_matrix2 = 0
    cosine_sim = 0
    indices = 0
    path = 0
    col_df = -1
    col_mat = -1
    ratings = -1
    user = []

    def __init__(self, path):
        #print("Initializing Recommender...")
        self.path = path
        self.myData = pd.read_csv(path)
        self.indices = pd.Series(self.myData.index, index=self.myData['title']).drop_duplicates()
        #print("Recommender Initialized")
        self.clean_dataset()
        self.df = self.myData.copy(deep=True)
        self.df['description'] = self.df['description'].fillna('')
        self.tfidf2 = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix2 = self.tfidf2.fit_transform(self.df['description'])
        
        dataframe = pd.DataFrame(self.tfidf_matrix2.A)
        pca = PCA(n_components=3400) 
        pca.fit(dataframe)
        ehh = pca.transform(dataframe)
        self.tfidf_matrix2 = ehh

        self.cosine_sim = linear_kernel(self.tfidf_matrix2, self.tfidf_matrix2)
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()
        #print("Now Ready To Recommend...")

    def recalculate_recommender(self, newData):
        self.df = newData
        self.df['description'] = self.df['description'].fillna('')
        self.tfidf2 = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix2 = self.tfidf2.fit_transform(self.df['description'])
        dataframe = pd.DataFrame(self.tfidf_matrix2.A)
        pca = PCA(n_components=3400) 
        pca.fit(dataframe)
        ehh = pca.transform(dataframe)
        self.tfidf_matrix2 = ehh
        self.cosine_sim = linear_kernel(self.tfidf_matrix2, self.tfidf_matrix2)
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def getUsers(self):
        n = int(input("Enter the Total Number of Users:"))
        in_users = []
        for i in range(n):
            age = int(input("Enter Your Age:"))
            movie = input("Enter Your Movie Preference:")
            in_users.append([movie, age])
        self.user = in_users

    def addUsers(self,users):
        self.user.extend(users)
        #print("Successfully Added",len(users),"New Users")

    def combine(self, a):
        row_0 = self.myData.iloc[[a[0]]]
        for i in range(len(row_0)):
            if (self.myData.iloc[[a[0], i]]).empty:
                for j in range(1, len(a)):
                    if not (self.myData.iloc[[a[j], i]]).empty:
                        self.myData.at[[a[0], i]] = self.myData.iloc[[a[j], i]]
                        break

    def clean_dataset(self, param='title'):
        #print()
        #print("Now Cleaning The Dataset...")
        delete_indices = []
        for i in range(len(self.myData)):
            idx = self.indices[self.myData.loc[i, param]]
            temp = []
            if (idx.size > 1):
                for j in range(0, len(idx)):
                    temp.append(idx[j])
                delete_indices.append(temp)
            else:
                delete_indices.append([i])
        for i in range(len(delete_indices)):
            self.combine(delete_indices[i])
        #print("Dataset Cleaned...")
        #print()
        self.myData = self.myData.drop_duplicates(subset=['title'], keep='first')

    def age_filtered_dataset(self,users = user):
        users_a = []
        users_m = []
        for i in range(len(users)):
            user = users[i]
            users_m.append(user[0])
            users_a.append(user[1])
        min_age = min(users_a)
        max_age = max(users_a)
        allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG", "TV-14","R","TV-MA","NR","PG","UR","NC-17"]
        if (min_age < 7):
            allowed_rating = ["TV-Y"]
        elif min_age <= 13 and max_age <= 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV"]
        elif min_age <= 13 and max_age > 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG"]
        elif min_age <= 14 and max_age <= 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-14"]
        elif min_age <= 17 and max_age > 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG", "TV-14"]
        allowed_rating.extend(["G","TV-G"])
        #print(self.df.shape)
        final = self.df[self.df['rating'].isin(allowed_rating)]
        final.reset_index()
        #print(final.shape)
        for i in users_m:
            row = self.df[self.df['title'] == i].values.tolist()[0]
            final.loc[len(final.index)] = row
        #print(final.shape)
        #final.at[i, 'country'] = x[0]
        final.reset_index(drop=True)
        #print(final)  
        return final

    def get_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        return sim_scores

    def useRecommender(self, titles):
        main_list = []
        for title in titles:
            main_list.append(self.get_recommendations(title))
        final_score = []
        for j in range(len(main_list[0])):
            current_score = 0
            for i in range(len(main_list)):
                current_score += main_list[i][j][1]
            final_score.append([j, current_score])
        final_score = sorted(final_score, key=lambda x: x[1], reverse=True)
        final_score = final_score[1:100]
        movie_indices = [i[0] for i in final_score]
        return self.df[['title','rating']].iloc[movie_indices]

    def recommend(self):
        content = self.recommend_content(self.user)
        # collaborative = self.recommend_collaborative(self.user)
        # demographic = self.recommend_demographic()
        return content

    def recommend_content(self, users=user):
        preferences = []
        for i in users:
            preferences.append(i[0])
        #newData = self.age_filtered_dataset(users)
        #print("Recalculating the Entries To Suit Your Preferences")
        # self.recalculate_recommender(self.df)
        #print("Now searching from a catalogue of over", len(self.myData), "Movies and TV Shows...")
        temp = (self.useRecommender(preferences))['title']
        temp2 = (self.useRecommender(preferences))['rating']
        out = list(temp)
        age = list(temp2)
        # print("Here's What We Think You'll Like:")
        num = 1
        users_a = []
        users_m = []
        for i in range(len(users)):
            user = users[i]
            users_m.append(user[0])
            users_a.append(user[1])
        min_age = min(users_a)
        max_age = max(users_a)
        allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG", "TV-14","R","TV-MA","NR","PG","UR","NC-17"]
        if (min_age < 7):
            allowed_rating = ["TV-Y"]
        elif min_age <= 13 and max_age < 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV"]
        elif min_age <= 13 and max_age >= 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG"]
        elif min_age <= 14 and max_age < 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-14"]
        elif min_age <= 14 and max_age >= 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-14","TV-PG","PG"]
        elif min_age > 14 and max_age < 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-14"]
        elif min_age < 18 and max_age >= 18:
            allowed_rating = ["TV-Y", "TV-Y7", "TV-Y7-FV", "PG-13", "TV-PG", "TV-14"]
        output = []
        for i in range(len(out)):
            if (out[i] not in preferences) and age[i] in allowed_rating:
                output.append(str(num)+" "+str(out[i]))
                num += 1
            if (num == 10):
                break
        return output
        
    def calc_collaborative(self):
        df = pd.read_csv('Datasets//ratings.csv')
        movie_titles = pd.read_csv("Datasets\movies.csv")
        df = pd.merge(df,movie_titles,on='movieId')
        ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
        ratings['rcount'] = pd.DataFrame(df.groupby('title')['rating'].count())
        moviemat = df.pivot_table(index='userId',columns='title',values='rating')
        ratings.sort_values('rcount',ascending=False)
        return df,moviemat,ratings

    def recommend_collaborative(self,users = user,min_ratings = 20):
        if(self.col_df == -1):
            self.col_df,self.col_mat,self.ratings = self.calc_collaborative()
        preferences = []
        for i in users:
            preferences.append(i[0])
        l = []
        for i in preferences:
            find_name = self.col_df["title"].str.startswith(i, na = False)
            x = self.col_df['title'][find_name]
            x = list(x)
            if(len(x) >= 1):
                i = x[0]
                rating_vector = self.col_mat[i]
                similar_movies = self.col_mat.corrwith(rating_vector)
                correlation_val = pd.DataFrame(similar_movies,columns=['cor_val'])
                correlation_val = correlation_val.join(self.ratings['rcount'])
                l.append(correlation_val[correlation_val['rcount']>min_ratings])
        
        if(len(l) >= 1):
            mov = []
            for i in range(len(l[0])):
                mov.append([0,l[0].index[i]])
            for i in l:
                k = 0
                for j in i['cor_val']:
                    if(j == j):
                        mov[k][0] += j
                    else:
                        mov[k][0] += 0
                    k+=1
            mov.sort(reverse=True)
            #print()
            #print("Others Also Watched:")
            for i in range(5):
                print("\t",i+1,mov[i][1])
            return mov
        else:
            print()

    def recommend_demographic(self):
        df2 = pd.read_excel('Datasets\data3.xlsx')
        df2=df2.dropna(axis=0)
        df2_cp=df2.dropna().reset_index(drop=True)
        alpha = 2
        beta = 1
        score = []
        for i in range(len(df2_cp)):
            imdb_rating = (df2_cp.loc[i, "imdb_score"])
            tmdb_rating = (df2_cp.loc[i, "tmdb_score"])
            score.append((alpha*imdb_rating + beta*tmdb_rating)/(alpha+beta))
        df2_cp['new_score'] = score
        top_10 = df2_cp.sort_values('new_score', ascending=False)
        y = top_10[["title", "new_score"]]
        num = 1
        # print()
        # print("Don't like any of these? Start Here:")
        for i in y['title']:
            print("\t", num, i)
            num+=1
            if(num == 11):
                break
    def getCorrectedQuery(self,query):
        pass

    def ranked_search(self,query):
        correct_query = self.getCorrectedQuery(query)
        search_results = self.useRecommender([correct_query])

def start(args):
    r = Recommender("D:\Desktop\IR\Git_Project\Information-Retrival-Project\dashin\dashin\merged_genre.csv") # DATASET PATH HERE 
    r.addUsers(args)
    recoms = r.recommend()
    return recoms
    # print(len(r.cosine_sim))
