import json
import pandas as pd

class Task1:
    def __init__(self, filepath, dirpath):
        self.dirpath = dirpath
        self.filepath = filepath
        self.tags_dict = {}
        self.topic_tags_dict = {}
    
    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    
    def get_tags(self, df):
        return df['tags']
    
    def get_grouped_topics(self, df):
        return df[['topic','tags']]
    
    def build_tags_histogram(self, sr):
        size = sr.size
        sr = [ele.split(", ") for ele in sr]
        for i in range(size):
            for tag in sr[i]:
                if tag != '':
                    if tag not in self.tags_dict.keys():
                        self.tags_dict[tag] = 1
                    else:
                        self.tags_dict[tag] += 1
    
    def get_100_first(self):
        sr = self.get_tags(self.convert_to_dataframe(self.filepath))
        self.build_tags_histogram(sr)
        sorted_histogram = pd.Series(self.tags_dict).sort_values(ascending=False)
        result = list(sorted_histogram.head(n=100).index)
        with open('%s/100_first_popular_tags.txt' % self.dirpath, 'a') as f:
            f.write('100 tags phổ biến nhất là:\n')
            for r in result:
                f.write('- %s\n' % r)
    
    def countX(self, lst, x): 
        return lst.count(x) 
    
    def build_seperate_histogram(self):
        df = self.convert_to_dataframe(self.filepath)
        cur_df = self.get_grouped_topics(df)
        grouped_dict = cur_df.groupby('topic').groups
        for key in grouped_dict.keys():
            tags_dict = {}
            index_list = list(grouped_dict[key])
            sr = cur_df['tags'][index_list].apply(lambda x: x.split(', '))
            for i in range(sr.size):
                for tag in sr.iloc[i]:
                    if tag != '':
                        if tag not in tags_dict.keys():
                            tags_dict[tag] = 1
                        else:
                            tags_dict[tag] += 1
            sorted_hist = pd.Series(tags_dict).sort_values(ascending=False)
            res = list(sorted_hist.head(n=20).index)
            self.topic_tags_dict[key] = res
        with open('%s/20_first_popular_tags_each.txt' % self.dirpath, 'a') as f:
            for key in self.topic_tags_dict.keys():
                f.write('- 20 tags phổ biến nhất trong chủ đề %s:\n' % key)
                f.write(', '.join(self.topic_tags_dict[key]))
                f.write('\n')
            
    
    def main(self):
        self.get_100_first()
        self.build_seperate_histogram()
        
                
if __name__=="__main__":
    DIRPATH = "result/"
    FILEPATH = "/home/vudat1710/Downloads/Training OSP/Training week 1-2/Fresher_Data_Science_week1-2/Week 1/Crawler/baomoicrawler/data_week_2.json"
    a = Task1(FILEPATH, DIRPATH)
    a.main()