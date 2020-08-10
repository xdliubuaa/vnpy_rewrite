
from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
from vnpy.trader.database import database_manager
from vnpy.trader.constant import Exchange, Interval

class tickTobar(CtaTemplate):
    author = "liuxd"

    window_size = 15
    interval_type = "MINUTE"

    interval = Interval.MINUTE

    parameters = ["window_size", "interval_type"]

    number = 0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        if self.interval_type == "MINUTE":
            self.interval = Interval.MINUTE
        elif self.interval_type == "HOUR":
            self.interval = Interval.HOUR
        elif self.interval_type == "DAY":
            self.interval = Interval.DAILY
        
        self.bg = BarGenerator(self.on_bar, self.window_size, self.on_transfer_bar, self.interval)
        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_tick(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

        self.put_event()

    def on_save_bar(self, bar: BarData):
        #self.number = self.number + 1
        #print("135 on_save_bar: {}, {}, {}".format(self.number, self.interval, bar))
        bar.interval = self.interval
        if self.interval == Interval.MINUTE:
            bar.interval = Interval.MINUTE
            if self.window_size == 15:
                bar.interval = Interval.MINUTE15
        elif self.interval == Interval.HOUR:
            bar.interval = Interval.HOUR
            if self.window_size == 4:
                bar.interval = Interval.HOUR4
            elif self.window_size == 6:
                bar.interval = Interval.HOUR6
        elif self.interval == Interval.DAILY:
            bar.interval = Interval.DAILY

        database_manager.save_bar_data([bar])

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

    def on_transfer_bar(self, bar: BarData):
        """"""

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.on_save_bar(bar)

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
