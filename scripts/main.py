# -*- coding: utf-8 -*-
"""Модуль с основным кодом (интерфейсом)
Created on Fri Apr 12 13:25:32 2024

@author: Николай
"""
# Подключение библиотек
import os
import configparser
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog as pathd
import pandas as pd
import graphics as gra
import text_reports as tr

# Нахождение родительской папки с кодом
parent_dir_path = os.path.dirname(os.path.abspath(__file__))
# Определение каталога работы
os.chdir(parent_dir_path)


def show_df(dft):
    '''Просмотр и сохранение текстового отчета
    In: dft - pd.DataFrame для текстового отчтета
    Out: None
    
    @author: Николай'''
    def clck():
        """Обработка нажатия кнопки"""
        dft.to_excel(f'../output/{entry.get()}.xlsx', index=False)
        print('Отчет был успешно сохранен в work/output')
    treport = tki.Tk()
    treport.title('Текстовый отчет')
    # Создаем Treeview
    cont = tki.Frame(treport, bg=rtwind_bg)
    cont.pack(padx=10)
    tree = ttk.Treeview(cont, columns=list(dft.columns), show='headings')
    for col in dft.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=8, side='left', anchor='center', expand=1)
    scrl = tki.Scrollbar(cont, command=tree.yview)
    scrl.pack(side='right', anchor='e', fill = 'y')
    # Заполняем данными
    for _, row in dft.iterrows():
        tree.insert("", "end", values=list(row))
    cont1 = tki.Frame(treport, bg=rtdop_bg)
    cont1.pack(pady=8, ipady=5, padx=5)
    lbl = tki.Label(cont1, text='Введите название отчета', font=dop_font,
                    bg=rtdop_bg)
    lbl.pack(side='left', padx=5)
    btn = tki.Button(cont1, text='Сохранить', font=base_font,
                    bg=base_bg, command=clck)
    btn.pack(side='right', padx=5)
    entry = tki.Entry(cont1)
    entry.pack(side='right')
    btn_ex = tki.Button(treport, text='Выход', font=base_font,
                    bg=base_bg, command=treport.destroy)
    btn_ex.pack(anchor='se', pady=[10, 10], padx=[0, 10], expand=1)
    treport.config(bg=rtwind_bg)
    treport.mainloop()


