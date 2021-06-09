import pandas as pd

class DeepDiveAnalysis:
    def __init__(self,path,sheet) -> None:
        self.path = path
        self.sheet = sheet
        self.level = ["Zone", "Subbrand", "Region", "Brand"] #Edit this list to add new levels
        self.df = pd.read_excel(path,sheet_name=sheet)
    
    '''
        This Function preprocesses the DataFrame.
        The Format of the Month Column has been changed to meet the requirements in the question.
        A new column names Period is created and the old column month is dropped.
    '''
    def preprocess(self):
        self.df["Period"] = pd.to_datetime(self.df['month'], format='%m').dt.month_name().str.slice(stop=3)
        self.df["Period"] = self.df["Period"].astype(str)+self.df["month"].dt.year.astype(str)
        self.df = self.df.drop(labels=["month"],axis=1)
    
    '''
        This function checks the sales volume of the target period and the reference period.
    '''
    def check_sales(self,manufacturer, target_period, reference_period):
        df_=self.df[self.df["Manufacturer"]==manufacturer]
        g1 = df_[df_["Period"]==target_period]['Value Offtake(000 Rs)'].sum()
        g2 = df_[df_["Period"]==reference_period]['Value Offtake(000 Rs)'].sum()
        if(g1>g2):
            return True
        else:
            return False
    

    '''
        Function to compute the Growth Rate using Sales Volume.
    '''
    def growth_rate(self, manufacturer, level, focus_area, target_period, reference_period):
        df_ = self.df[(self.df[level]==focus_area) & (self.df["Manufacturer"]==manufacturer)]
        g1 = df_[df_["Period"]==target_period]['Value Offtake(000 Rs)'].sum()
        g2 = df_[df_["Period"]==reference_period]['Value Offtake(000 Rs)'].sum()
        return round(((g1-g2)*100/g2),2)


    '''
        Function to compute the Contribution using Sales Volume.
    '''
    def contribution(self, manufacturer, level, focus_area, target_period):
        df_ = self.df[self.df['Manufacturer']==manufacturer]
        g1 = df_[(df_["Period"]==target_period) & (df_[level]==focus_area)]['Value Offtake(000 Rs)'].sum()
        g2 = df_[df_["Period"]==target_period]['Value Offtake(000 Rs)'].sum()
        # print(g1,"----->",g2)
        return round(((g1/g2)*100),2)

    '''
        Function to fetch focus areas relevant to the Manufacturer.
    '''
    def fetch_focus_areas(self, Manufacturer):
        df_ = self.df[self.df["Manufacturer"]==Manufacturer]
        focus_area=dict()
        for i in self.level:
            focus_area[i] = set(df_[i].values)
        return self.level,focus_area


    '''
        This is the Function relevant to the quesiton given to me.
    '''
    def func(self, Manufacturer,target_period, reference_period):
        if(self.check_sales(manufacturer=Manufacturer, target_period=target_period, reference_period=reference_period)):
            message= str("There is no decline in sales for "+Manufacturer+" during "+str(reference_period)+" "+str(target_period))
            return message
        else:
            df_ = self.df[self.df["Manufacturer"]==Manufacturer]
            levels, focus_areas = self.fetch_focus_areas(Manufacturer=Manufacturer)
            output_df = dict()
            index = 0
            for level in levels:
                for focus_area in focus_areas[level]:
                    output_df[index] = dict()
                    output_df[index]["Manufacturer"] = Manufacturer
                    output_df[index]["level"] = level
                    output_df[index]["focus_area"] = focus_area
                    output_df[index]["growth_rate"] = self.growth_rate(manufacturer=Manufacturer, level=level, focus_area=focus_area, target_period=target_period, reference_period=reference_period)
                    output_df[index]["contribution"] = self.contribution(manufacturer=Manufacturer, level=level, focus_area=focus_area, target_period=target_period)
                    output_df[index]["product"] = output_df[index]["growth_rate"]*output_df[index]["contribution"]
                    # print(output_df[index])
                    index+=1
            
            return_df = pd.DataFrame(output_df).transpose()
            return return_df



