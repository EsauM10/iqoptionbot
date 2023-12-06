from threading import Thread
from typing import Any, Callable
from api.entities import Asset

from api.repository import Repository
from api.services.events import FrontendChannels
from api.services.decorators.exchange import ExchangeAdapter
from api.services.logging import FrontendLogHandler
from api.services.strategies import RetracementM5Strategy

from trading.bot import TradingBot
from trading.logger import TradingLogger


def on_bot_stopped(asset: Asset, frontend: FrontendChannels):
    asset.running = False
    frontend.update_start_button(asset)


class BotHandler:
    def __init__(self, frontend: FrontendChannels, repository: Repository) -> None:
        self.frontend   = frontend
        self.repository = repository
        self.exchange   = ExchangeAdapter(frontend, repository)
        self.thread     = Thread()

    def login_required(self, func: Callable[..., Any]) -> Any:
        def wrapper(*args: Any, **kwargs: Any):
            if(not self.is_connected):
                return self.frontend.redirect('login')
            return func(*args, **kwargs)
        return wrapper
    
    @property
    def is_connected(self) -> float:
        return self.exchange.api.check_connect()
    
    def connect(self, email: str, password: str):
        try:
            self.exchange.api.email = email
            self.exchange.api.password = password
            self.exchange.connect()
        except:
            raise Exception('Invalid credentials')        

    def make_trading_bot(self, asset: Asset) -> TradingBot:
        handler = FrontendLogHandler(asset, self.frontend, self.repository)
        TradingLogger.add_handler(handler, clear=True)
        strategy = RetracementM5Strategy(asset, self.frontend, self.repository)
        on_stop = lambda: on_bot_stopped(asset, self.frontend)
        return TradingBot(self.exchange, self.repository.setup, strategy, on_stop)

    def start_new_thread(self, asset: Asset):
        bot = self.make_trading_bot(asset)
        self.thread = Thread(target=bot.run, args=[])
        self.thread.start()

    def finish_thread(self):
        self.repository.stop_all_assets()
        self.thread.join()

    def start(self, asset_name: str):
        if(self.thread.is_alive()):
            self.finish_thread()

        asset = self.repository.get_asset_by_name(asset_name)
        self.start_new_thread(asset)

    def stop(self):
        if(self.thread.is_alive()):
            self.finish_thread()
     