def edit_df_b():
    '''Редактор справочника DFB
    In, out: None
    
    @author: Матвей'''
    def contf():
        '''Создание таблицы'''
        global CONT
        CONT = tki.Frame(treport, bg=rtwind_bg)
        CONT.pack(padx=10, pady=10, anchor='n', expand=1)
        tree = ttk.Treeview(CONT, columns=list(DFB.reset_index().columns), show='headings')
        for col in list(DFB.reset_index().columns):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(pady=8, side='left', anchor='center', expand=1)
        scrl = tki.Scrollbar(CONT, command=tree.yview)
        scrl.pack(side='right', anchor='e', fill = 'y')
        # Заполняем данными
        for _, row in DFB.reset_index().iterrows():
            tree.insert("", "end", values=list(row))
    def clck3():
        '''Обработка нажатия кнопки удалить'''
        global DFM, DFALL
        DFB.drop(int(entry3.get()), inplace=True)
        DFB.reset_index(drop=True, inplace=True)
        DFM = DFB.merge(DFT, on='Price_in_dollars')
        DFALL = DFM.merge(DFG, on='App')
        CONT.destroy()
        contf()
    def clck2():
        """Обработка нажатия кнопки сохранить"""
        DFB.to_pickle(f'../data/{entry2.get()}.pkl')
        print('Справочник был успешно сохранен в work/data')
    def clck1():
        '''Обработка нажатия кнопки добавить'''
        global DFB, DFM, DFALL
        add_str = list(entry1.get().split())
        if len(add_str) == 8:
            for i in range(2, 7):
                if i == 3 or i == 5:
                    add_str[i] = int(add_str[i])
                else:
                    add_str[i] = float(add_str[i])
            add_row = pd.Series(add_str, index=DFB.columns)
            DFB = pd.concat([DFB, add_row.to_frame().T], ignore_index=True)
            DFB[['Rating', 'Size_in_bytes', 'Price_in_dollars']] = \
            DFB[['Rating', 'Size_in_bytes', 'Price_in_dollars']].astype(float)
            DFB[['Reviews', 'Installs']] = DFB[['Reviews', 'Installs']].astype(int)
            DFM = DFB.merge(DFT, on='Price_in_dollars')
            DFALL = DFM.merge(DFG, on='App')
            CONT.destroy()
            contf()
        else:
            print('Невозможно добавить такую строку')

    treport = tki.Tk()
    treport.title('Редактор')
    # Создаем Treeview
    cont1 = tki.Frame(treport, bg=rtdop_bg)
    cont1.pack(pady=8, ipady=5, padx=5)
    lbl1 = tki.Label(cont1, text='Введите строку для добавления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl1.pack(side='top', pady=[5, 0])
    btn1 = tki.Button(cont1, text='Добавить', font=base_font,
                    bg=base_bg, command=clck1)
    btn1.pack(side='right', padx=[0, 5])
    entry1 = tki.Entry(cont1, width=17*len(DFB.columns)+1)
    entry1.pack(side='left', padx=5)
    cont3 = tki.Frame(treport, bg=rtdop_bg)
    cont3.pack(pady=2, ipady=5, padx=5)
    lbl3 = tki.Label(cont3, text='Введите индекс строки для удаления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl3.pack(side='left', padx=5)
    btn3 = tki.Button(cont3, text='Удалить', font=base_font,
                    bg=base_bg, command=clck3)
    btn3.pack(side='right', padx=5)
    entry3 = tki.Entry(cont3)
    entry3.pack(side='right')
    cont2 = tki.Frame(treport, bg=rtdop_bg)
    cont2.pack(pady=9, ipady=5, padx=5)
    lbl2 = tki.Label(cont2, text='Введите название справочника',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl2.pack(side='left', padx=5)
    btn2 = tki.Button(cont2, text='Сохранить', font=base_font,
                    bg=base_bg, command=clck2)
    btn2.pack(side='right', padx=5)
    entry2 = tki.Entry(cont2)
    entry2.pack(side='right')
    contf()
    treport.config(bg=rtwind_bg)
    treport.mainloop()


def edit_df_t():
    '''Редактор справочника DFT
    In, out: None
    
    @author: Андрей'''
    def contf():
        '''Создание таблицы'''
        global CONT
        CONT = tki.Frame(treport, bg=rtwind_bg)
        CONT.pack(padx=10, pady=10, anchor='n', expand=1)
        tree = ttk.Treeview(CONT, columns=list(DFT.reset_index().columns), show='headings')
        for col in list(DFT.reset_index().columns):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(pady=8, side='left', anchor='center', expand=1)
        scrl = tki.Scrollbar(CONT, command=tree.yview)
        scrl.pack(side='right', anchor='e', fill = 'y')
        # Заполняем данными
        for _, row in DFT.reset_index().iterrows():
            tree.insert("", "end", values=list(row))
    def clck3():
        '''Обработка нажатия кнопки удалить'''
        global DFM, DFALL
        DFT.drop(int(entry3.get()), inplace=True)
        DFT.reset_index(drop=True, inplace=True)
        DFM = DFB.merge(DFT, on='Price_in_dollars')
        DFALL = DFM.merge(DFG, on='App')
        CONT.destroy()
        contf()
    def clck2():
        """Обработка нажатия кнопки сохранить"""
        DFT.to_pickle(f'../data/{entry2.get()}.pkl')
        print('Справочник был успешно сохранен в work/data')
    def clck1():
        '''Обработка нажатия кнопки добавить'''
        global DFT, DFM, DFALL
        add_str = list(entry1.get().split())
        if len(add_str) == 2:
            add_str[0] = float(add_str[0])
            add_row = pd.Series(add_str, index=DFT.columns)
            DFT = pd.concat([DFT, add_row.to_frame().T], ignore_index=True)
            DFT[['Price_in_dollars']] = DFT[['Price_in_dollars']].astype(float)
            DFM = DFB.merge(DFT, on='Price_in_dollars')
            DFALL = DFM.merge(DFG, on='App')
            CONT.destroy()
            contf()
        else:
            print('Невозможно добавить такую строку')

    treport = tki.Tk()
    treport.title('Редактор')
    # Создаем Treeview
    cont1 = tki.Frame(treport, bg=rtdop_bg)
    cont1.pack(pady=8, ipady=5, padx=5)
    lbl1 = tki.Label(cont1, text='Введите строку для добавления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl1.pack(side='top', pady=[5, 0])
    btn1 = tki.Button(cont1, text='Добавить', font=base_font,
                    bg=base_bg, command=clck1)
    btn1.pack(side='right', padx=[0, 5])
    entry1 = tki.Entry(cont1, width=15*len(DFT.columns)+1)
    entry1.pack(side='left', padx=5)
    cont3 = tki.Frame(treport, bg=rtdop_bg)
    cont3.pack(pady=2, ipady=5, padx=5)
    lbl3 = tki.Label(cont3, text='Введите индекс строки для удаления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl3.pack(side='left', padx=5)
    btn3 = tki.Button(cont3, text='Удалить', font=base_font,
                    bg=base_bg, command=clck3)
    btn3.pack(side='right', padx=5)
    entry3 = tki.Entry(cont3)
    entry3.pack(side='right')
    cont2 = tki.Frame(treport, bg=rtdop_bg)
    cont2.pack(pady=9, ipady=5, padx=5)
    lbl2 = tki.Label(cont2, text='Введите название справочника',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl2.pack(side='left', padx=5)
    btn2 = tki.Button(cont2, text='Сохранить', font=base_font,
                    bg=base_bg, command=clck2)
    btn2.pack(side='right', padx=5)
    entry2 = tki.Entry(cont2)
    entry2.pack(side='right')
    contf()
    treport.config(bg=rtwind_bg)
    treport.mainloop()


def edit_df_g():
    '''Редактор справочника DFG
    In, out: None
    
    @author: Николай'''
    def contf():
        '''Создание таблицы'''
        global CONT
        CONT = tki.Frame(treport, bg=rtwind_bg)
        CONT.pack(padx=10, pady=10, anchor='n', expand=1)
        tree = ttk.Treeview(CONT, columns=list(DFG.reset_index().columns), show='headings')
        for col in list(DFG.reset_index().columns):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(pady=8, side='left', anchor='center', expand=1)
        scrl = tki.Scrollbar(CONT, command=tree.yview)
        scrl.pack(side='right', anchor='e', fill = 'y')
        # Заполняем данными
        for _, row in DFG.reset_index().iterrows():
            tree.insert("", "end", values=list(row))
    def clck3():
        '''Обработка нажатия кнопки удалить'''
        global DFM, DFALL
        DFG.drop(int(entry3.get()), inplace=True)
        DFG.reset_index(drop=True, inplace=True)
        DFM = DFB.merge(DFT, on='Price_in_dollars')
        DFALL = DFM.merge(DFG, on='App')
        CONT.destroy()
        contf()
    def clck2():
        """Обработка нажатия кнопки сохранить"""
        DFG.to_pickle(f'../data/{entry2.get()}.pkl')
        print('Справочник был успешно сохранен в work/data')
    def clck1():
        '''Обработка нажатия кнопки добавить'''
        global DFG, DFM, DFALL
        add_str = list(entry1.get().split())
        if len(add_str) == 2:
            add_str[0] = float(add_str[0])
            add_row = pd.Series(add_str, index=DFG.columns)
            DFG = pd.concat([DFG, add_row.to_frame().T], ignore_index=True)
            DFM = DFB.merge(DFT, on='Price_in_dollars')
            DFALL = DFM.merge(DFG, on='App')
            CONT.destroy()
            contf()
        else:
            print('Невозможно добавить такую строку')

    treport = tki.Tk()
    treport.title('Редактор')
    # Создаем Treeview
    cont1 = tki.Frame(treport, bg=rtdop_bg)
    cont1.pack(pady=8, ipady=5, padx=5)
    lbl1 = tki.Label(cont1, text='Введите строку для добавления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl1.pack(side='top', pady=[5, 0])
    btn1 = tki.Button(cont1, text='Добавить', font=base_font,
                    bg=base_bg, command=clck1)
    btn1.pack(side='right', padx=[0, 5])
    entry1 = tki.Entry(cont1, width=17*len(DFG.columns)+1)
    entry1.pack(side='left', padx=5)
    cont3 = tki.Frame(treport, bg=rtdop_bg)
    cont3.pack(pady=2, ipady=5, padx=5)
    lbl3 = tki.Label(cont3, text='Введите индекс строки для удаления',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl3.pack(side='left', padx=5)
    btn3 = tki.Button(cont3, text='Удалить', font=base_font,
                    bg=base_bg, command=clck3)
    btn3.pack(side='right', padx=5)
    entry3 = tki.Entry(cont3)
    entry3.pack(side='right')
    cont2 = tki.Frame(treport, bg=rtdop_bg)
    cont2.pack(pady=9, ipady=5, padx=5)
    lbl2 = tki.Label(cont2, text='Введите название справочника',
                     font=('Arial', 11, 'italic'), bg=rtdop_bg)
    lbl2.pack(side='left', padx=5)
    btn2 = tki.Button(cont2, text='Сохранить', font=base_font,
                    bg=base_bg, command=clck2)
    btn2.pack(side='right', padx=5)
    entry2 = tki.Entry(cont2)
    entry2.pack(side='right')
    contf()
    treport.config(bg=rtwind_bg)
    treport.mainloop()


def cbc(wind):
    """Создание cluster_bar_chart_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Матвей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        print("Сохраняйте график в work/graphics")
        if cmb1.get() == 'Content_rating':
            gra.cluster_bar_chart_make1(D=DFM, quantitative=cmb2.get())
        else:
            gra.cluster_bar_chart_make2(D=DFM, quantitative=cmb2.get())
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        lbl2.destroy()
        cmb1.destroy()
        cmb2.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = ('Content_rating', 'Category')
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def cht(wind):
    """Создание categorized_histogram_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Андрей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        print("Сохраняйте график в work/graphics")
        gra.categorized_histogram_make(D=DFM, qualitative=cmb1.get(),
                                            quantitative=cmb2.get())
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        lbl2.destroy()
        cmb1.destroy()
        cmb2.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = ('Type', 'Content_rating')
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def cbawp(wind):
    """Создание categorized_box_and_whisker_plot_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Николай"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        print("Сохраняйте график в work/graphics")
        if cmb1.get() == 'Category':
            gra.categorized_box_and_whisker_plot_make2(D=DFM, quantitative=cmb2.get())
        else:
            gra.categorized_box_and_whisker_plot_make1(D=DFM, qualitative=cmb1.get(),
                                                            quantitative=cmb2.get())
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        lbl2.destroy()
        cmb1.destroy()
        cmb2.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = ('Type', 'Content_rating', 'Category')
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def cst(wind):
    """Создание categorized_scatterplot_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Андрей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        print("Сохраняйте график в work/graphics")
        gra.categorized_scatterplot_make(D=DFM, qualitative=cmb1.get(),
                                              quantitative1=cmb2.get(),
                                              quantitative2=cmb3.get())
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        lbl2.destroy()
        lbl3.destroy()
        cmb1.destroy()
        cmb2.destroy()
        cmb3.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = ('Type', 'Content_rating', 'Category')
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Выбор первого показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    lbl3 = tki.Label(wind, text='Выбор второго показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl3.pack(pady=8)
    cmb3 = ttk.Combobox(wind)
    cmb3['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb3.current(0) #Значение по умолчанию
    cmb3.focus()
    cmb3.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def bfg(wind):
    """Создание bar_for_genres_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Николай"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        print("Сохраняйте график в work/graphics")
        gra.bar_for_genres_make(D=DFALL, quantitative=cmb1.get())
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        cmb1.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def pvt(wind):
    """Создание pivot_table_make
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Андрей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        args = [DFM.columns[k] for k in ltb.curselection()]
        df_tr = tr.pivot_table_make(D=DFM, x=args, y=cmb1.get(),
                            val=cmb2.get(), func=cmb3.get())
        show_df(df_tr)
    def clck2():
        '''Очистка элементов'''
        lbl.destroy()
        ltb.destroy()
        scrl.destroy()
        cont.destroy()
        lbl1.destroy()
        lbl2.destroy()
        lbl3.destroy()
        cmb1.destroy()
        cmb2.destroy()
        cmb3.destroy()
        btnc.destroy()
    lbl = tki.Label(wind, text='Выбор показаетелей >', font=dop_font,
                    bg=dop_bg, fg=dop_fg)
    lbl.pack(pady=8)
    cont = tki.Frame(wind)
    cont.pack()
    ltb = tki.Listbox(cont, selectmode=tki.EXTENDED, height=4, font="Arial 12")
    for i in DFM.columns:
        ltb.insert(tki.END, i)
    ltb.pack(side='left', anchor='center', expand=1)
    scrl = tki.Scrollbar(cont, command=ltb.yview)
    scrl.pack(side='right', anchor='e', fill = 'y')
    lbl1 = tki.Label(wind, text='Выбор другого показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = tuple(DFM.columns)
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Выбор переменной >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = tuple(DFM.select_dtypes(include=['int', 'float']).columns)
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    lbl3 = tki.Label(wind, text='Выбор функции >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl3.pack(pady=8)
    cmb3 = ttk.Combobox(wind)
    cmb3['values'] = ('sum', 'min', 'max')
    cmb3.current(0) #Значение по умолчанию
    cmb3.focus()
    cmb3.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def flr(wind):
    """Создание filtered_report
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Николай"""
    print("*В критерии пишите числа вместо нижнего подчеркивания")
    def clck():
        """
        Обработка нажатия кнопки
        """
        args = [DFM.columns[k] for k in ltb.curselection()]
        df_tr = tr.filtered_report(D=DFM, names=args, cndname=cmb1.get(), cndval=cmb2.get())
        show_df(df_tr)
    def clck2():
        '''Очистка элементов'''
        lbl.destroy()
        ltb.destroy()
        scrl.destroy()
        cont.destroy()
        lbl1.destroy()
        lbl2.destroy()
        cmb1.destroy()
        cmb2.destroy()
        btnc.destroy()
    lbl = tki.Label(wind, text='Выбор показаетелей >', font=dop_font,
                    bg=dop_bg, fg=dop_fg)
    lbl.pack(pady=8)
    cont = tki.Frame(wind)
    cont.pack()
    ltb = tki.Listbox(cont, selectmode=tki.EXTENDED, height=4, font="Arial 12")
    for i in DFM.columns:
        ltb.insert(tki.END, i)
    ltb.pack(side='left', anchor='center', expand=1)
    scrl = tki.Scrollbar(cont, command=ltb.yview)
    scrl.pack(side='right', anchor='e', fill = 'y')
    lbl1 = tki.Label(wind, text='Выбор показателя для критерия >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = tuple(DFM.columns)
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    lbl2 = tki.Label(wind, text='Напишите критерий >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl2.pack(pady=8)
    cmb2 = ttk.Combobox(wind)
    cmb2['values'] = ('', '<_', '>_', '_<*<_')
    cmb2.current(0) #Значение по умолчанию
    cmb2.focus()
    cmb2.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def rfq(wind):
    """Создание report_for_qualitative
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Николай"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        df_tr = tr.report_for_qualitative(D=DFM, x=cmb1.get())
        show_df(df_tr)
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        cmb1.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателя >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    cmb1 = ttk.Combobox(wind)
    cmb1['values'] = tuple(DFM.select_dtypes(include=['object']).columns)
    cmb1.current(0) #Значение по умолчанию
    cmb1.focus()
    cmb1.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def rflq(wind):
    """Создание report_for_list_quantitatives
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Матвей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        args = [DFM.select_dtypes(include=['int', 'float']).columns[k]
                for k in ltb.curselection()]
        df_tr = tr.report_for_list_quantitatives(D=DFM, x=args)
        show_df(df_tr)
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        ltb.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателей >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    ltb = tki.Listbox(wind, selectmode=tki.EXTENDED, height=5, font="Arial 12")
    for i in DFM.select_dtypes(include=['int', 'float']).columns:
        ltb.insert(tki.END, i)
    ltb.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def corr(wind):
    """Создание correlation_report
    In: wind - tkinter.Tk, в котором происходит анализ
    Out: None
    
    @author: Матвей"""
    def clck():
        """
        Обработка нажатия кнопки
        """
        args = [DFM.select_dtypes(include=['int', 'float']).columns[k]
                for k in ltb.curselection()]
        df_tr = tr.correlation_report(D=DFM, x=args)
        show_df(df_tr)
    def clck2():
        '''Очистка элементов'''
        lbl1.destroy()
        ltb.destroy()
        btnc.destroy()
    lbl1 = tki.Label(wind, text='Выбор показателей >', font=dop_font,
                    bg=dop_bg,fg=dop_fg)
    lbl1.pack(pady=8)
    ltb = tki.Listbox(wind, selectmode=tki.EXTENDED, height=5, font="Arial 12")
    for i in DFM.select_dtypes(include=['int', 'float']).columns:
        ltb.insert(tki.END, i)
    ltb.pack()
    btnc = tki.Frame(wind)
    btnc.pack(pady=8, ipadx=5)
    btn = tki.Button(btnc, text='Построить', font=dop_font,
                    bg=dop_bg,fg=dop_fg, command=clck)
    btn.pack(side='left')
    btn2 = tki.Button(btnc, text='Очистить', font=dop_font,
                     bg=dop_bg, fg=dop_fg, command=clck2)
    btn2.pack(side='right')


def open_docr():
    '''This function open "Руководство_разработчика"
    In, out: None
    
    @author: Николай'''
    os.system("start WINWORD.EXE {}".format(r'../notes/Руководство_разработчика.docx'))


def open_docp():
    '''This function open "Руководство_пользователя"
    In, out: None
    
    @author: Николай'''
    os.system("start WINWORD.EXE {}".format(r'../notes/Руководство_пользователя.docx'))


def loaddf():
    """Загрузка данных и их дальнейшая обработка
    In: None
    Out: 0
    
    @author: Николай
    """
    print("Выберите все справочники из каталога work/data с расширением .pkl")
    global DFB, DFT, DFG, DFALL, DFM
    ftypes = [('Двоичный файлы', '*pkl'), ('Excel/csv файлы', ['*.xlsx', '*.csv']),
              ('Все файлы', '*')]
    dlg, dlg2, dlg3 = [pathd.Open(filetypes = ftypes) for _ in range(3)]
    path = [dlg.show(), dlg2.show(), dlg3.show()]
    if len(path[0]) != 0 and len(path[1]) != 0 and len(path[2]) != 0:
        if path[0][-3:] == 'pkl' and path[1][-3:] == 'pkl' and path[2][-3:] == 'pkl':
            path = sorted(path, key=len)
            DFB, DFT, DFG = [pd.read_pickle(i) for i in path]
        else: DFB = pd.DataFrame()
    else: DFB = pd.DataFrame()
    if (not DFB.empty) and (not DFT.empty) and (not DFG.empty):
        path_b, path_t, path_g = [path[i][path[i].rfind('/')+1:] for i in range(3)]
        DFM = DFB.merge(DFT, on='Price_in_dollars')
        DFALL = DFM.merge(DFG, on='App')
        wind = tki.Tk()
        wind.geometry('800x500+200+80')
        wind.title(f"Анализируемые справочники: {path_b}, {path_t}, {path_g}")

        btn_wind_exit = tki.Button(wind, text='Вернуться к\nвыбору справочников', font=base_font,
                        bg=base_bg, command=wind.destroy)
        btn_wind_exit.pack(pady=[0, 10], side='bottom')

        # Создание меню
        mainmenu = tki.Menu(wind, tearoff=0)

        graphic = tki.Menu(wind, tearoff=0)
        graphic.add_command(label="Кластеризованная столбчатая диаграмма",
                            command=lambda: cbc(wind))
        graphic.add_command(label="Категоризированная гистограмма",
                            command=lambda: cht(wind))
        graphic.add_command(label="Категоризированная диаграмма box-and-whiskers",
                            command=lambda: cbawp(wind))
        graphic.add_command(label="Категоризированная диаграмма рассеивания",
                            command=lambda: cst(wind))
        graphic.add_command(label="Столбчатая диаграмма для атрибута 'Genres'",
                            command=lambda: bfg(wind))

        table = tki.Menu(wind, tearoff=0)
        table.add_command(label="По критериям", command=lambda: flr(wind))
        table.add_command(label="О качественном атрибуте", command=lambda: rfq(wind))
        table.add_command(label="О количественных атрибутах", command=lambda: rflq(wind))
        table.add_command(label="Корреляция между атрибутами", command=lambda: corr(wind))
        table.add_command(label="Сводная таблица", command=lambda: pvt(wind))

        doc = tki.Menu(mainmenu, tearoff=0)
        doc.add_command(label="Руководство пользоваетеля", command=open_docp)
        doc.add_command(label="Руководство разработчика", command=open_docr)

        file_edit = tki.Menu(mainmenu, tearoff=0)
        file_edit.add_command(label=f"{path_b}", command=edit_df_b)
        file_edit.add_command(label=f"{path_t}", command=edit_df_t)
        file_edit.add_command(label=f"{path_g}", command=edit_df_g)

        # Размещение пунктов в меню
        mainmenu.add_cascade(label="Справочники", menu=file_edit)
        mainmenu.add_cascade(label="Графический отчет", menu=graphic)
        mainmenu.add_cascade(label="Текстовый отчет", menu=table)
        mainmenu.add_cascade(label="Документации", menu=doc)

        wind.config(menu=mainmenu, bg=wind_bg)
        wind.mainloop()

    return 0

# Создание объекта парсера
conf = configparser.ConfigParser()
# Считывание файла conf.ini
conf.read('conf.ini')
# Конфигурация
base_bg = conf.get('base', 'bg')
base_font = eval(conf.get('base', 'font'))
base4_bg = conf.get('base4', 'bg')
base4_font = eval(conf.get('base4', 'font'))
head_bg = conf.get('head', 'bg')
head_font = eval(conf.get('head', 'font'))
wind_bg = conf.get('wind', 'bg')
dop_bg = conf.get('dop', 'bg')
dop_fg = conf.get('dop', 'fg')
dop_font = eval(conf.get('dop', 'font'))
rtwind_bg = conf.get('rtwind', 'bg')
rtdop_bg = conf.get('rtdop', 'bg')


root = tki.Tk()
root.geometry('500x300+350+180')
root.title("Анализ данных")
lb_start = tki.Label(root, text='Вас приветсвтвует приложение для анализа данных!',
                      bg=head_bg, font=head_font)
lb_start.pack(pady=8, ipady=4, ipadx=3, fill='x')
btn_start = tki.Button(root, text='Выберите справочники', font=base4_font,
                bg=base4_bg, command=loaddf)
btn_start.pack(pady=30, anchor='center')
btn_start_exit = tki.Button(root, text='Выход', font=base_font,
                bg=base_bg, command=root.destroy)
btn_start_exit.pack(pady=[0, 10], padx=[0, 10], anchor='se', expand=1)

root.config(bg=wind_bg)
root.mainloop()
