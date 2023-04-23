import nltk
import pandas as pd
nltk.download('punkt',quiet=True)
nltk.download("stopwords",quiet=True)
import string 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pickle

class Query:
    input_li = []
    # op_li = []

    def tokenize_seq(self,new_s):
        new_s = new_s.lower()
        translate_table = dict((ord(char), " ") for char in string.punctuation)   
        new_s = new_s.translate(translate_table)
        li = word_tokenize(new_s)
        stop_words = set(stopwords.words("english"))
        filter_li = []
        for words in li:
            if(words not in stop_words):
                filter_li.append(words)
        return filter_li

    def __init__(self,input_seq):
        input_li = self.tokenize_seq(input_seq)
        # op_li = []
        # first_op_li = []
        # if(op_seq != ""):
        #     first_op_li = op_seq.split(",")
        #     for i in range(len(first_op_li)):
        #         temp_l = first_op_li[i].split()
        #         for j in temp_l:
        #             op_li.append(j)
        # for i in range(len(op_li)):
        #     op_li[i] = (op_li[i].strip()).lower()
        self.input_li = input_li
        # self.op_li = op_li
    
    def getQuery(self):
        return self.input_li

class Inverted_Index:

    inverted_ind = {}
    # universal_set = set()
    # comparisons = 0
    # document_count = 0
    # name_arr = []

    def __init__(self):
        self.inverted_ind = {}
        # self.universal_set = set()
        # self.comparisons = 0
        # self.document_count = 0
        # self.name_arr = []
       
    # def extract_text(self,s,find_tags = False, remove_separators = False):
    #     new_s = s[::]
    #     if(find_tags):
    #         start = [0,0] #Start is inclusive 
    #         end = [0,0] #End is exclusive
    #         for i in range(len(s)):
    #             if(i + 7 <= len(s) and s[i:i+7] == "<TITLE>"):
    #                 start[0] = i+7
    #             elif(i + 8 <= len(s) and s[i:i+8] == "</TITLE>"):
    #                 end[0] = i
    #             elif(i + 6 <= len(s) and s[i:i+6] == "<TEXT>"):
    #                 start[1] = i+6
    #             elif(i + 7 <= len(s) and s[i:i+7] == "</TEXT>"):
    #                 end[1] = i
    #         new_s = s[start[0]:end[0]] + " " + s[start[1]:end[1]]
    #     if(remove_separators):
    #         new_s = " ".join(new_s.split("\n"))
    #         new_s = " ".join(new_s.split("-"))
    #     return new_s
    
    def addDoc(self,token_list,title): #token list in order, id of parent document 
        for i in range(len(token_list)):
            key = token_list[i]
            if(key in self.inverted_ind.keys()):
                self.inverted_ind[str(key)].append(title)
            else:
                li = [title]
                self.inverted_ind[str(key)] = li
            # self.universal_set.add(title)
                
    def new_Data(self,title,text):
        # f = open(path,"r")
        # s = f.read()
        # f.close()
        # new_s = self.extract_text(s)
        new_s = text
        new_s = new_s.lower()
        
        translate_table = dict((ord(char), " ") for char in string.punctuation)   
        new_s = new_s.translate(translate_table)
        li = word_tokenize(new_s)
        stop_words = set(stopwords.words("english"))
        filter_li = []
        for words in li:
            if(words not in stop_words):
                filter_li.append(words)
        filter_li = list(set(filter_li))
        self.addDoc(filter_li,title)
        # self.name_arr.append(path)
        # self.document_count+=1

    def showWord(self,key):
        return self.inverted_ind[str(key)]
    
    def getFreq(self,key):
        return len(self.inverted_ind[key])

    # def simplify_not(self,op_seq):
    #     if(op_seq == []):
    #         return op_seq
    #     simplified_seq = []
    #     not_count = 1
    #     for i in range(len(op_seq)-1):
    #         if(op_seq[i+1] == op_seq[i] and op_seq[i] == "not"):
    #             not_count+=1
    #         else:
    #             if(op_seq[i] == "not"):
    #                 if(not_count%2 == 1):
    #                     simplified_seq.append(op_seq[i])
    #                 not_count = 1
    #             else:
    #                 simplified_seq.append(op_seq[i])
    #     if(op_seq[len(op_seq)-1] == "not"):
    #         if(not_count%2 == 1):
    #             simplified_seq.append(op_seq[len(op_seq)-1])
    #     else:
    #         simplified_seq.append(op_seq[len(op_seq)-1])
    #     return simplified_seq
    
    def processQuery(self,input_seq):
        # self.comparisons = 0
        query = Query(input_seq)
        input_li = query.getQuery()
        op_li = ['or' for i in range(len(input_li)-1)]
        #op_li = ['and' for i in range(len(input_li)-1)]
        og_qry = self.getStringQuery(input_li,op_li)
        # op_li = self.simplify_not(op_li)
        # str_qry = self.getStringQuery(input_li,op_li)
        input_li_new = []
        for i in range(len(input_li)):
            if(input_li[i] in self.inverted_ind.keys()):
                input_li_new.append(self.inverted_ind[input_li[i]])
            
        output = self.query_sched(input_li_new,op_li)
        # comp_ans = self.comparisons
        # self.comparisons = 0
        return output,og_qry
    
    def getStringQuery(self,input_li,op_li):
        ans = []
        i = 0
        j = 0
        while(i < len(op_li) and j < len(input_li)):
            if(op_li[i] == "not"):
                ans.append(op_li[i])
                i+=1
            else:
                ans.append(input_li[j])
                j+=1
                ans.append(op_li[i])
                i+=1
        if(j < len(input_li)):
            ans.append(input_li[j])
        final_ans = " ".join(ans)
        return final_ans

    def getOutput(self,input_seq):
        #print("Original Keywords:",inp_seq)
        output, og_qry = self.processQuery(input_seq)
        # print("Generated Query:",og_qry)
        # print("Simplified Input Query:",str_qry)
        # print(output)
        out_list = []
        
        if(len(output) > 0 and len(output[0])>0):
            # print("Number of Documents:",len(output[0]))
            # print("Movie Names:")
            for j in range(len(output[0])):
                out_list.append(str(j) + ". " + output[0][j])
                # print("\t",str(j+1)+".",self.name_arr[output[0][j]])
        else:
            out_list.append("No results found!")
        # print("Number of comparisons for fetching result:",comp_ans)
        return out_list

    
    def query_sched(self,input_li,op_li): #input_li is list of lists, each list in input_li is the doc_list of a regex
        if(len(op_li) == 0):
            return input_li
        # elif(op_li[0] == "not"):
        #     output = self.query_not(input_li[0])
        #     return self.query_sched([output]+input_li[1:],op_li[1:])
        elif(op_li[0] == "and"):
            if(len(op_li) > 1 and op_li[1] == "not"):
                op_li[0] = "not"
                op_li[1] = "and"
                temp = input_li[0]
                input_li[0] = input_li[1]
                input_li[1] = temp
                return self.query_sched(input_li,op_li)
            else:
                output = self.query_and(input_li[0],input_li[1])
        elif(op_li[0]  == "or"):
            # if(len(op_li) > 1 and op_li[1] == "not"):
            #     op_li[0] = "not"
            #     op_li[1] = "or"
            #     temp = input_li[0]
            #     input_li[0] = input_li[1]
            #     input_li[1] = temp
            #     return self.query_sched(input_li,op_li)
            # else:
            # print(input_li)
            if len(input_li)<2:
                output = input_li
            # elif len(input_li[0][1])==0:
            #     output = input_li[0]
            else:
                output = self.query_or(input_li[0],input_li[1])

        new_l = [output]+ input_li[2:]
        return self.query_sched(new_l,op_li[1:])

    def query_and(self,t1,t2):
        t1_li = t1
        t2_li = t2
        merge_li = []
        st = 0
        st2 = 0
        while(st<len(t1_li) and st2 < len(t2_li)):
            if(t1_li[st] == t2_li[st2]):
                merge_li.append(t1_li[st])
                st +=1
                st2 +=1
            elif(t1_li[st]<t2_li[st2]):
                st +=1
            else:
                st2+=1
            # self.comparisons+=1
        return merge_li

    def query_or(self,a,b):
        a_list = a
        b_list = b
        ait = 0
        bit = 0
        output = []
        while(ait < len(a_list) and bit < len(b_list)):
            if(a[ait] < b[bit]):
                output.append(a[ait])
                ait+=1
            elif(a[ait] == b[bit]):
                output.append(a[ait])
                ait+=1
                bit+=1
            else:
                output.append(b[bit])
                bit+=1
            # self.comparisons+=1
        while(ait < len(a_list)):
            output.append(a[ait])
            ait+=1
        while(bit < len(b_list)):
            output.append(b[bit])
            bit+=1
        return output 
    
    # def query_not(self,a):
    #     univ = list(self.universal_set)
    #     univ.sort()
    #     output = []
    #     self.comparisons = 0
    #     ait = 0
    #     for i in range(len(univ)):
    #         if(ait < len(a)):
    #             self.comparisons+=1
    #         if(ait < len(a) and univ[i] == a[ait]):
    #             ait+=1
    #         else:
    #             output.append(univ[i])
    #     return output

