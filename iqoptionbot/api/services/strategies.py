from datetime import datetime

from trading.logger import TradingLogger
from trading.bot import TradingStrategy
from trading.exceptions import StopTradingBot
from trading.helpers import price_reached_target
from trading.models import Action, Candle, Color

from iqoptionbot.api.entities import Asset, PriceAlert
from iqoptionbot.api.repository import Repository
from iqoptionbot.api.events import FrontendChannels

logger = TradingLogger.instance()

def calculate_expiration(candle: Candle) -> int:
    expiration = candle.get_remaining_time_until_close()
    if(datetime.utcnow().second > 30):
        expiration -= 1
    return expiration


class RetracementM5Strategy(TradingStrategy):
    def __init__(self, asset: Asset, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(candles_amount=1)
        
        self.asset = asset
        self.frontend = frontend
        self.repository = repository
        self.repository.set_asset_running(asset)
        self.frontend.update_start_button(asset)
        logger.info('Monitorando preços')

    def get_trade_direction(self, candle: Candle) -> Action:
        expiration = calculate_expiration(candle)
        self.repository.setup.expiration = expiration

        if(expiration < 2):
            logger.info('Transação cancelada devido ao tempo de expiração menor que 2min')
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
        if(not self.asset.is_open):
            raise StopTradingBot('Ativo fechado recarregue a página para atualizar')
        if(not self.asset.running):
            raise StopTradingBot('Execução interrompida')
        if(not self.asset.alerts):
            self.asset.running = False
            logger.info('A lista de alertas está vazia')
            raise StopTradingBot('Execução interrompida')

        last_candle = candles[-1]
        self.asset.price = last_candle.close
        self.frontend.update_asset_price(self.asset)
        return self.check_alerts(last_candle)