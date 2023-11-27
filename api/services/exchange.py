from datetime import datetime
import time

from api.entities import Transaction
from api.repository import Repository
from api.services.events import FrontendChannels

from trading.exchanges.iqoption import IQOptionExchange
from trading.models import Action, Transaction as IQOptionTransaction



class ExchangeAdapter(IQOptionExchange):
    def __init__(self, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(email='', password='')
        self.frontend   = frontend
        self.repository = repository

    def get_current_price(self, asset: str) -> float:
        last_candle = super().get_candles(asset, timeframe=5, candles_amount=1, timestamp=time.time())[-1]
        return last_candle.close
    
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
        
        asset_data = self.repository.get_asset_by_name(transaction.asset)
        self.repository.create_log(f'Transação iniciada: direction={action.name}, expiration={expiration}min, timeframe=M5, value={amount}')        
        self.frontend.update_transactions(self.repository.transactions)
        self.frontend.update_asset_logs(asset_data)
        return transaction
    

    def wait(self, transaction: IQOptionTransaction) -> IQOptionTransaction:
        transaction = super().wait(transaction)

        asset = self.repository.get_asset_by_name(transaction.asset)
        self.repository.update_asset_profit(asset, profit=transaction.profit)
        self.repository.update_transaction_profit(transaction.id, transaction.profit)
        self.repository.create_log(f'Transação finalizada: profit={transaction.profit} status={transaction.status}')
        
        self.frontend.update_transactions(self.repository.transactions)
        self.frontend.update_asset_profit(asset)
        self.frontend.update_balance(self.balance())
        self.frontend.update_asset_logs(asset)
        return transaction
