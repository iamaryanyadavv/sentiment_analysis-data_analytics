import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans


data = pd.read_csv('./clustering/bangkok.csv')
sub = data.iloc[:,2:4]
x = sub["Overall Rating"]
y = sub["Pincode"]

km = KMeans(
    n_clusters=3, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
).fit(sub)
print(km.labels_)
print(km.cluster_centers_)



