from dataclasses import dataclass, field
from datetime import datetime
from typing import Any



@dataclass
class PriceAlert:
    id: int
    price: float
    counter: int = field(default=0, init=False, repr=False)

    def __init__(self, price: float):
        self.id = PriceAlert.counter
        self.price = price
        PriceAlert.counter += 1
    
    @property
    def to_dict(self) -> dict[str, Any]:
        return {'id': self.id, 'price': self.price}


@dataclass
class LogMessage:
    id: int
    date: datetime
    message: str
    counter: int = field(default=0, init=False, repr=False)

    def __init__(self, date: datetime, message: str):
        self.id = LogMessage.counter
        self.date = date
        self.message = message
        LogMessage.counter += 1
    
    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id, 
            'date': self.date.strftime('%d/%m/%Y %H:%M:%S'),
            'message': self.message
        }


@dataclass()
class Asset:
    name: str
    profit: float = 0.0
    price: float = 0.0
    running: bool = False
    is_open: bool = True
    alerts: list[PriceAlert] = field(default_factory=list)
    logs: list[LogMessage] = field(default_factory=list)

    def get_currencies_image_urls(self) -> list[str]:
        image_path = '/static/icons'
        asset = self.name.replace('-OTC', '')
        currency1 = asset[0:3]
        currency2 = asset[3:]
        return [
            f'{image_path}/{currency1}.SVG', 
            f'{image_path}/{currency2}.SVG'
        ]

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name, 
            'profit': self.profit,
            'running': self.running,
            'is_open': self.is_open,
            'price': self.price,
            'alerts': [alert.to_dict for alert in self.alerts],
            'logs': [log.to_dict for log in self.logs]
        }

    def __eq__(self, other: object) -> bool:
        if(not isinstance(other, Asset)): return False
        return other.name == self.name

@dataclass
class Transaction:
    id: int
    asset: str
    hour: datetime
    value: float
    profit: float
    direction: str
    is_completed: bool

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'asset': self.asset,
            'hour': self.hour.strftime('%H:%M'), 
            'value': self.value,
            'profit': self.profit,
            'direction': self.direction,
            'is_completed': self.is_completed
        }