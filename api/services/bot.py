from threading import Thread
from typing import Any, Callable

from api.repository import Repository
from api.services.events import FrontendChannels
from api.services.decorators.exchange import ExchangeAdapter
from api.services.logger import FrontendLogger
from api.services.strategies import RetracementM5Strategy

from trading.bot import TradingBot, TradingStrategy
from trading.logger import TradingLogger

logger = TradingLogger.instance()

class BotHandler:
    def __init__(self, frontend: FrontendChannels, repository: Repository) -> None:
        logger.addHandler(FrontendLogger(frontend, repository))
        self.frontend = frontend
        self.repository = repository
        self.exchange = ExchangeAdapter(frontend, repository)
        self.thread = Thread()

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

    def start_new_thread(self, strategy: TradingStrategy):
        bot = TradingBot(self.exchange, self.repository.setup, strategy)
        bot.time_interval = 0.05
        self.thread = Thread(target=bot.run, args=[])
        self.thread.start()

    def finish_thread(self):
        self.repository.stop_all_assets()
        self.thread.join()

    def start(self, asset_name: str):
        if(self.thread.is_alive()):
            self.finish_thread()

        asset    = self.repository.get_asset_by_name(asset_name)
        strategy = RetracementM5Strategy(asset, self.frontend, self.repository)
        self.start_new_thread(strategy)

    def stop(self):
        if(self.thread.is_alive()):
            self.finish_thread()
     
