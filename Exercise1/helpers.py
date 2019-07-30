import json
import pandas as pd 
import os

class Helpers:
    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df

    def dump_to_json(self, filepath, df):
        df.to_json(filepath, orient='records')

    def classify_data_by_topic(self, df, filepath):
        df.sort_values(by='topic')
        df.set_index(keys=['topic'], drop=False, inplace=True)
        topics = list(df['topic'].unique())
        print (topics)
        for topic in topics:
            topic_df = df.loc[df.topic == topic]
            print ("Dump %s" % topic)
            self.dump_to_json("%s/%s.json" % (filepath, topic), topic_df)
    
    def create_data_corpus(self, DIRECTORY):
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
                print("done %s" % DIRECTORY)
        with open('%s/data.json' % DIRECTORY, 'w') as f:
            json.dump(data, f)
        del data

    def classify_data_by_month(self, df):
        df.sort_values(by='month')
        df.set_index(keys=['month'], drop=False, inplace=True)
        months = list(df['month'].unique())
        print (months)
        for month in months:
            month_df = df.loc[df.month == month]
            print ("Dump %s" % month)
            self.dump_to_json('month/month_not_tokenized/%s.json' % month, month_df)
    
    def create_data_corpus_month(self):
        for i in range(12):
            DIRECTORY = 'month/month_tokenized/month_%d/' % (i+1)
            self.create_data_corpus(DIRECTORY)

    def main(self):
        # with open('data_week_2_noun.json', 'r') as f:
        #     data = json.load(f)
        # df = pd.DataFrame(data)
        # self.classify_data_by_topic(df, "data/data_not_tokenized/")
        # for filename in os.listdir("month/month_not_tokenized/"):
        #     if filename.endswith(".json"):
        #         os.mkdir("month/month_not_tokenized/month_%s" % filename[:-5])
        #         with open('month/month_not_tokenized/%s' % filename, 'r') as f:
        #             data = json.load(f)
        #         df = pd.DataFrame(data)
        #         self.classify_data_by_topic(df, 'month/month_not_tokenized/month_%s' % filename[:-5])
        self.create_data_corpus_month()

if __name__=="__main__":
    a = Helpers()
    a.main()

