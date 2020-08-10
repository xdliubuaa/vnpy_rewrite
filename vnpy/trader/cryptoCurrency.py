from datetime import timedelta
from typing import List
import csv
import os
import pandas as pd
import re
import time
import numpy as np
from datetime import  datetime

from .setting import SETTINGS
from .constant import Exchange, Interval
from .object import BarData, HistoryRequest, TickData


INTERVAL_VT2RQ = {
    Interval.MINUTE: "1m",
    Interval.HOUR: "60m",
    Interval.DAILY: "1d",
}

INTERVAL_ADJUSTMENT_MAP = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta()         # no need to adjust for daily bar
}


class cryptoCurrency:
    """
    get history data from file.
    """

    def __init__(self):
        """"""
        self.path = SETTINGS["currency.path"]

        self.inited = False
        self.symbols = set()

    def init(self):
        """"""
        if self.inited:
            return True

        if not self.path:
            print("get currency data异常, path:{}, ...".format(self.path))
            return False

        self.inited = True
        return True

    def convert_exchange(self, exch):
        if exch == "ba":
            return "BINANCE"
        elif exch == "hb":
            return  "HUOBI"
        elif exch == "ok":
            return  "OKEX"
        else:
            return "OTHER"
        
    def get_history(self, req:HistoryRequest):
        symbol = req.symbol
        exch = req.exchange
        interval = req.interval

        #start = req.start
        #end = req.end

        #print("get_history, req:{}, ...".format(req))
        start = req.start.strftime('%Y%m%d')
        end = req.end.strftime('%Y%m%d')
        
        data: List[TickData] = []

        for root,dirs,files in os.walk(self.path):
            for file in files:
                file_long = os.path.join(root,file)
                #print("get_history, file_long:{}, ...".format(file_long))

                df = pd.read_csv(file_long, sep=',', header=None)

                for i in df.index:
                    col = np.array(df.iloc[i])
                    if symbol != col[1]:
                        continue

                    timeArray = time.localtime(col[3]+24*3600)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    tick = TickData(
                        symbol=col[1],
                        exchange=exch,
                        datetime=otherStyleTime,
                        name=col[1],
                        open_interest=col[24],
                        volume=col[15].replace(']', ''),
                        last_price=col[14].replace('[', ''),  # 最新价
                        last_volume=col[15].replace(']', ''),

                        open_price=col[24],
                        high_price=col[26],
                        low_price=col[27],
                        pre_close=col[25],

                        ask_price_1=col[4].replace('[', ''), # 卖1价
                        ask_price_2=col[6].replace('[', ''),
                        ask_price_3=col[8].replace('[', ''),
                        ask_price_4=col[10].replace('[', ''),
                        ask_price_5=col[12].replace('[', ''),

                        bid_price_1=col[14].replace('[', ''), #买1价
                        bid_price_2=col[16].replace('[', ''),
                        bid_price_3=col[18].replace('[', ''),
                        bid_price_4=col[20].replace('[', ''),
                        bid_price_5=col[22].replace('[', ''),

                        ask_volume_1=col[5].replace(']', ''),
                        ask_volume_2=col[7].replace(']', ''),
                        ask_volume_3=col[9].replace(']', ''),
                        ask_volume_4=col[11].replace(']', ''),
                        ask_volume_5=col[13].replace(']', ''),

                        bid_volume_1=col[15].replace(']', ''),
                        bid_volume_2=col[17].replace(']', ''),
                        bid_volume_3=col[19].replace(']', ''),
                        bid_volume_4=col[21].replace(']', ''),
                        bid_volume_5=col[23].replace(']', ''),
                        gateway_name="CU"
                    )

                    data.append(tick)
                    if i == 1:
                        print(tick)

        return data

currencyData = cryptoCurrency()