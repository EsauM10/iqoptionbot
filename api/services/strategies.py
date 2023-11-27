from trading.bot import TradingStrategy
from trading.exceptions import StopTradingBot
from trading.helpers import price_reached_target
from trading.models import Action, Candle, Color

from api.entities import Asset, PriceAlert
from api.repository import Repository
from api.services.events import FrontendChannels

import threading

class RetracementM5Strategy(TradingStrategy):
    def __init__(self, asset: Asset, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(candles_amount=100)
        self.asset = asset
        self.frontend = frontend
        self.repository = repository
        self.repository.set_asset_running(asset)
        self.repository.create_log('Monitorando Preços')
        self.frontend.update_asset_data(asset)

    def get_trade_direction(self, candle: Candle) -> Action:
        expiration = candle.get_remaining_time_until_close()
        self.repository.setup.expiration = expiration

        if(expiration < 2):
            self.repository.create_log('Transação cancelada devido ao tempo de expiração menor que 2min')
            return Action.HOLD
        return Action.BUY if(candle.color == Color.RED) else Action.SELL


    def remove_alert(self, alert: PriceAlert):
        self.asset.alerts.remove(alert)
        self.frontend.update_asset_alerts(self.asset)


    def check_alerts(self, last_candle: Candle) -> Action:
        for alert in self.asset.alerts:
            if(not price_reached_target(last_candle.close, alert.price)):
                continue

            self.remove_alert(alert)
            return self.get_trade_direction(last_candle)
        else:
            return Action.HOLD

    def evaluate(self, candles: list[Candle]) -> Action:
        if(not self.asset.running):
            self.repository.create_log('Execução interrompida')
            self.frontend.update_asset_data(self.asset)
            raise StopTradingBot('Execução interrompida')
        if(not self.asset.alerts):
            self.asset.running = False
            self.repository.create_log('A lista de alertas está vazia')
            self.repository.create_log('Execução interrompida')
            self.frontend.update_asset_data(self.asset)
            raise StopTradingBot('Execução interrompida')

        print(f'[{self.asset.name}]: {threading.active_count()} threads running')
        last_candle = candles[-1]
        self.asset.price = last_candle.close
        self.frontend.update_asset_price(self.asset)
        return self.check_alerts(last_candle)