
# Day 6 of AoC 2018: Chronal Coordinates
https://adventofcode.com/2018/day/6

## Part one


```python
import pandas as pd
import numpy as np
import altair as alt
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import distance
```


```python
points = pd.read_csv('day06_input.txt', names=['x', 'y'])
```


```python
len(points)
```




    50




```python
points['label'] = range(len(points))
```


```python
labels = alt.Chart(points).mark_text(color='red').encode(
    x=alt.X('x:Q'),
    y=alt.Y('y:Q'),
    text=alt.Text('label:N')
)
labels
```




![png](day06_files/day06_6_0.png)



I will make a classifier with k nearest neighbors, using 1 neighbor and Manhattan distance. And then I will use this classifier to predict all points on a grid.


```python
knn = KNeighborsClassifier(n_neighbors=1, metric="manhattan")
```


```python
knn.fit(points.values, np.arange(50))
```




    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='manhattan',
               metric_params=None, n_jobs=1, n_neighbors=1, p=2,
               weights='uniform')



I used [this answer from stackoverflow](https://stackoverflow.com/questions/32208359/is-there-a-multi-dimensional-version-of-arange-linspace-in-numpy) to create the grid


```python
x_min, x_max = points.x.min(), points.x.max()
y_min, y_max = points.y.min(), points.y.max()
grid = np.mgrid[x_min:(x_max+1), y_min:(y_max+1)].reshape(2,-1).T
```


```python
grid.shape
```




    (98596, 2)




```python
predictions = knn.predict(grid)
```


```python
predictions_df = pd.DataFrame({'x':grid[:, 0],
                               'y':grid[:, 1],
                               'pred':predictions
                              })
```


```python
predictions_df.to_csv('day06_grid_predictions.csv', index=False)
```


```python
grid_chart = alt.Chart('day06_grid_predictions.csv').mark_point().encode(
    x=alt.X('x:Q'),
    y=alt.Y('y:Q'),
    color=alt.Color('pred:N', legend=None, scale=alt.Scale(scheme='category20')),
    tooltip='pred:N'
)

grid_chart + labels
```




![png](day06_files/day06_16_0.png)



Looks good! The area that seems to be overlapping are due to the fact that there are only 20 colors in the scheme, while I want to plot 50 zones, we can see that they are indeed separated with the tooltip.

I have to only take into account the finite areas, so any area that "touches" the ends has to be dismissed.


```python
def find_infinite_area(pred, num_labels=50, x_min=x_min, 
                       x_max=x_max, y_min=y_min, y_max=y_max):
    """
    Returns a set of labels the touches the ends
    """
    infinite_area = set()
    x_min
    for label in range(num_labels):
        label_df = pred.query('pred == @label')
        if (x_min in label_df['x'].values) or (x_max in label_df['x'].values)\
          or (y_min in label_df['y'].values) or (y_max in label_df['y'].values):
            infinite_area.add(label)
    return infinite_area
```


```python
infinite_area = find_infinite_area(predictions_df)
print(infinite_area)
```

    {0, 2, 4, 5, 7, 11, 14, 17, 19, 20, 23, 24, 25, 27, 30, 32, 33, 35, 36, 37, 39, 40, 41, 45}


I update the dataframe


```python
predictions_df['infinite'] = predictions_df['pred'].isin(infinite_area)
```


```python
predictions_df.to_csv('day06_grid_predictions.csv', index=False)
```


```python
grid_chart.encode(color=alt.Color('infinite:O')) + labels
```




![png](day06_files/day06_24_0.png)



OK, it seems to have done a good job! Let's now filter those areas and count the number of values, which will give the total area. I will have to take care of points being at an equal distance of 2 data points.


```python
predictions_df.query('not infinite')['pred'].value_counts()[:5]
```




    10    3960
    1     3661
    6     3454
    22    3433
    48    2588
    Name: pred, dtype: int64



So, the area 10 is the largest. The value does not take into account that I should not count the points that are at the same distance of 2 labels.


```python
area10 = predictions_df.query('pred == 10').loc[:, ['x', 'y']].values
```


```python
cityblock(area10[0], points.query('label == 10').loc[:, ['x', 'y']].values)
```




    34




```python
def center_coord(id):
    return points.loc[id, ['x', 'y']].values.reshape(-1, 2)


def matrix_neighbor(ids=None):
    if ids is None:
        # This is from visual inspection
        ids = [33, 20, 22, 42, 46]
    all_neighbors = np.zeros(shape=(len(ids), 2))
    for i, id in enumerate(ids):
        all_neighbors[i, :] = center_coord(id)
    return all_neighbors
```


```python
coords_neighbors_10 = matrix_neighbor()
```


```python
distances_neighbors = distance.cdist(area10, coords_neighbors_10, metric='cityblock')
```


```python
distances_10 = distance.cdist(area10, center_coord(10), metric='cityblock')
```


```python
differences = distances_neighbors - distances_10
```


```python
np.sum(np.any(differences == 0, axis=1))
```




    66



There are 66 ties in the distances, so we must substract those from the area.


```python
print(f'Solution for part 1: {len(area10) - 66}')
```

    Solution for part 1: 3894


## Part 2


```python
np.sum(np.sum(, axis=1) < 10000)
```




    39398



Let's compute the distance for our grid of points to all the points.


```python
all_distances = distance.cdist(grid, points.loc[:, ['x', 'y']].values, metric='cityblock')
```

Now, we need to sum all the distances.


```python
sum_distances = np.sum(all_distances, axis=1)
```

We need to find and count the values that are less than 10000.


```python
print(f'Solution for part 2: {np.sum(sum_distances < 10000)}')
```

    Solution for part 2: 39398


Just for fun, plot this


```python
predictions_df['sum_dist'] = sum_distances
predictions_df['close'] = sum_distances < 10000
```


```python
predictions_df.to_csv('day06_grid_predictions.csv', index=False)
```


```python
grid_chart.encode(color=alt.Color('sum_dist:Q', bin=True),
                  tooltip=['sum_dist:Q', 'close:O']) + labels.mark_point(color='red')
```




![png](day06_files/day06_49_0.png)


