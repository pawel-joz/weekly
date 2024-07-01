import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


def weekly_feenics(path, office='Galway'):
    data = pd.read_csv(path, parse_dates=['Time'])

    data = data[~data['Reader'].isna()]

    data.loc[data['Reader'].str.contains('GWY'), 'Office'] = 'Galway'
    data.loc[data['Reader'].str.contains('MNP'), 'Office'] = 'MenloPark'

    data = data.drop(
        columns=['Work Email', 'Work Phone', 'Badge', 'AccessLevels', 'Reader', 'Controller TimeZone', 'Tags', 'Card',
                 'AccessType'])

    data['day'] = data['Time'].dt.day
    data['week'] = data['Time'].dt.strftime('%Y-%U')
    data['weekday'] = data['Time'].dt.day_name()
    data['Time'] = data['Time'].dt.strftime('%m/%d/%Y')

    data = data.drop_duplicates()

    data = data[(data['weekday'] != 'Saturday') & (data['weekday'] != 'Sunday')]

    data = data.sort_values(by='Time')

    print()
    print()

    fig = plt.figure(figsize=(12, 5))
    g = sns.catplot(data=data[data['Office'] == office], x='Time', kind='count', aspect=1.8, hue='weekday')
    ax = g.facet_axis(0, 0)
    for c in ax.containers:
        ax.bar_label(c, label_type='edge')
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle(f'{office} ')
    g.set(xlabel='Day', ylabel='Number of employees')
    plt.xticks(rotation=60)
    plt.show()

    fig = plt.figure(figsize=(2, 6))
    gu = sns.barplot(data=data[data['Office'] == office], x='week',
                     y=data[data['Office'] == office]['Person'].nunique())
    for i in gu.containers:
        gu.bar_label(i)
    plt.title(f'{office} Unique')
    gu.set(xlabel='Week', ylabel='Unique employees')
    plt.xticks(rotation=60)
    plt.show()

    distr = data.groupby(['Office'], as_index=False)['Person'].value_counts()
    gh = sns.histplot(data=distr[distr['Office'] == office], x='count', bins=10)
    gh.set_xticks(range(1, 5))
    gh.set(title=f'Number of days in office - {office}')
    gh.set(xlabel='Number of days in office', ylabel='Number of employees')
    plt.show()

    return data