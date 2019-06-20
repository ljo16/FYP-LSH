from matplotlib import pyplot as plt
import seaborn
import pandas as pd
import numpy as np
import pylab

ix = pd.IndexSlice
df = pd.DataFrame(data=[(2, 50), (50, 2), (10, 10), (5, 20), (20, 5)], columns=['pieces', 'size'])
df['hashes'] = df['pieces'] * df['size']
for pr in np.linspace(0, 1, 200):
    df[pr] = 1 - (1 - pr**df['size']) ** df['pieces']

df = pd.pivot_table(df, index=['hashes', 'pieces', 'size'])

ax = df.T.plot(figsize=(10, 7), title='Probability of being candidate pairs given actual Jaccard similarity, s');
plt.ylabel('p(candidate | Jaccad)');
plt.xlabel('Jaccard similarity, s, of a pair of documents');
plt.legend(list(df.loc[ix[100]].index),
           bbox_to_anchor=(1., 1, 1., 0), loc='upper left', fontsize=12, 
           ncol=1, borderaxespad=0., title='Each line represents\nchoosing (b bands, r rows)\n');

plt.savefig('banding.png', bbox_inches='tight')
