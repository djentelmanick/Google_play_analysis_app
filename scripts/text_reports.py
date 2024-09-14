# -*- coding: utf-8 -*-
"""Модуль для построения текстовых отчетов
Created on Tue May 21 09:03:33 2024

@author: Николай
"""

from typing import Callable
import pandas as pd

# Создание функции для генерации сводной таблицы
def pivot_table_make(*, D: pd.DataFrame, x: list, y: str, val: int, func: Callable) -> pd.DataFrame:
    '''This function creates "Pivot table".
    

    Parameters
    ----------
    x : list
        List of the attributes of the df. Column of the Pivot table.
    y : str
        Another attribute of the df. Row of the Pivot table.
    val : int
        Values of the df.
    func : Callable
        Some kind of function for processing values.

    Returns
    -------
    pd.DataFrame
        The resulting Pivot table.
    
    @author: Андрей
    '''
    D = pd.pivot_table(D, values=val, index=y, columns=x, aggfunc=func)
    D.reset_index(inplace=True)
    return D


# Создание функции для генерации фильтрованного df
def filtered_report(*, D: pd.DataFrame, names:list, cndname:str,
                   cndval:str) -> pd.DataFrame:
    '''This function creates a report from the df according to certain criteria.
    

    Parameters
    ----------
    D : pd.DataFrame
    names : list
        Attributes for the report.
    cndname : str
        Criterion attribute.
    cndval : str
        Value of the criterion.

    Returns
    -------
    statement : pd.DataFrame
        The resulting report.
    
    @author: Николай
    '''
    if '*' in cndval:
        x_i = cndval.find('*')
        ind = D.loc[(D[cndname] >= float(cndval[:x_i-1])) &
                    (D[cndname] <= float(cndval[x_i+2:]))].index
    elif '>' in cndval:
        ind = D[cndname] > float(cndval[1:])
    elif '<' in cndval:
        ind = D[cndname] < float(cndval[1:])
    else:
        ind = D[cndname] == cndval
    statement = D.loc[ind, names]
    return statement

# Создание функции для генерации отчета о качественном атрибуте
def report_for_qualitative(*, D: pd.DataFrame, x: str) -> pd.DataFrame:
    '''This function creates a report for the qualitive attribute of the df.
    

    Parameters
    ----------
    D : pd.DataFrame
    x : str
        One of the qualitive attribute of the df.

    Returns
    -------
    qualitative_freq_table : pd.DataFrame
        The resulting report.
    
    @author: Николай
    '''
    qualitative_freq_table = D[x].value_counts().reset_index()
    qualitative_freq_table.columns = ['Level', 'Frequency']
    qualitative_freq_table['Percentage'] = round(qualitative_freq_table['Frequency'] /
                                                 len(D) * 100, 1)
    return qualitative_freq_table


# Создание функции для генерации отчета о количественных атрибутах
def report_for_list_quantitatives(*, D: pd.DataFrame, x:list) -> pd.DataFrame:
    '''This function creates a report for the quantitatives attributes of the df.
    

    Parameters
    ----------
    D : pd.DataFrame
    x : list
        The list of the quantitatives attributes of the df.

    Returns
    -------
    transposed_df : pd.DataFrame
        The resulting report.
    
    @author: Матвей
    '''
    quantitative_stats = D[x].describe().reset_index()
    quantitative_stats.columns = [''] + x
    quantitative_stats.loc[len(D.describe())] = ['variance'] + [D[i].var() for i in x]
    transposed_df = quantitative_stats.T.reset_index()
    transposed_df.columns = transposed_df.iloc[0] # Первая строка как заголовки
    transposed_df = transposed_df.drop(0)
    transposed_df.reset_index(drop=True, inplace=True)
    return transposed_df


# Создание функции для генерации корреляционного отчета
def correlation_report(*, D: pd.DataFrame(), x:list) -> pd.DataFrame():
    '''This function creates a correlarion report for df.


    Parameters
    ----------
    D : pd.DataFrame
    x : list
        The list of the quantitatives attributes of the df.

    Returns
    -------
    pd.DataFrame
        The resulting report.
    
    @author: Матвей
    '''
    D = D[x].corr()
    D.reset_index(inplace=True)
    D.rename(columns = {'index': ''}, inplace=True)
    return D
