from datetime import datetime
from threading import Lock
import time

from api.entities import Transaction
from api.repository import Repository
from api.services.events import FrontendChannels

from trading.exchanges.iqoption import IQOptionExchange
from trading.models import Action, Candle, Transaction as IQOptionTransaction



class ExchangeAdapter(IQOptionExchange):
    def __init__(self, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(email='', password='')
        self.frontend   = frontend
        self.repository = repository
        self.lock = Lock()
    
    def get_current_price(self, asset: str) -> float:
        last_candle = self.get_candles(asset, timeframe=5, candles_amount=1, timestamp=time.time())[-1]
        return last_candle.close
    
    def get_candles(self, asset: str, timeframe: int, candles_amount: int, timestamp: float) -> list[Candle]:
        with self.lock:
            return super().get_candles(asset, timeframe, candles_amount, timestamp)

    def buy(self, asset: str, expiration: int, amount: float, action: Action) -> IQOptionTransaction:
        transaction = super().buy(asset, expiration, amount, action)
        
        self.repository.create_transaction(Transaction(
            id=transaction.id,
            asset=transaction.asset,
            hour=datetime.now(),
            value=amount,
            profit=transaction.profit,
            direction='CALL' if(action == Action.BUY) else 'PUT',
            is_completed=transaction.is_completed
        ))
        self.frontend.update_balance(self.balance())
        self.frontend.update_transactions(self.repository.transactions)
        return transaction
    

    def wait(self, transaction: IQOptionTransaction) -> IQOptionTransaction:
        transaction = super().wait(transaction)

        asset = self.repository.get_asset_by_name(transaction.asset)
        self.repository.update_asset_profit(asset, profit=transaction.profit)
        self.repository.update_transaction_profit(transaction.id, transaction.profit)        
        self.frontend.update_transactions(self.repository.transactions)
        self.frontend.update_asset_profit(asset)
        self.frontend.update_balance(self.balance())
        return transaction

    def get_account_mode(self) -> str:
        return self.api.get_balance_mode() # type: ignore