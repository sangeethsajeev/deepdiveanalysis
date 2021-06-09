import os
from custom_class import DeepDiveAnalysis

path = os.path.join(os.path.abspath(os.path.dirname(__file__))+"/Case Study - Deep Dive Analysis.xlsx")
sheet = "input_data"

'''
Manufacturers:
GLAXOSMITHKLINE
AMUL
NESTLE
MONDELEZ
KRAFT FOODS
'''


try:
    deepDiveAnalysis = DeepDiveAnalysis(path=path, sheet=sheet)
    deepDiveAnalysis.preprocess()
    '''
        Please use the below function to run the Analysis.
    '''
    # print(deepDiveAnalysis.func(Manufacturer="AMUL", target_period="May2019", reference_period="Apr2019"))
    print(deepDiveAnalysis.func(Manufacturer="NESTLE", target_period="May2019", reference_period="Apr2019"))


except Exception as e:
    print(e)
