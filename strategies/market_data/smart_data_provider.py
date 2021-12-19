from datetime import datetime, timedelta, date

from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
import tushare as ts
from pytz import timezone
import pandas as pd
import numpy as np
import peewee
import logging

from utils.system_configs import tushare_config
from market_data.base_data_provider import AbstractDataProvider
from market_data.tushare_data_provider import TuShareDataProvider
from market_data.akshare_data_provider import AkShareDataProvider
from market_data import data_definition
from market_data.models import FutureHoldingData

CHINA_TZ = timezone("Asia/Shanghai")
UTC_TZ = timezone("UTC")

logger = logging.getLogger(__name__)

class SmartDataProvider(AbstractDataProvider):
    def __init__(self, database_manager=None):        
        super().__init__(database_manager)
        
        self.akshare_provider = AkShareDataProvider(database_manager)
        self.tushare_provider = TuShareDataProvider(database_manager)
        
    def download_data(self, data_requirement):
        if type(data_requirement) == data_definition.FutureHoldingData:
            return self.akshare_provider.download_data(data_requirement)
        if type(data_requirement) == data_definition.FutureTickData:
            return self.tushare_provider.download_data(data_requirement)
        if type(data_requirement) == data_definition.IndexData:
            return self.tushare_provider.download_data(data_requirement)
        if type(data_requirement) == data_definition.StockDailyData:
            return self.tushare_provider.download_data(data_requirement)
        if type(data_requirement) == data_definition.FundNavData:
            return self.tushare_provider.download_fund_nav_data(data_requirement)
        logger.error(f"Unknown data: {data_requirement}")
        
    def get_fx_quote_for_cny(self, currency):
        return self.akshare_provider.get_fx_quote_for_cny(currency)
        
    def get_future_info_for_symbol(self, symbol):
        return self.akshare_provider.get_future_info_for_symbol(symbol)
    
    def update_future_info(self):
        return self.akshare_provider.update_future_info()