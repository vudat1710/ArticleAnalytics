import csv
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

class Analyze:
    def __init__(self, filepath):
        self.filepath = filepath

    def convert_to_dataframe(self, filepath):
        return pd.read_csv(filepath)
    
    def get_cols_name_and_num_cols(self, df):
        names = list(df.columns)
        print("Số trường trong dataset là: %d" % len(names))
        print("Các trường có trong dataset là: %s" % (', '.join(names)))
    
    def get_num_rows(self, df):
        print("Có %d hàng trong dataset" % (df.shape[0]))
    
    def calc_each_col(self, df):
        for col in list(df.columns):
            current_col = df[col]
            print("Tính toán trường %s:\n" % col)
            print("- Min: %f\n" % current_col.min())
            print("- Max: %f\n" % current_col.max())
            print("- Mean: %f\n" % current_col.mean())
            print("- Variance: %f\n" % current_col.var())
            print("- Standard deviation: %f\n" % current_col.std())
    
    def analyze_draw_hist(self, df):
        fig = plt.figure()
        i = 1
        print("Tần suất tại các cột là:\n")
        for col in list(df.columns):
            _dict = df[col].value_counts().to_dict()
            print("Tần suất tại cột %s là:" % col)
            print(_dict)
            print("\n")
            axes = fig.add_subplot(3,3,i)
            axes.set_title("%s" % col)
            axes = df[col].hist()
            i += 1
        plt.savefig('histogram.png')
    
    def get_max_outcome(self, df):
        sr = df['Outcome'].sort_values(ascending=False)
        print("Trường tương quan nhất với Outcome là: %s" % sr.index[1])

    def corr_cols(self, df):
        print("Methods: 1 for ‘pearson’, 2 for ‘kendall’, 3 for ‘spearman’")
        while(True):
            var = input("Chọn phương thức đánh giá tương quan (điền số từ 1 đến 3): ")
            try:
                method = int(var)
                if 0 < method < 4:
                    break
                else:
                    continue
            except ValueError:
                continue
        if method ==  1:
            corr_df = df.corr(method='pearson')
            print(corr_df)
            self.get_max_outcome(corr_df)
        elif method == 2:
            corr_df = df.corr(method='kendall')
            print(corr_df)
            self.get_max_outcome(corr_df)
        elif method == 3:
            corr_df = df.corr(method='spearman')
            print(corr_df)
            self.get_max_outcome(corr_df)
    
    def z_score(self, df):
        for col in list(df.columns):
            col_z = col + "_zscore"
            cur_df = df[col]
            df[col_z] = (cur_df - cur_df.mean()) / cur_df.std(ddof=0)
        df.to_json('diabetes_zscore.json', orient='records')
        print("Done Z-score!")
    
    def minmax_score(self, df):
        for col in list(df.columns):
            col_mm = col + "_minmax"
            cur_df = df[col]
            df[col_mm] = (cur_df - cur_df.min()) / (cur_df.max() - cur_df.min())
        df.to_json('diabetes_minmax.json', orient='records')
        print("Done Minmax-score")
    
    def binning(self, df):
        bins = [20,31,41,51,61,71,81]
        s = pd.cut(df['Age'], bins)
        return s
    
    def add_columns_range_age(self, df):
        bins = [20,31,41,51,61,71,81]
        temp = np.zeros(shape=(df['Age'].size))
        for i in range(len(bins) - 1):
            df['age_%d_%d' % (bins[i], bins[i+1])] = pd.DataFrame(temp)
        s = self.binning(df)
        grouped = df.groupby(s).groups
        for interval in grouped.keys():
            for index in grouped[interval]:
                df['age_%d_%d' % (interval.left, interval.right)][index] = 1
        df.to_json("diabetes_binning.json", orient='records')
        print("Done binning")

    def main(self):
        df = self.convert_to_dataframe(self.filepath)
        # self.get_cols_name_and_num_cols(df)
        # self.get_num_rows(df)
        # self.calc_each_col(df)
        self.analyze_draw_hist(df)
        # self.corr_cols(df)
        # self.z_score(df)
        # self.minmax_score(df)
        # self.add_columns_range_age(df)

if __name__ == "__main__":
    FILEPATH = "diabetes.csv"
    a = Analyze(FILEPATH)
    a.main()
