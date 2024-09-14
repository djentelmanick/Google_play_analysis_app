# -*- coding: utf-8 -*-
"""Модуль для построения графиков
Created on Mon May 20 21:18:56 2024

@author: Николай
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Создание кластеризованных столбчатых диаграмм
def cluster_bar_chart_make1(*, D: pd.DataFrame, quantitative: str) -> None:
    '''This function creates "Cluster Bar Chart".
    Save is in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Матвей
    '''
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Content_rating', y=quantitative, hue='Type', data=D, width=0.6)
    plt.xlabel('Content_rating')
    plt.ylabel(quantitative)
    # plt.ticklabel_format(style='plain', axis='y')
    plt.title('Кластеризованная столбчатая диаграмма')
    plt.show()


def cluster_bar_chart_make2(*, D: pd.DataFrame,
                            quantitative: str) -> None:
    '''This function creates "Cluster Bar Chart".
    Save is it in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Матвей
    '''
    plt.figure(figsize=(10, 7))
    sns.barplot(x='Category', y=quantitative, hue='Type', data=D, width=0.6)
    plt.xlabel('Category')
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel(quantitative)
    plt.title('Кластеризованная столбчатая диаграмма')
    plt.subplots_adjust(top=0.92, bottom=0.22)
    plt.show()


# Создание категоризированных гистограмм
def categorized_histogram_make(*, D: pd.DataFrame, qualitative: str,
                               quantitative: str) -> None:
    '''This function creates "Categorized Histogram".
    Save is it in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    qualitative : str
        Qualitative attribute of the df.
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None

    @author: Андрей
    '''
    plt.figure(figsize=(10, 6))
    sns.histplot(data=D, x=quantitative, hue=qualitative, multiple="dodge", bins=10)
    plt.title('Категоризированная гистограмма')
    plt.xlabel(quantitative)
    plt.ylabel('Количество')
    plt.show()


# Создание категоризированных диаграмм box-and-whiskers
def categorized_box_and_whisker_plot_make1(*, D: pd.DataFrame, qualitative: str,
                                           quantitative: str) -> None:
    '''This function creates "Categorized box-and-whisker Plot".
    Save is it in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    qualitative : str
        Qualitative attribute of the df.
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Николай
    '''
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=qualitative, y=quantitative, data=D)
    plt.title('Категоризированная диаграмма box-and-whiskers')
    plt.xlabel(qualitative)
    plt.ylabel(quantitative)
    plt.show()


def categorized_box_and_whisker_plot_make2(*, D: pd.DataFrame, quantitative: str) -> None:
    '''This function creates "Categorized box-and-whisker Plot".
    Save is it in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Николай
    '''
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='Category', y=quantitative, data=D)
    plt.title('Категоризированная диаграмма box-and-whiskers')
    plt.xlabel('Category')
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel(quantitative)
    plt.subplots_adjust(top=0.92, bottom=0.22)
    plt.show()


# Создание категоризированных диаграмм рассеивания
def categorized_scatterplot_make(*, D: pd.DataFrame, qualitative: str, quantitative1: str,
                                 quantitative2: str) -> None:
    '''This function creates "Categorized Scatterplot".
    Save is it in the working directory in the folder "graphics".
    

    Parameters
    ----------
    D : pd.DataFrame
    qualitative : str
        Qualitative attribute of the df.
    quantitative1 : str
        Quantitative attribute of the df.
    quantitative2 : str
        Another quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Андрей
    '''
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=quantitative1, y=quantitative2, hue=qualitative, data=D)
    plt.title('Категоризированная диаграмма рассеивания')
    plt.xlabel(quantitative1)
    plt.ylabel(quantitative2)
    plt.subplots_adjust(left=0.07, right=0.82, top=0.95, bottom=0.1)
    if qualitative == 'Category':
        plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.58), fontsize=8)
    if qualitative == 'Content_rating':
        plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.82))
    if qualitative == 'Type':
        plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.9))
        plt.subplots_adjust(left=0.07, right=0.9, top=0.95, bottom=0.1)
    plt.show()


def bar_for_genres_make(*, D: pd.DataFrame, quantitative: str) -> None:
    '''This function creates "bar" for best 20 genres by a specific attribute
    
    
    Parameters
    ----------
    D : pd.DataFrame
    quantitative : str
        Quantitative attribute of the df.

    Returns
    -------
    None
    
    @author: Николай
    '''
    ratings_counts = D.groupby('Genres')[quantitative].mean().sort_values(
        ascending=False).head(20)
    ratings_counts.plot(kind='bar').set_ylabel(quantitative)
    plt.xlabel('Genres')
    plt.title('Топ-20 жанров по определенному атрибуту')
    plt.subplots_adjust(top=0.92, bottom=0.4)
    plt.show()
