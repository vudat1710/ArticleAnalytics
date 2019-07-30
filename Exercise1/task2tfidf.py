import json, math, os, operator, re
import pandas as pd
import numpy as np
import constants as cs
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

class Task2Tfidf:  
    def __init__(self, dirpath):
        self.dirpath = dirpath

    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    
    def computeTF(self, word_dict_topic, words):
        tf_dict = {}
        wordsCount = len(words)
        for word, count in word_dict_topic.items():
            tf_dict[word] = count/float(wordsCount)
        return tf_dict
    
    def compute_word_dict(self, corpus):
        word_dict = {}
        for topic in corpus.keys():
            for word in corpus[topic]:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        return word_dict
    
    def compute_word_dict_by_topic(self, word_dict, corpus):
        word_dict_topic = dict.fromkeys(word_dict, 0)
        for word in corpus:
            word_dict_topic[word] += 1
        return word_dict_topic
    
    def computeIDF(self, corpus):
        idf_dict = {}
        N = len(corpus)
        idf_dict = dict.fromkeys(corpus[0].keys(), 0)
        for doc in corpus:
            for word, val in doc.items():
                if val > 0:
                    idf_dict[word] += 1
        for word, val in idf_dict.items():
            idf_dict[word] = math.log10(N / float(val))
        return idf_dict

    def computeTFIDF(self, tf_dict, idf_dict): 
        tfidf_dict = {}
        for word, val in tf_dict.items():
            tfidf_dict[word] = val * idf_dict[word]
        return tfidf_dict

    def create_data_corpus(self):
        DIRECTORY = "data/"
        data = {}
        for filename in os.listdir(DIRECTORY):
            if filename.endswith(".json"):
                print ("%s" % filename)
                filepath = "%s%s" %(DIRECTORY, filename)
                df = self.convert_to_dataframe(filepath)
                content = list(df['content'])
                content = [x for x in content if x!= []]
                top = []
                for i in range(len(content)):
                    content[i] = [word.lower() for word in content[i]]
                    top = top + content[i]
                data.update({filename[:-5] : top})
                # data.update({filename[:-5] : content})
                print("done")
        with open('data2.json', 'w') as f:
            json.dump(data, f)
        print(data['Pháp luật'])
        return (data)
    
    def computeTFIDFVector(self, tfidf_dict, word_dict, content):
        word_unique = word_dict.unique()
        tfidf_vector = [0.0] * len(word_unique)
        for i, word in enumerate(word_unique):
            if word in tfidf_dict:
                tfidf_vector[i] = tfidf_dict[word]
        return tfidf_vector

    def get_top20(self):
        with open('%s/data.json' % self.dirpath, 'r') as f:
            data = json.load(f)
        tf_dict = []
        word_dict = self.compute_word_dict(data)
        dict_topic = []
        for topic in data.keys():
            word_dict_topic = self.compute_word_dict_by_topic(word_dict, data[topic])
            dict_topic.append(word_dict_topic)
            each_tf_dict = self.computeTF(word_dict_topic,data[topic])
            tf_dict.append(each_tf_dict)
        idf_dict = self.computeIDF(dict_topic)
        tfidf_dict = [self.computeTFIDF(each_tf_dict, idf_dict) for each_tf_dict in tf_dict]
        result = []
        for i in range(len(tfidf_dict)):
            sorted_hist = pd.Series(dict(tfidf_dict[i])).sort_values(ascending=False)
            result.append(list(sorted_hist.head(n=20).index))
        topics = list(data.keys())
        dictonary = dict(zip(topics, result))
        with open("%s/20_first_popular_words_each_tfidf.txt" % self.dirpath, 'w') as f:
            for topic in dictonary.keys():
                f.write('- 20 từ khóa phổ biến nhất trong chủ đề %s:\n' % topic)
                f.write(', '.join(dictonary[topic]))
                f.write('\n')
        f.close()

    def main(self):
        # self.create_data_corpus()
        self.get_top20()

if __name__=="__main__":
    # FILEPATH = 'tokenized_content_3.json'
    dirpath = "."
    a = Task2Tfidf(dirpath)
    a.main()
    

    