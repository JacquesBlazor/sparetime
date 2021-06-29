url = 'https://data.gov.tw/dataset/116285'
import pandas as pd
dataset = pd.read_json('53a72b2dcfdd9ecae43afda4b86089be_export.json', encoding='utf-8')
dataset.columns
dataset['縣市'] = dataset['醫事機構地址'].str.slice(0, 3)
dataset[(dataset['成人口罩剩餘數']+dataset['兒童口罩剩餘數'])<50]
