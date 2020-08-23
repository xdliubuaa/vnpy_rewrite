# By Traders, For Traders.


<p align="center">
    <img src ="https://img.shields.io/badge/version-2.0.9-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7-blue.svg" />
    <img src ="https://img.shields.io/circleci/build/github/vnpy/vnpy?token=4d11df68295c8cc02a2bede46094991364190bbc"/>
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

vn.py是一套基于Python的开源量化交易系统开发框架，于2015年1月正式发布，在开源社区5年持续不断的贡献下一步步成长为全功能量化交易平台，目前国内外金融机构用户已经超过300家，包括：私募基金、证券自营和资管、期货资管和子公司、高校研究机构、自营交易公司、交易所、Token Fund等。


## 环境准备

* 支持的系统版本：Windows 7以上/Windows Server 2008以上/Ubuntu 18.04 LTS
* 支持的Python版本：Python 3.7 64位（**注意必须是Python 3.7 64位版本**）

## 安装步骤

在[这里](https://github.com/vnpy/vnpy/releases)有最新版本，解压后运行以下命令安装：

这里是基于vnpy-2.0.9版本进行修改的，先安装python版本，可以通过
  - 安装[Anaconda](https://www.anaconda.com/download/)，python3.6及以上版本 64位版本(32位应该也可以，但没测试过)
    建议安装[老版本的Anaconda](https://repo.anaconda.com/archive/)
  - 安装[MongoDB](https://www.mongodb.com/download-center#production)，并将[MongoDB配置为系统服务](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#configure-a-windows-service-for-mongodb-community-edition)
    -  如果你想下载更多的历史数据，建议配备比较大的的硬盘。
    -  [MogonDB客户端](https://robomongo.org/download)
    - **注意: 在Windows下安装MongoDB时，会默认安装MongoDB Compass。 MongoDB Compass安装很慢，不需要安装**
    - talib
        - Windows
            - 请到[这儿](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)安装对应的whl版本

**Windows**

    install.bat

**Ubuntu**

    bash install.sh

## 脚本运行

在源码根目录下已经创建了run.py，类似以下示例代码：

```Python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy.gateway.ctp import CtpGateway
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.cta_backtester import CtaBacktesterApp

def main():
    """Start VN Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()

if __name__ == "__main__":
    main()
```

在该目录下打开CMD（按住Shift->点击鼠标右键->在此处打开命令窗口/PowerShell）后运行下列命令启动VN Trader：

    python run.py

## 使用指南
1. 找到C:\Users\${USER_NAME}\.vntrader\vt_setting.json文件，配置好mongodb和dataSource.type
   也可以在启动了VN Trader界面上的全局配置上配置好配置项
2. 在VN Trader界面上找到回测界面，点击进入，找到tickToBar的策略，主要使用以下两种功能
  - **下载数据**：从tick文件中读取tick数据，然后存入到mongodb数据库中
  - **开始回测**: 将tick数据转换成分钟，小时，天的bar数据

3. 转换好bar数据后，回测策略就可以直接使用bar数据；也可以直接通过tick数据进行策略回测；这两者都需要配置对应的配置项。

## 功能特点

1. 全功能量化交易平台（vnpy.trader），整合了多种交易接口，并针对具体策略算法和功能开发提供了简洁易用的API，用于快速构建交易员所需的量化交易应用。

2. 覆盖国内外所有交易品种的交易接口（vnpy.gateway）：

    * 国内市场

        * CTP（ctp）：国内期货、期权

        * CTP Mini（mini）：国内期货、期权

        * CTP证券（sopt）：ETF期权

        * 飞马（femas）：国内期货

        * 宽睿（oes）：国内证券（A股）

        * 中泰XTP（xtp）：国内证券（A股）

        * 华鑫奇点（tora）：国内证券（A股）

        * 鑫管家（xgj）：期货资管

        * 融航（rohon）：期货资管

    * 海外市场

        * 富途证券（futu）：港股、美股

        * 老虎证券（tiger）：全球证券、期货、期权、外汇等

        * Interactive Brokers（ib）：全球证券、期货、期权、外汇等

        * 易盛9.0外盘（tap）：全球期货

        * 直达期货（da）：全球期货

        * OANDA（oanda）：外汇、CFD

    * 数字货币

        * BitMEX（bitmex）：数字货币期货、期权、永续合约

        * Bybit（bybit）：数字货币永续合约

        * OKEX永续（okexs）：数字货币永续合约

        * OKEX合约（okexf）：数字货币期货

        * 火币合约（hbdm）：数字货币期货

        * Gate.io永续（gateios）：数字货币永续合约

        * Deribit（deribit），数字货币期权、永续合约

        * 币安（binance）：数字货币现货

        * OKEX（okex）：数字货币现货

        * 火币（huobi）：数字货币现货

        * Bitfinex（bitfinex）：数字货币现货

        * Coinbase（coinbase）：数字货币现货

        * Bitstamp（bitstamp）：数字货币现货

        * 1Token（onetoken）：数字货币券商（现货、期货）

    * 特殊应用

        * RPC服务（rpc）：跨进程通讯接口，用于分布式架构

3. 开箱即用的各类量化策略交易应用（vnpy.app）：

    * cta_strategy：CTA策略引擎模块，在保持易用性的同时，允许用户针对CTA类策略运行过程中委托的报撤行为进行细粒度控制（降低交易滑点、实现高频策略）

    * cta_backtester：CTA策略回测模块，无需使用Jupyter Notebook，直接使用图形界面直接进行策略回测分析、参数优化等相关工作

    * spread_trading：价差交易模块，支持自定义价差，实时计算价差行情和持仓，支持半自动价差算法交易以及全自动价差策略交易两种模式

    * option_master：期权交易模块，针对国内期权市场设计，支持多种期权定价模型、隐含波动率曲面计算、希腊值风险跟踪等功能

    * algo_trading：算法交易模块，提供多种常用的智能交易算法：TWAP、Sniper、Iceberg、BestLimit等等，支持常用算法配置保存

    * script_trader：脚本策略模块，针对多标的组合类交易策略设计，同时也可以直接在命令行中实现REPL指令形式的交易，不支持回测功能

    * portfolio_manager：投资组合模块，面向各类基本面交易策略，以独立的策略子账户为基础，提供交易仓位的自动跟踪以及盈亏实时统计功能

    * rpc_service：RPC服务模块，允许将某一VN Trader进程启动为服务端，作为统一的行情和交易路由通道，允许多客户端同时连接，实现多进程分布式系统

    * csv_loader：CSV历史数据加载器，用于加载CSV格式文件中的历史数据到平台数据库中，用于策略的回测研究以及实盘初始化等功能，支持自定义数据表头格式

    * data_recorder：行情记录模块，基于图形界面进行配置，根据需求实时录制Tick或者K线行情到数据库中，用于策略回测或者实盘初始化

    * risk_manager：风险管理模块，提供包括交易流控、下单数量、活动委托、撤单总数等规则的统计和限制，有效实现前端风控功能

4. Python交易API接口封装（vnpy.api），提供上述交易接口的底层对接实现。

5. 简洁易用的事件驱动引擎（vnpy.event），作为事件驱动型交易程序的核心。

6. 跨进程通讯标准组件（vnpy.rpc），用于实现分布式部署的复杂交易系统。

7. Python高性能K线图表（vnpy.chart），支持大数据量图表显示以及实时数据更新功能。


## 版权说明

MIT
