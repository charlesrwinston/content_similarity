import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
import sys

import numpy as np
import json


screenName = sys.argv[1]

sortedUserEntities = json.loads(open('data/{}-sorted-user-entities.json'.format(screenName), 'r').read())
sortedSampleEntities = json.loads(open('data/{}-sorted-sample-entities.json'.format(screenName), 'r').read())
userEntities = json.loads(open('data/{}-user-entities.json'.format(screenName), 'r').read())
sampleEntities = json.loads(open('data/{}-sample-entities.json'.format(screenName), 'r').read())
entityDimensions = json.loads(open('data/{}-entity-dimensions.json'.format(screenName), 'r').read())

totalUserMentions = sum([item[1] for item in sortedUserEntities])
totalSampleMentions = sum([item[1] for item in sortedSampleEntities])
dpoints = []
if sys.argv[2] == 'user':
    filename = '{}-top-entities-chart.png'.format(screenName)
    title = '{}\'s Top Entities'.format(screenName)
    for item in sortedUserEntities[:10]:
        ent = item[0]
        count = item[1]
        sampleCount = sampleEntities[ent] if ent in sampleEntities else 0
        userPercent = 100 * count / float(totalUserMentions)
        samplePercent = 100 * sampleCount / float(totalSampleMentions)
        dpoints.append([screenName, ent, userPercent])
        dpoints.append(['Network', ent, samplePercent])
elif sys.argv[2] == 'network':
    filename = '{}-network-top-entities-chart.png'.format(screenName)
    title = '{} Network\'s Top Entities'.format(screenName)
    for item in sortedSampleEntities[:10]:
        ent = item[0]
        count = item[1]
        userCount = userEntities[ent] if ent in userEntities else 0
        userPercent = 100 * userCount / float(totalUserMentions)
        samplePercent = 100 * count / float(totalSampleMentions)
        dpoints.append([screenName, ent, userPercent])
        dpoints.append(['Network', ent, samplePercent])

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
