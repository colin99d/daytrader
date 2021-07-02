from sklearn.model_selection import train_test_split
from sklearn import linear_model
import scipy.stats as scpy
import pandas as pd
import numpy as np

def z_score_analyzer(data, symbols):
    opens = []
    closes = []
    decisions = []
    
    for symbol in symbols:
        x=0
        y=-2
        z=-1
        #features = ['Open','pHigh','pLow','pClose','pVolume']
        #symbolz = [x for symbol in features]
        #X = data[features, symbolz][i+1:i+64]
        X = data['Open', symbol][x:y].to_numpy().reshape(-1,1)
        y = data['Close',symbol][x:y]
            
        #Split data into train and test
        train_X, val_X, train_y, val_y = train_test_split(X, y)
        
        #Create model and predictions
        model = linear_model.LinearRegression()
        model.fit(train_X, train_y)
        preds_val = model.predict(val_X)
            
        #Compute stock 95% confidence interval
        l1 = preds_val - val_y
        mean = np.average(l1)
        stdev = np.std(l1)
        predict = data['Open',symbol][z].reshape(1,-1)
        pred_increase = model.predict(predict)- data['Open',symbol][z]

        #Compute long/short with confidence 
        zscore = 3
        while True:
            lowf = mean - zscore*stdev + pred_increase
            highf = mean + zscore*stdev + pred_increase
                
            if lowf > 0 and highf > 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2)
                break
                
            elif lowf < 0 and highf < 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2) *-1
                break 
                
            else:
                zscore -= .001

        #Add data to lists
        opens.append(data['Open',symbol][z])
        closes.append(data['Close',symbol][z])
        decisions.append(decision)
        
    #Turn lists into a Dataframe 
    df = pd.DataFrame({'ticker': symbols,'date': data.index[z],'open': opens,'decision': decisions,'close':closes})
    df_sorted = df.sort_values(by=['decision']).reset_index()
    long = df_sorted['ticker'][len(df_sorted)-1]
    #longs = [df_sorted['date'][len(df_sorted)-1],df_sorted['ticker'][len(df_sorted)-1],df_sorted['open'][len(df_sorted)-1],df_sorted['decision'][len(df_sorted)-1],df_sorted['close'][len(df_sorted)-1]]
    pricel = df_sorted['open'][len(df_sorted)-1]
    decisionl = df_sorted['decision'][len(df_sorted)-1]
    return long, pricel, decisionl, data.index[z]