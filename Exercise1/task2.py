import json, re, sys
import pandas as pd
from underthesea import word_tokenize, sent_tokenize
import constants as cs

class Task2:
    def __init__(self, filepath, dirpath):
        self.filepath = filepath
        self.dirpath = dirpath
        self.vocab = []
        self.word_dict = {}
        self.topic_words_dict = {}
        self.pattern_special = re.compile(cs.SPECIAL_CHAR)
        self.pattern_punct = re.compile(cs.PUNCTUATION)
        self.pattern_num = re.compile(cs.NUMBER)
        self.stopwords = self.get_list("stopwords.txt",[])
        self.first_names = self.get_list("first_names.txt",[])
    
    def get_list(self, filepath, _list):
        with open(filepath, 'r') as f:
            for line in f.readlines():
                _list.append(line.strip())
        f.close()
        return _list
    
    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    
    def get_content(self, df):
        return df['content']
    
    def get_grouped_topics(self, df):
        return df[['topic','content']]
    
    def check_name(self, word):
        tok = word.split(" ")
        for i in tok:
            if i[0].islower():
                return False
        return True
    
    def normalize_content(self, paragraph):       
        paragraph = re.sub(cs.DATE_MONTH,'', paragraph)
        paragraph = re.sub(cs.FULL_DATE,'', paragraph)
        paragraph = re.sub(cs.MONTH_YEAR,'', paragraph) 
        paragraph = re.sub(cs.TIME,'', paragraph)
        paragraph = re.sub(cs.EMAIL,'', paragraph)
        paragraph = re.sub(cs.URL,'', paragraph)
        paragraph = re.sub(cs.SPECIAL_CHAR, '', paragraph)
        paragraph = re.sub(cs.NUMBER, '', paragraph)
        return paragraph

    def remove_punct(self, _list):
        for i in range(len(_list)):
            if self.pattern_punct.match(_list[i]):
                _list.remove(_list[i])
        return _list

    def dump_tokenized_content(self, df):
        print("Tokenizing...")
        df['content'] = df['content'].apply(lambda x: word_tokenize(self.normalize_content(str(x))))
        df['content'] = df['content'].apply(lambda x: self.remove_punct(x))
        print("Dump to json for further uses...")
        df.to_json('tokenized_content_3.json', orient='records')
    
    def build_word_histogram_tokenized(self, df):
        size = df.shape[0]
        for i in range(size):
            # print(df.loc[i]['content'])
            for word in df.loc[i]['content']:

                # if (not self.pattern_num.match(word) and not self.pattern_special.match(word) and not self.pattern_punct.match(word) and word not in self.stopwords):
                if (word not in self.stopwords):
                    # print(word)
                    if (word in self.first_names or self.check_name(word)):
                        self.word_dict[word] = 1
                    else:
                        if word.lower() not in self.vocab:
                            self.vocab.append(word.lower())
                            self.word_dict[word.lower()] = 1
                        else:
                            self.word_dict[word.lower()] += 1
    
    def get_100_first(self):
        cur_df = self.get_grouped_topics(self.convert_to_dataframe(self.filepath))
        self.build_word_histogram_tokenized(cur_df)
        sorted_histogram = pd.Series(self.word_dict).sort_values(ascending=False)
        result = list(sorted_histogram.head(n=100).index)
        with open('%s/100_keywords.txt' % self.dirpath, 'a') as f:
            f.write('100 từ khóa phổ biến nhất là:\n')
            for r in result:
                f.write('- %s\n' % r)
    
    def countX(self, lst, x): 
        return lst.count(x) 
    
    def build_seperate_histogram(self):
        cur_df = self.convert_to_dataframe(self.filepath)
        grouped_dict = cur_df.groupby('topic').groups
        # print(cur_df)
        for key in grouped_dict.keys():
            word_dict = {}
            vocab = []
            index_list = list(grouped_dict[key])
            for i in index_list:
                words = cur_df['content'][i]
                # print (words)
                for word in words:
                    if (word not in self.stopwords):
                    # print(word)
                        if (word in self.first_names or self.check_name(word)):
                            word_dict[word] = 1
                        else:
                            if word.lower() not in vocab:
                                vocab.append(word.lower())
                                word_dict[word.lower()] = 1
                            else:
                                word_dict[word.lower()] += 1
            sorted_hist = pd.Series(word_dict).sort_values(ascending=False)
            res = list(sorted_hist.head(n=20).index)
            self.topic_words_dict[key] = res
        with open('%s/20_first_popular_words_each.txt' % self.dirpath, 'a') as f:
            for key in self.topic_words_dict.keys():
                f.write('- 20 từ khóa phổ biến nhất trong chủ đề %s:\n' % key)
                f.write(', '.join(self.topic_words_dict[key]))
                f.write('\n')
            
    
    def main(self):
        # print (self.stopwords)
        self.get_100_first()
        self.build_seperate_histogram()
        # string = 'Khi thi đại học là một mình mình đi thi, làm bài nhưng 4 năm đại học để được danh hiệu như hiện tại còn có sự giúp đỡ của bạn bè, thầy cô. Cấp 3 là một bài thi để vào trường, còn ĐH lại là kết quả rèn luyện của cả 4 năm nên Phương Anh nghĩ điểm số cũng có sự đóng góp của nhiều tố khác nữa nên mỗi danh hiệu đều có một cảm xúc riêng. T. 9/10/1000'
        # result = self.normalize_content(string)
        # print (result)
        # df = self.convert_to_dataframe(self())
        # self.dump_tokenized_content(df)
        # a = word_tokenize(self.normalize_content(string))
        # print (self.remove_punct(a))
        
                
if __name__=="__main__":
    DIRPATH = 'result/'
    # FILEPATH = "/home/vudat1710/Downloads/Training OSP/Training week 1-2/Fresher_Data_Science_week1-2/Week 1/Crawler/baomoicrawler/data_week_2.json"
    FILEPATH = 'tokenized_content_3.json'
    a = Task2(FILEPATH, DIRPATH)
    a.main()