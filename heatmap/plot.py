import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plotHeatmap(data, areas_by_axis, figsize=5, **kwargs):
    def findYArea():
        for j in range(areas_by_axis):
            if (i*areas_size) <= x and x <= ((i+1)*areas_size)   and   (j*areas_size) <= y and y <= ((j+1)*areas_size):
                heatmap_df.at[areas_by_axis-j, chr(letter_code)] += 1
                return True
        return False
    
    index = [i+1 for i in range(areas_by_axis)]
    columns = [chr(65+i) for i in range(areas_by_axis)]
    heatmap_df = pd.DataFrame(index=index, columns=columns)
    heatmap_df.fillna(0, inplace=True)
    
    if kwargs.get('player'):
        mask = data['player'] == kwargs.get('player')
        data = data[mask]
    
    for index, row in data.iterrows():
        x, y = row['X'], row['Y']

        areas_size = 100/areas_by_axis
        letter_code = 64
        
        for i in range(areas_by_axis): # For each area in x axis
            letter_code += 1
            if findYArea():
                break
    
    max_value = kwargs.get('max_value')
    if not max_value:
        max_value = heatmap_df.max().max()
    
    fmt = 'd'
    
    if kwargs.get('annot') and kwargs.get('normalize') and not kwargs.get('max_value'):
        heatmap_df = heatmap_df/heatmap_df.sum().sum()
        max_value = None
        fmt = '.2f'
    
    labels = bool(kwargs.get('show_labels'))
    if labels:
        labels = 'auto'
    
    plt.figure(figsize=(figsize*1.6, figsize))
    sns.heatmap(heatmap_df, cmap='Blues', vmin=0, vmax=max_value, annot=kwargs.get('annot'), fmt=fmt,
                xticklabels=labels, yticklabels=labels)
    plt.show()