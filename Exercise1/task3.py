import json, pickle
import pandas as pd 
from underthesea import pos_tag

class Task3:
    def __init__(self, filepath, dirpath):
        self.dirpath =dirpath
        self.filepath = filepath
        self.content = []
        self.content_postag = []
        self.noun_list = []
        self.proper_noun_list = []
        self.topic_noun_dict = {}
        self.topic_pnoun_dict = {}

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
    
    def get_all_contents(self, data, df):
        for i in range(len(data)):
            # content = data[i]['content']
            self.content.append(data[i]['content'])
            self.content_postag.append(pos_tag(data[i]['content']))
            print(i)
        postag = pd.DataFrame({'postag': self.content_postag})
        postag_df = pd.concat([df, postag], axis=1)
        postag_df.to_json('data_week_2_postag.json',orient='records')
        self.dump_to_pickle('content_postag.pkl', self.content_postag)
    
    def build_nouns(self, df):
        for _list in df['postag']:
            noun_dict = {}
            proper_noun_dict = {}
            for ele in _list:
                if ele[1] is 'N':
                    word = ele[0]
                    if word in noun_dict:
                        noun_dict[word] += 1
                    else:
                        noun_dict[word] = 1
                if ele[1] == 'Np':
                    word = ele[0]
                    if word in proper_noun_dict:
                        proper_noun_dict[word] += 1
                    else:
                        proper_noun_dict[word] = 1
            self.noun_list.append(noun_dict)
            self.proper_noun_list.append(proper_noun_dict)
            del noun_dict
            del proper_noun_dict
        nouns = pd.DataFrame({'nouns': self.noun_list})
        proper_nouns = pd.DataFrame({'propernouns': self.proper_noun_list})
        noun_df = pd.concat([df, nouns, proper_nouns], axis=1)
        noun_df.to_json('data_week_2_noun.json', orient='records')

    def dump_to_pickle(self, filepath, data):
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        f.close()
    
    def get_100_first_propernoun(self):
        df = self.convert_to_dataframe(self.filepath)
        proper_nouns = df['propernouns']
        Np_dict = {}
        for _dict in proper_nouns:
            for word in _dict.keys():
                if word not in Np_dict:
                    Np_dict[word] = _dict[word]
                else:
                    Np_dict[word] += _dict[word]
        sorted_histogram = pd.Series(Np_dict).sort_values(ascending=False)
        result = list(sorted_histogram.head(n=100).index)
        with open("%s/top_100_propernouns.txt" % self.dirpath, 'w') as f:
            f.write('100 danh từ riêng phổ biến nhất là:\n')
            for r in result:
                f.write('- %s\n' % r)
    
    def build_seperate_histogram(self):
        cur_df = self.convert_to_dataframe(self.filepath)
        grouped_dict = cur_df.groupby('topic').groups
        # print(cur_df)
        for key in grouped_dict.keys():
            noun_dict = {}
            propernoun_dict = {}
            vocab = []
            index_list = list(grouped_dict[key])
            for i in index_list:
                noun = cur_df['nouns'][i]
                propernoun = cur_df['propernouns'][i]
                for n in noun.keys():
                    if n in noun_dict:
                        noun_dict[n] += noun[n]
                    else:
                        noun_dict[n] = noun[n]
                for np in propernoun.keys():
                    if np in propernoun_dict:
                        propernoun_dict[np] += propernoun[np]
                    else:
                        propernoun_dict[np] = propernoun[np]
                # print (words)
                
            noun_sorted_hist = pd.Series(noun_dict).sort_values(ascending=False)
            noun_res = list(noun_sorted_hist.head(n=20).index)
            self.topic_noun_dict[key] = noun_res
            pnoun_sorted_hist = pd.Series(propernoun_dict).sort_values(ascending=False)
            pnoun_res = list(pnoun_sorted_hist.head(n=20).index)
            self.topic_pnoun_dict[key] = pnoun_res
        with open('%s/20_first_popular_noun_each.txt' % self.dirpath, 'a') as f:
            for key in self.topic_noun_dict.keys():
                f.write('- 20 danh từ phổ biến nhất trong chủ đề %s:\n' % key)
                f.write(', '.join(self.topic_noun_dict[key]))
                f.write('\n')
        f.close()
        with open('%s/20_first_popular_pnoun_each.txt' % self.dirpath, 'a') as f:
            for key in self.topic_pnoun_dict.keys():
                f.write('- 20 danh từ riêng phổ biến nhất trong chủ đề %s:\n' % key)
                f.write(', '.join(self.topic_pnoun_dict[key]))
                f.write('\n')
        f.close()
    
    def main(self):
        # with open(self.filepath, 'r') as f:
        #     data = json.load(f)
        # f.close()
        # df = self.convert_to_dataframe(self.filepath)
        # with open('data_week_2_postag.json','r') as f:
        #     data = json.load(f)
        # self.get_all_contents(data, df)
        # print("done postag")

        # df_postag = self.convert_to_dataframe('data_week_2_postag.json')
        # self.build_nouns(df_postag)
        # print("done nouns")
        self.get_100_first_propernoun()
        self.build_seperate_histogram()


if __name__=="__main__":
    DIRPATH = "result/"
    a = Task3('data_week_2_noun.json', DIRPATH)
    a.main()
    