import tensorflow as tf
from IPython.display import display
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import lasio
import os
import pandas as pd
pd.set_option('display.max_columns', None)


def fnlist(dir='.\data', show=1):
    filename_list = []
    for i in os.listdir(dir):
        if '.las' in i:
            filename_list.append(os.path.join(dir, i))
    if show == 1:
        display(filename_list)
    return filename_list


def lasdf(filename, depth, show=1):
    df = lasio.read(filename).df()[depth[0]:depth[1]]
    df[df < 0] = 0
    df = df.loc[:, (df != 0).any(axis=0)]
    if show == 1:
        display(df.shape)
        display(df.columns)
    return df


def crossplot(df, columns=None, color_col='SW', show=1):
    if columns == None:
        columns = df.columns.to_list()
    n = len(columns)
    fig = make_subplots(
        rows=n,
        cols=n,
        row_titles=columns,
        column_titles=columns
    )
    for i in range(n):
        for j in range(n):
            trace = go.Scattergl(
                name=columns[i]+'-'+columns[j],
                y=df[columns[i]],
                x=df[columns[j]],
                text=df[color_col],
                mode='markers',
                hovertemplate='%{x},%{y}<br>' +
                '%{text}',
                marker=dict(
                    size=4,
                    color=df[color_col]
                )
            )
            fig.append_trace(trace, i+1, j+1)
            if j+1 == 1:
                fig['layout']['yaxis'+str(i*n+1)].update(
                    {'title': columns[i]}
                )
            if i+1 == n:
                fig['layout']['xaxis'+str(i*n+j+1)].update(
                    {'title': columns[j]}
                )
    if show == 1:
        fig.show(auto_open=True)
    return fig


def logsplot(df, columns=None, space=0.05, show=1):
    if columns == None:
        columns = df.columns.to_list()

    leny = len(columns)
    curvelist = dict()
    layout = dict()
    nax = 0

    for i in columns:
        nax = nax+1
        curvelist[i] = go.Scattergl(
            x=df[i],
            y=df.index,
            xaxis='x' if nax == 1 else 'x'+str(nax),
            name=i
        )
        layout['xaxis' if nax == 1 else 'xaxis'+str(nax)] = {
            "domain": [(nax-1)/leny+space/leny, nax/leny-space/leny],
            'title': i
        }
        layout['yaxis' if nax == 1 else 'yaxis'+str(nax)] = {
            "anchor": 'x' if nax == 1 else 'x'+str(nax),
            'autorange': 'reversed',
            'showspikes': True
        }
    fig = go.Figure(
        data=[i for i in curvelist.values()],
        layout=layout
    )
    if show == 1:
        fig.show(auto_open=True)
    return fig


def tftrain(
    train_x, train_y,
    layers=None, batch=64, epochs=100, verbose=0,
    test_x=None, test_y=None,
    file=None
):

    ncol = train_x.shape[1]
    if layers == None:
        layers = str(ncol+2)*2+'r'

    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.Flatten(input_shape=(ncol,))
    )
    for i in layers:
        if i == 'r':
            model.add(
                tf.keras.layers.Dense(ncol+2, activation='relu')
            )
        else:
            model.add(
                tf.keras.layers.Dense(int(i))
            )
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(1))

    optimizer = tf.keras.optimizers.Adam(0.001)
    model.compile(optimizer=optimizer, loss="mse")
    model.summary()
    model.fit(
        x=train_x,
        y=train_y,
        batch_size=batch,
        epochs=epochs,
        shuffle=1,
        initial_epoch=0,
        verbose=verbose
    )
    if isinstance(test_x, type(None)) or isinstance(test_y, type(None)):
        pass
    else:
        score = model.evaluate(test_x, test_y, verbose=1)
        display('test score : ', score)
    if file != None:
        model.save(filepath=file)
    return model


fl = fnlist()
display(fl[3])

################# 单井算法 69-33 ########################
df_694k = lasdf(fl[3], [1830, 1960])
model_6933 = tftrain(
    train_x=)
################# 邻井算法 694k 6916h ########################
'''
df_694k = lasdf(fl[4], [1830, 1960])
cols_694k = ['SP', 'GR', 'AC', 'RT', 'RXO']
'''
'''plot

logsfig_694k = logsplot(df_694k, cols_694k)
crossfig_694k = crossplot(df_694k, cols_694k)
'''
'''

df_694k['Y'] = 0
df_694k['Y'][1929.3:1931.3] = 74
df_694k['Y'][1932.6:1938.9] = 74
df_694k['Y'][1841:1844.1] = 24

'''
'''全序列解释
model_694k = tftrain(
    train_x=train_df_694k[cols_694k],
    train_y=train_df_694k['Y'],
    layers='999r9r',
    batch=256,
    epochs=128,
    test_x=df_694k[cols_694k],
    test_y=df_694k['Y']
)
'''

'''特定层位解释
train_df_694k=df_694k[1910:1960]
model_694k = tftrain(
    train_x=train_df_694k[cols_694k],
    train_y=train_df_694k['Y'],
    layers='999r9r',
    batch=32,
    epochs=50,
    test_x=df_694k[cols_694k],
    test_y=df_694k['Y']
)


cols_chk=['SP', 'GR', 'AC', 'RT','Y','rs']
df_694k['rs']=model_694k.predict(df_694k[cols_694k])
chkfig_694k=logsplot(df_694k,cols_chk)



display(fl[2])
df_6916h = lasdf(fl[2], [1890, 2180])

cols_6916h = ['SP', 'GR', 'AC', 'RT', 'RXO']
df_6916h['rs']=model_694k.predict(df_6916h[cols_6916h])
cols_chk1=['SP', 'GR', 'AC', 'RT','rs']
chkfig_6916h=logsplot(df_6916h,cols_chk1)
'''

'''plot
logsfig_6916h = logsplot(df_6916h, cols_6916h)
'''
