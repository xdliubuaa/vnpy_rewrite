from datetime import timedelta
from typing import List

import tushare as ts
from datetime import  datetime

from .setting import SETTINGS
from .constant import Exchange, Interval
from .object import BarData, HistoryRequest


INTERVAL_VT2TS = {
    Interval.MINUTE: "1m",
    Interval.HOUR: "60m",
    Interval.DAILY: "1d",
}

INTERVAL_ADJUSTMENT_MAP = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta()         # no need to adjust for daily bar
}


class tushareQurey:
    """
    querying history data from tushare pro.
    """

    def __init__(self):
        """"""
        self.ts_token = SETTINGS["tusharepro.token"]

        self.inited = False
        self.symbols = set()

    def init(self):
        """"""
        if self.inited:
            return True

        if not self.ts_token:
            return False

        ts.set_token(self.ts_token)

        self.inited = True
        return True

    def exchange_bond(self, exchange:Exchange):
        if exchange.value == "SSE":
            return "SH"
        elif exchange.value == "SZSE":
            return  "SZ"
        else :
            return  exchange.value
        
    def tuquery(self, req:HistoryRequest):
        symbol = req.symbol
        exchange = req.exchange
        interval = req.interval

        #start = req.start
        #end = req.end

        start = req.start.strftime('%Y%m%d')
        end = req.end.strftime('%Y%m%d')
        
        tcode = f'{symbol}'+'.'+ self.exchange_bond(exchange)

        #print(tcode, start, end)
        #print("TuSharePro parameter {} [{}, {}] ...".format(tcode, start, end))
        #self.write_log(f"tuquery code:{tcode}-symbol:{symbol}, exchange: {exchange}")
        # For adjust timestamp from bar close point (RQData) to open point (VN Trader)
        #adjustment = INTERVAL_ADJUSTMENT_MAP[interval]

        # For querying night trading period data
        #end += timedelta(1)

        try:
            pro = ts.pro_api()
            df = pro.daily(ts_code= tcode, start_date= start, end_date= end)
        except Exception as ex:
                print("{} TuSharePro异常[{}, {}]: {}, ...".format(tcode, start, end, ex))

        data: List[BarData] = []

        if df is not None:
            for index, row in df.iterrows():
                date = datetime.strptime(row.trade_date,'%Y%m%d')
                
                bar = BarData(
                    symbol=tcode,
                    exchange=exchange,
                    interval=interval,
                    datetime=date,
                    open_price=row["open"],
                    high_price=row["high"],
                    low_price=row["low"],
                    close_price=row["close"],
                    volume=row["amount"],
                    gateway_name="TU"
                )
                data.append(bar)
        else:
            print("{} TuSharePro异常 df is none [{}, {}], ...".format(tcode, start, end))
        return data

tushareData = tushareQurey()