# -*- coding: utf-8 -*-
"""Модуль для приведения данных к третьей нормальной форме
Created on Thu May 16 12:59:03 2024

@author: Николай
"""

import pandas as pd
import numpy as np

# Чтение датасета
df = pd.read_csv(r'C:\work\data\googleplaystore.csv')

## Подготовка данных
# Удаление неанализируемых столбцов
df.drop(['Last Updated', 'Current Ver', 'Android Ver'], axis=1, inplace=True)

# Удаление дубликатов
df.drop_duplicates(keep='first', subset=['App'], inplace=True)

# Преобразование 'Installs' в целочисленный тип
df['Installs'] = df['Installs'].apply(lambda x : x.replace('+',"") if '+' in str(x) else x)
df['Installs'] = df['Installs'].apply(lambda x : x.replace(',',"") if ',' in str(x) else x)
df = df[df['Installs']!='Free']
df['Installs'] = df['Installs'].astype(int)

# Испрвим пустое значение 'Type' на 'Free' там, где 'Installs' = 0
df.loc[df['Type'].isnull(), 'Type'] = 'Free'

# Преобразование 'Size' в вещественный тип
def convert_size_to_bytes(size_str) -> float:
    '''This function convert attribute 'Size' to bytes
    
    
    Parameters
    ----------
    size_str : str

    Returns
    -------
    float
    
    @author: Николай
    '''
    if size_str == 'Varies with device':
        return np.nan
    if size_str.endswith('M'):
        return float(size_str[:-1]) * 1024 * 1024
    if size_str.endswith('k'):
        return float(size_str[:-1]) * 1024
    return np.nan


df['Size'] = df['Size'].apply(convert_size_to_bytes)


# Преобразование 'Reviews' в целочисленный тип
df['Reviews'] = df['Reviews'].astype(int)

# Преобразование 'Price' в целочисленный тип
df['Price'] = df['Price'].apply(lambda x : float(x.replace('$',"")) if '$' in str(x) else float(x))

# Переименование столбцов
df.rename(columns = {'Size': 'Size_in_bytes'}, inplace=True)
df.rename(columns = {'Content Rating': 'Content_rating'}, inplace=True)
df.rename(columns = {'Price': 'Price_in_dollars'}, inplace=True)

# Восстановление правильной индексации
df.reset_index(drop=True, inplace=True)

df1 = df[['App', 'Genres']]

for ind, row in df1.iterrows():
    if ';' in row['Genres']:
        df1.loc[len(df1)] = {'App': row['App'], 'Genres': row['Genres'][row['Genres'].find(';')+1:]}
        df1.loc[ind] = {'App': row['App'], 'Genres': row['Genres'][:row['Genres'].find(';')]}

df1.drop_duplicates(inplace=True)
df1.sort_values(by='App', ascending=True, inplace=True)
df1.reset_index(drop=True, inplace=True)
df1.to_pickle('c:/work/data/3nf_Genres_from_Apps.pkl')

df2 = df[['Price_in_dollars', 'Type']]
df2.drop_duplicates(inplace=True)
df2.sort_values(by='Price_in_dollars', ascending=True, inplace=True)
df2.reset_index(drop=True, inplace=True)
df2.to_pickle('c:/work/data/3nf_Type_from_Price.pkl')

df_3nf = df.drop(['Type', 'Genres'], axis=1)
df_3nf.to_pickle('c:/work/data/3nf_Basic.pkl')
