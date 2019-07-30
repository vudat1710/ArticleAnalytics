import re, json, math, operator, pickle
import constants as cs
import pandas as pd
import numpy as np

class Task4:
    def __init__(self, filepath):
        self.filepath = filepath
        self.vocab = []
        self.word_dict = {}
        self.topic_words_dict = {}
    
    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df

    def build_word_histogram_tokenized(self, df):
        size = df.shape[0]
        for i in range(size):
            for word in df.loc[i]['content']:
                if word not in self.word_dict:
                    self.word_dict[word] = 1
                    self.vocab.append(word)
                else:
                    self.word_dict[word] += 1
    
    def turn_to_onehot(self, content, word_unique):
        onehot = [0] * len(word_unique)
        for word in content:
            index = word_unique.index(word)
            onehot[index] = 1
        return onehot

    


    #tf-idf
    def computeTF(self, word_dict_topic, words):
        tf_dict = {}
        wordsCount = len(words)
        for word, count in word_dict_topic.items():
            tf_dict[word] = count/float(wordsCount)
        return tf_dict
    
    def compute_word_dict(self, corpus):
        word_dict = {}
        for i in range(len(corpus)):
            for word in corpus[i]['content']:
                if word.lower() in word_dict:
                    word_dict[word.lower()] += 1
                else:
                    word_dict[word.lower()] = 1
        return word_dict

    def compute_word_dict_each(self, corpus):
        word_list = []
        for i in range(len(corpus)):
            word_dict = {}
            for word in corpus[i]['content']:
                if word.lower() in word_dict:
                    word_dict[word.lower()] += 1
                else:
                    word_dict[word.lower()] = 1
            word_list.append(word_dict)
            del word_dict
        with open("dict/word_list.pkl", 'wb') as f:
            pickle.dump(word_list, f)
    
    def computeIDF(self, corpus, word_dict):
        idf_dict = {}
        N = len(corpus)
        idf_dict = dict.fromkeys(word_dict.keys(), 0)
        for each in corpus:
            for word in each.keys():
                idf_dict[word] += 1
        for word, val in idf_dict.items():
            idf_dict[word] = math.log10(N / float(val))
        return idf_dict
        # idf_dict = self.computeIDF(word_list, word_dict)

    def computeTFIDF(self, tf_dict, idf_dict): 
        tfidf_dict = {}
        for word, val in tf_dict.items():
            tfidf_dict[word] = val * idf_dict[word]
        return tfidf_dict
    
    def computeTFIDFVector(self, tfidf_dict, word_unique, content):
        tfidf_vector = [0.0] * len(word_unique)
        for word in content:
            if word in tfidf_dict:
                i = word_unique.index(word)
                tfidf_vector[i] = tfidf_dict[word]
        return tfidf_vector

    def cosine(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def euclide(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.linalg.norm(a-b)
    
    def jaccard(self, a, b):
        a = np.array(a)
        b = np.array(b)
        intersection = len(set(a).intersection(set(b)))
        union = len(set(a).union(set(b)))
        return intersection / float(union)

    def main(self):
        df = self.convert_to_dataframe(self.filepath)

        with open(self.filepath, 'r') as f:
            data = json.load(f)
        f.close()
        word_dict = self.compute_word_dict(data)
        # print (word_dict)
        # self.compute_word_dict_each(data)
        # with open('dict/word_list.pkl', 'rb') as fi:
        #     word_list = pickle.load(fi)
        # fi.close()
        # tf_dict = []
  
        content = list(df['content'])
        content = [x for x in content if x!= []]
        for i in range(len(content)):
            content[i] = [word.lower() for word in content[i]]
        # for i in range(len(content)):
        #     each_tf_dict = self.computeTF(word_list[i], content[i])
        #     tf_dict.append(each_tf_dict)
        # print("done tf")
        # idf_dict = self.computeIDF(word_list, word_dict)
        # print("done idf")
        # tfidf_dict = [self.computeTFIDF(each_tf_dict, idf_dict) for each_tf_dict in tf_dict]
        # print ("done tfidf")
        # with open('tfidf.pkl', 'wb') as f:
        #     pickle.dump(tfidf_dict, f)
        # f.close()
        with open('tfidf.pkl', 'rb') as f:
            tfidf_dict = pickle.load(f)
        f.close()
        word_unique = list(word_dict.keys())
        a = self.computeTFIDFVector(tfidf_dict[4], word_unique, content[4])
        b = self.computeTFIDFVector(tfidf_dict[5], word_unique, content[5])
        print (a)
        a1 = self.turn_to_onehot(content[4], word_unique)
        b1 = self.turn_to_onehot(content[5], word_unique)
        print(self.cosine(a,b))
        print(self.euclide(a,b))  
        print(self.jaccard(a,b))

if __name__=="__main__":
    filepath = "tokenized_content_3.json"
    a = Task4(filepath)
    a.main()