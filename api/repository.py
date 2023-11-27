from datetime import datetime
from api.entities import Asset, LogMessage, PriceAlert, Transaction
from api.exceptions import NotFoundException

from trading.models import TradingSetup

class Repository:
    def __init__(self):
        self.selected_asset = ''
        self.assets: list[Asset] = []
        self.transactions: list[Transaction] = []
        self.setup = TradingSetup(
            asset='EURUSD',
            timeframe=5,
            money_amount=1.0,
            stoploss=2.0,
            stopgain=2.0,
        )

    def __get_asset(self, asset_name: str) -> Asset | None:
        for asset in self.assets:
            if(asset.name == asset_name):
                return asset
        return None
    
    def get_alert_by_id(self, id: int) -> PriceAlert:
        for asset in self.assets:
            for alert in asset.alerts:
                if(alert.id == id):
                    return alert
        raise NotFoundException(f'PriceAlert with id={id} not found.')
        
    def get_asset_by_name(self, asset_name: str) -> Asset:
        asset = self.__get_asset(asset_name)
        if(asset is None):
            raise NotFoundException(f'Asset [{asset_name}] not found.')
        return asset

    def create_alert(self, asset_name: str, price: float) -> PriceAlert:
        asset = self.get_asset_by_name(asset_name)
        alert = PriceAlert(price)
        asset.alerts.append(alert)
        return alert

    def create_assets(self, assets: list[str]):
        for asset_name in assets:
            if(self.__get_asset(asset_name) is not None):
                continue
            
            self.assets.append(Asset(name=asset_name))
            
    def create_log(self, message: str):
        asset = self.get_asset_by_name(self.selected_asset)
        log_message = LogMessage(datetime.now(), message)
        asset.logs.append(log_message)

    def create_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_alerts(self, asset_name: str) -> list[PriceAlert]:
        asset = self.get_asset_by_name(asset_name)
        return asset.alerts
        
    def get_logs(self, asset_name: str) -> list[LogMessage]:
        asset = self.get_asset_by_name(asset_name)
        return asset.logs

    def get_open_assets_names(self) -> list[str]:
        return [
            asset.name for asset in self.assets
            if(asset.is_open)
        ]

    def get_transactions(self) -> list[Transaction]:
        return self.transactions
    
    def delete_alert(self, alert_id: int):
        for asset in self.assets:
            for alert in asset.alerts:
                if(alert.id == alert_id):
                    asset.alerts.remove(alert)
                    return
        raise NotFoundException(f'PriceAlert with id={alert_id} not found.')
    
    def set_asset_running(self, asset: Asset):
        self.selected_asset = asset.name
        self.setup.asset = asset.name
        asset.running = True

    def stop_all_assets(self):
        for asset in self.assets:
            asset.running = False
    
    def update_asset_profit(self, asset: Asset, profit: float):
        asset.profit += profit
    
    def update_transaction_profit(self, transaction_id: int, profit: float):
        for transaction in self.transactions:
            if(transaction.id == transaction_id):
                transaction.profit = profit
                transaction.is_completed = True

    