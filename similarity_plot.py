import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
import sys

import numpy as np
import json


screenNames = [
    'KingJames',
    'realDonaldTrump',
    'tylerthecreator',
    'kanyewest'
]
dpoints = []
filename = 'similarity-chart.png'
title = 'Similarity Comparison Network to Average'
for screenName in screenNames:
    networkSimilarityObject = json.loads(open('data/{}-similarity.json'.format(screenName), 'r').read())
    avgSimilarityObject = json.loads(open('data/{}-avg-similarity.json'.format(screenName), 'r').read())
    networkSimilarity = networkSimilarityObject['similarity']
    avgSimilarity = avgSimilarityObject['similarity']
    dpoints.append(['Network', screenName, networkSimilarity])
    dpoints.append(['Average', screenName, avgSimilarity])




'''
dpoints = np.array([['rosetta', '1mfq', 9.97],
           ['rosetta', '1gid', 27.31],
           ['rosetta', '1y26', 5.77],
           ['rnacomposer', '1mfq', 5.55],
           ['rnacomposer', '1gid', 37.74],
           ['rnacomposer', '1y26', 5.77],
           ['random', '1mfq', 10.32],
           ['random', '1gid', 31.46],
           ['random', '1y26', 18.16]])
'''
dpoints = np.array(dpoints)

fig = plt.figure()
ax = fig.add_subplot(111)

def barplot(ax, dpoints):
    '''
    Create a barchart for data across different categories with
    multiple conditions for each category.

    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''

    # Aggregate the conditions and the categories according to their
    # mean values
    conditions = [(c, np.mean(dpoints[dpoints[:,0] == c][:,2].astype(float)))
                  for c in np.unique(dpoints[:,0])]
    categories = [(c, np.mean(dpoints[dpoints[:,1] == c][:,2].astype(float)))
                  for c in np.unique(dpoints[:,1])]

    # sort the conditions, categories and data so that the bars in
    # the plot will be ordered by category and condition
    conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
    categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]

    dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))

    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))

    # Create a set of bars at each position
    colors = ['sandybrown', 'steelblue']
    for i,cond in enumerate(conditions):
        indeces = range(1, len(categories)+1)
        vals = dpoints[dpoints[:,0] == cond][:,2].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond,
               #color=cm.Accent(float(i) / n))
               color=colors[i])

    # Set the x-axis tick labels to be equal to the categories
    ax.set_xticks(indeces)
    ax.set_xticklabels(categories)
    plt.setp(plt.xticks()[1], rotation=90)

    # Add the axis labels
    ax.set_ylabel("Percent of Mentions")
    ax.set_xlabel("Entities Mentioned")

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')

barplot(ax, dpoints)
plt.title(title)
plt.gcf().subplots_adjust(bottom=0.35)
plt.savefig('charts/{}'.format(filename))
#plt.show()