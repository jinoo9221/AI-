import time
import datetime
import requests
import pandas as pd
import os.path

timestamp = last_update_time = datetime.datetime.now()

while (1):
    #response = requests.get ('https://api.bithumb.com/public/orderbook/ETH_KRW/?count=5')
    #print (response.text)

    book = {}
    response = requests.get('https://api.bithumb.com/public/orderbook/ETH_KRW/?count=5')
    book = response.json()
    # print(response.status_code)
    
    timestamp = datetime.datetime.now()
    if ((timestamp - last_update_time).total_seconds() < 1.0):
        continue
    last_update_time = timestamp

    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    req_time = req_timestamp.split(' ')[0]


    # timestamp,price,type,quantity
    data = book['data']
    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric, errors='ignore')
    
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index()
    del bids['index']
    bids['type'] = 0

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric, errors='ignore')

    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1

    df = bids.append(asks)
    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp


    # print(df)
    fn = "2022-05-18-bithumb-ETH-orderbook.csv"
    should_write_header = os.path.exists(fn)
    if should_write_header == False:
        df.to_csv(fn, index=False, header=True, mode = 'a')
    else:
        df.to_csv(fn, index=False, header=False, mode = 'a')

    time.sleep(1)
