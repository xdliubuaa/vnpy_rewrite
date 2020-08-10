from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# from vnpy.gateway.ctp import CtpGateway
# from vnpy.gateway.huobi import HuobiGateway
# from vnpy.gateway.okex import OkexGateway
from vnpy.gateway.binance import BinanceGateway

from vnpy.app.csv_loader import CsvLoaderApp
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.cta_backtester import CtaBacktesterApp

def main():
    """Start VN Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    # main_engine.add_gateway(CtpGateway)
    #main_engine.add_gateway(HuobiGateway)
    #main_engine.add_gateway(OkexGateway)
    main_engine.add_gateway(BinanceGateway)

    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(CsvLoaderApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()

if __name__ == "__main__":
    main()
