import json, os
import pandas as pd
from task1 import Task1
from task2 import Task2
from task3 import Task3
from task2tfidf import Task2Tfidf

class Task5:
    def convert_to_dataframe(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    
    def create_month_df(self, df):
        df['time'] = df['time'].apply(lambda x: x[:8])
        df['month'] = pd.DatetimeIndex(df['time'])
        df.to_json('data_week_2_not_tokenized_month.json', orient='records')
    
    def get_100_first_tags(self):
        for filename in os.listdir("month/month_tokenized"):
            if filename.endswith("json"):
                a = Task1("month/month_tokenized/%s" % filename, "month/month_tokenized/month_%s" % filename[:-5])
                a = Task3("month/month_not_tokenized/%s" % filename, "month/month_not_tokenized/month_%s" % filename[:-5])
                a = Task2Tfidf("month/month_tokenized/month_%s" % filename[:-5])
                a.main()
                print("done %s" % filename)

    def main(self):
        # df = self.convert_to_dataframe('data_week_2_noun.json')
        # self.create_month_df(df)
        self.get_100_first_tags()

if __name__=="__main__":
    a = Task5()
    a.main()

    
