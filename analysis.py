#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    df = pd.read_pickle(filename) 
    if verbose:
        print("orig_size={:.1f} MB".format(df.memory_usage(index=True, deep=True).sum()/1048576))
    df['date'] = df['p2a']

    df = df.astype('category')
    
    df['p13a'] = pd.to_numeric(df['p13a'])
    df['p13b'] = pd.to_numeric(df['p13b'])
    df['p13c'] = pd.to_numeric(df['p13c'])
    df['p53'] = pd.to_numeric(df['p53'])
    df['region'] = df['region'].astype(str)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').astype('datetime64[ns]')
    
    if verbose:
        print("new_size={:.1f} MB".format(df.memory_usage(index=True, deep=True).sum()/1048576))
    
    #print(df.info(memory_usage='deep'))
    
    return df


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):

    fig, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
    fig.patch.set_facecolor('gray')
    axs[0].title.set_text("Nasledky nehod v jednotlivych regionoch")

    plt.setp(axs[0], ylabel='Pocet umrti')
    plt.setp(axs[1], ylabel='Pocet tezce ranenych')
    plt.setp(axs[2], ylabel='Pocet lehce ranenych')
    plt.setp(axs[3], ylabel='Pocet nehod')

    df['region'].value_counts().plot(ax=axs[3], kind="bar", rot=0)

    order_list = []
    for label in axs[3].get_xticklabels():
        order_list.append(label.get_text())

    df.groupby(['region'])['p13a'].sum().loc[order_list].plot(ax=axs[0], kind="bar", colormap="autumn", rot=0)    
    df.groupby(['region'])['p13b'].sum().loc[order_list].plot(ax=axs[1], kind="bar", colormap="spring", rot=0)
    df.groupby(['region'])['p13c'].sum().loc[order_list].plot(ax=axs[2], kind="bar", colormap="plasma", rot=0)

    fig.set_size_inches(6.5, 9.5)

    if fig_location:
        fig_location = fig_location.split('/')
        myfile = fig_location[-1]
        fig_location = "/".join(fig_location[0:-1])
        if not os.path.exists(fig_location) and fig_location:
            os.makedirs(fig_location)
        plt.savefig(os.path.join(fig_location, myfile))

    if show_figure:
        plt.show()

    plt.close()

# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):

    pd.options.mode.chained_assignment = None
    fig, axs = plt.subplots(nrows=2, ncols=2)
    df1 = df.loc[(df['region'] == 'JHM')]
    df1['reason'] = pd.cut(df1['p12'], bins=[100,200,300,400,500,600,700], include_lowest=True, right=False, labels=['Nezavinena vodicom', 'Neprimerana rychlost', 'Nespravne predchadzanie', 'Nedanie prednosti', 'Nespravny sposob jazdy', 'Technicka zavada'])
    df1['skoda'] = pd.cut(df1['p53'], bins=[0, 500, 2000, 5000, 10000, 99999999], include_lowest=True, right=False, labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

    g = sns.countplot(x="skoda", hue="reason", data=df1, ax=axs[0,0])
    g.set_title('JHM')
    g.set(xlabel='Skoda [tisic Kc]', ylabel='Pocet')
    g.legend_.remove()
    axs[0,0].set(yscale="log")
    

    df1 = df.loc[(df['region'] == 'LBK')]
    df1['reason'] = pd.cut(df1['p12'], bins=[100,200,300,400,500,600,700], include_lowest=True, right=False, labels=['Nezavinena vodicom', 'Neprimerana rychlost', 'Nespravne predchadzanie', 'Nedanie prednosti', 'Nespravny sposob jazdy', 'Technicka zavada'])
    df1['skoda'] = pd.cut(df1['p53'], bins=[0, 500, 2000, 5000, 10000, 99999999], include_lowest=True, right=False, labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

    g = sns.countplot(x="skoda", hue="reason", data=df1, ax=axs[0,1])
    g.set_title('LBK')
    g.set(xlabel='Skoda [tisic Kc]', ylabel='')
    g.legend_.remove()
    axs[0,1].set(yscale="log")


    df1 = df.loc[(df['region'] == 'PHA')]
    df1['reason'] = pd.cut(df1['p12'], bins=[100,200,300,400,500,600,700], include_lowest=True, right=False, labels=['Nezavinena vodicom', 'Neprimerana rychlost', 'Nespravne predchadzanie', 'Nedanie prednosti', 'Nespravny sposob jazdy', 'Technicka zavada'])
    df1['skoda'] = pd.cut(df1['p53'], bins=[0, 500, 2000, 5000, 10000, 99999999], include_lowest=True, right=False, labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

    g = sns.countplot(x="skoda", hue="reason", data=df1, ax=axs[1,0])
    g.set_title('PHA')
    g.set(xlabel='Skoda [tisic Kc]', ylabel='Pocet')
    g.legend_.remove()
    axs[1,0].set(yscale="log")


    df1 = df.loc[(df['region'] == 'STC')]
    df1['reason'] = pd.cut(df1['p12'], bins=[100,200,300,400,500,600,700], include_lowest=True, right=False, labels=['Nezavinena vodicom', 'Neprimerana rychlost', 'Nespravne predchadzanie', 'Nedanie prednosti', 'Nespravny sposob jazdy', 'Technicka zavada'])
    df1['skoda'] = pd.cut(df1['p53'], bins=[0, 500, 2000, 5000, 10000, 99999999], include_lowest=True, right=False, labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

    g = sns.countplot(x="skoda", hue="reason", data=df1, ax=axs[1,1])
    g.set_title('STC')
    g.set(xlabel='Skoda [tisic Kc]', ylabel='')
    g.legend_.remove()
    axs[1,1].set(yscale="log") 

    handles, labels = axs[1,1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='right', bbox_to_anchor=(1.0, 0.5))

    fig.set_size_inches(13, 10)
    plt.subplots_adjust(right=0.78, wspace=0.2) 

    fig.suptitle('Pricina nehody a skoda')

    if fig_location:
        fig_location = fig_location.split('/')
        myfile = fig_location[-1]
        fig_location = "/".join(fig_location[0:-1])
        if not os.path.exists(fig_location) and fig_location:
            os.makedirs(fig_location)
        plt.savefig(os.path.join(fig_location, myfile))

    if show_figure:
        plt.show()
    
    plt.close()
    
# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):

    pd.options.mode.chained_assignment = None
    fig, axs = plt.subplots(nrows=2, ncols=2)

    df1 = df.loc[(df['region'] == 'JHM')]
    
    df1['reason'] = pd.cut(df1['p16'], bins=[0,1,2,3,4,5,6,7,8,9,10], include_lowest=True, right=False, 
    labels=['Iny stav','Suchy - neznecisteny','Suchy-znecisteny','Mokry','Blato','Poladovica - posypane', 'poladovica - neposypane', 
            'rozliaty olej', 'snehova vrstva','nahla zmena stavu'])

    df1 = df1.reset_index()
    df1['date'] = df1['date'].apply(lambda x: x.strftime('%Y-%m'))
    df1.set_index('date', inplace=True)
    
    pivoted = df1.pivot_table(index=['date','reason'], aggfunc='size')
    pivoted = pivoted.to_frame().reset_index()

    pivoted.columns = ['date', 'reason', 'count']

    g = sns.lineplot(x="date", y="count", hue="reason", data=pivoted, ax=axs[0,0])
    g.set_title('JHM')
    g.set(xlabel='', ylabel='Pocet nehod')
    g.legend_.remove()



    df1 = df.loc[(df['region'] == 'LBK')]
    
    df1['reason'] = pd.cut(df1['p16'], bins=[0,1,2,3,4,5,6,7,8,9,10], include_lowest=True, right=False, 
    labels=['Iny stav','Suchy - neznecisteny','Suchy-znecisteny','Mokry','Blato','Poladovica - posypane', 'poladovica - neposypane', 
            'rozliaty olej', 'snehova vrstva','nahla zmena stavu'])

    df1 = df1.reset_index()
    df1['date'] = df1['date'].apply(lambda x: x.strftime('%Y-%m'))
    df1.set_index('date', inplace=True)
    
    pivoted = df1.pivot_table(index=['date','reason'], aggfunc='size')
    pivoted = pivoted.to_frame().reset_index()

    pivoted.columns = ['date', 'reason', 'count']

    g = sns.lineplot(x="date", y="count", hue="reason", data=pivoted, ax=axs[0,1])
    g.set_title('LBK')
    g.set(xlabel='', ylabel='')
    g.legend_.remove()



    df1 = df.loc[(df['region'] == 'PHA')]
    
    df1['reason'] = pd.cut(df1['p16'], bins=[0,1,2,3,4,5,6,7,8,9,10], include_lowest=True, right=False, 
    labels=['Iny stav','Suchy - neznecisteny','Suchy-znecisteny','Mokry','Blato','Poladovica - posypane', 'poladovica - neposypane', 
            'rozliaty olej', 'snehova vrstva','nahla zmena stavu'])

    df1 = df1.reset_index()
    df1['date'] = df1['date'].apply(lambda x: x.strftime('%Y-%m'))
    df1.set_index('date', inplace=True)
    
    pivoted = df1.pivot_table(index=['date','reason'], aggfunc='size')
    pivoted = pivoted.to_frame().reset_index()

    pivoted.columns = ['date', 'reason', 'count']

    g = sns.lineplot(x="date", y="count", hue="reason", data=pivoted, ax=axs[1,0])
    g.set_title('PHA')
    g.set(xlabel='Rok', ylabel='Pocet nehod')
    g.legend_.remove()



    df1 = df.loc[(df['region'] == 'STC')]
    
    df1['reason'] = pd.cut(df1['p16'], bins=[0,1,2,3,4,5,6,7,8,9,10], include_lowest=True, right=False, 
    labels=['Iny stav','Suchy - neznecisteny','Suchy-znecisteny','Mokry','Blato','Poladovica - posypane', 'poladovica - neposypane', 
            'rozliaty olej', 'snehova vrstva','nahla zmena stavu'])

    df1 = df1.reset_index()
    df1['date'] = df1['date'].apply(lambda x: x.strftime('%Y-%m'))
    df1.set_index('date', inplace=True)
    
    pivoted = df1.pivot_table(index=['date','reason'], aggfunc='size')
    pivoted = pivoted.to_frame().reset_index()

    pivoted.columns = ['date', 'reason', 'count']

    g = sns.lineplot(x="date", y="count", hue="reason", data=pivoted, ax=axs[1,1])
    g.set_title('STC')
    g.set(xlabel='Rok', ylabel='')
    g.legend_.remove()

    

    for j in range(2):
        for k in range(2):
            for i, label in enumerate(axs[j,k].get_xticklabels()):
                if i % 12 != 0:
                    label.set_visible(False)

    handles, labels = axs[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='right', bbox_to_anchor=(1.0, 0.5))

    fig.set_size_inches(15, 10)
    plt.subplots_adjust(right=0.78, wspace=0.1) 

    fig.suptitle('Stav vozovky v case nehod')

    if fig_location:
        fig_location = fig_location.split('/')
        myfile = fig_location[-1]
        fig_location = "/".join(fig_location[0:-1])
        if not os.path.exists(fig_location) and fig_location:
            os.makedirs(fig_location)
        plt.savefig(os.path.join(fig_location, myfile))

    if show_figure:
        plt.show()
    
    plt.close()

if __name__ == "__main__":
    #pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    plot_damage(df, "02_priciny.png", True)
    plot_surface(df, "03_stav.png", True)