def getNum(i):
    return (4-len(str(i)))*"0" + str(i)

def index_recommend(args):
    try:
        #inverted_index = pickle.load(open("D:\Desktop\IR\Git_Project\Information-Retrival-Project\dashin\dashin\baseline1_savefile.pickle", "rb"))
        inverted_index = pickle.load(open("/Users/cloud9xpress/Desktop/codeCloud/dashin_front-end/48_MidReview/baseline1_savefile.pickle", "rb"))
        # print(inverted_index.inverted_ind.keys())
    except (OSError, IOError) as e:
        inverted_index = Inverted_Index()
        # df = pd.read_csv('D:\Desktop\IR\Git_Project\Information-Retrival-Project\dashin\dashin\merged_genre.csv')
        df = pd.read_csv('/Users/cloud9xpress/Desktop/codeCloud/dashin_front-end/48_MidReview/dashin/merged_genre.csv')
        for ind in df.index:
            f = inverted_index.new_Data(str(df['title'][ind]), str(df['title'][ind]) + " " + str(df['cast'][ind]) + " " + str(df['listed_in'][ind]) + " " + str(df['description'][ind]))
        # for j in range(1,1401): # 1,1401
        #     f = inverted_index.new_Data("Data/CSE508_Winter2023_Dataset/cranfield"+getNum(j))
        pickle.dump(inverted_index, open("./baseline1_savefile.pickle", "wb"))
    # inp_seq = input()
    output = inverted_index.getOutput(args)
    return output