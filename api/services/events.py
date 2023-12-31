from typing import Literal
from flask_socketio import SocketIO

from api.entities import Asset, PriceAlert, Transaction

NotificationType = Literal['info', 'warning', 'error']

class FrontendChannels:
    def __init__(self, socket: SocketIO) -> None:
        self.socket = socket
    
    def add_alert(self, alert: PriceAlert):
        self.socket.emit('addAlertItem', alert.to_dict)

    def delete_alert(self, alert_id: int):
        self.socket.emit('deleteAlertItem', alert_id)

    def push_notification(self, notification_type: NotificationType, message: str):
        self.socket.emit('pushNotification', {'message': message, 'type': notification_type})

    def update_account_balance(self, balance: float):
        self.socket.emit('setAccountBalance', balance)

    def update_asset_data(self, asset: Asset):
        self.update_asset_name(asset)
        self.update_asset_currencies(asset)
        self.update_asset_profit(asset)
        self.update_start_button(asset)
        self.update_asset_price(asset)
        self.update_asset_price_input(asset)
        self.update_asset_logs(asset)

    def update_asset_name(self, asset: Asset):
        self.socket.emit('setAssetName', {'name': asset.name})

    def update_asset_alerts(self, asset: Asset):
        data = asset.to_dict
        self.socket.emit('setAlerts', {'name': data['name'], 'alerts': data['alerts']})

    def update_asset_currencies(self, asset: Asset):
        currency1, currency2 = asset.get_currencies_image_urls()
        self.socket.emit('setCurrencies', {
            'name': asset.name, 
            'currency1': currency1,
            'currency2': currency2,
        })

    def update_asset_logs(self, asset: Asset):
        data = asset.to_dict
        self.socket.emit('setLogs', {'name': data['name'], 'logs': data['logs']})

    def update_asset_price(self, asset: Asset):
        self.socket.emit('setPrice', {'name': asset.name, 'price': asset.price})

    def update_asset_price_input(self, asset: Asset):
        self.socket.emit('setPriceAlertInput', {'name': asset.name, 'price': asset.price})

    def update_asset_profit(self, asset: Asset):
        self.socket.emit('setProfit', {'name': asset.name, 'profit': asset.profit})
    
    def update_balance(self, balance: float):
        self.socket.emit('setAccountBalance', balance)

    def update_open_assets(self, selected_asset: str, open_assets: list[str]):
        self.socket.emit('setOpenAssets', {
            'selectedAsset': selected_asset, 
            'openAssets': open_assets
        })

    def update_transactions(self, transactions: list[Transaction]):
        data = [item.to_dict for item in transactions]
        self.socket.emit('setTransactions', data)
    
    def update_start_button(self, asset: Asset):
        self.socket.emit('updateStartButton', {
            'name': asset.name, 
            'running': asset.running,
            'is_open': asset.is_open
        })

    def redirect(self, pathname: str):
        self.socket.emit('redirect', pathname)
