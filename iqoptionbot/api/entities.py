from dataclasses import dataclass, field
from datetime import datetime
import time
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


@dataclass
class Schedule:
    start_timestamp: float
    end_timestamp: float
    date_format: str = '%d/%m/%Y %H:%M:%S'

    @property
    def is_open_now(self) -> bool:
        return self.start_timestamp <= time.time() <= self.end_timestamp 
       
    @property
    def start_hour(self) -> str:
        return datetime.fromtimestamp(self.start_timestamp).strftime(self.date_format)
    
    @property
    def end_hour(self) -> str:
        return datetime.fromtimestamp(self.end_timestamp).strftime(self.date_format)

    def __repr__(self) -> str:
        return f'Schedule({self.start_hour}, {self.end_hour})'

@dataclass()
class Asset:
    name: str
    profit: float = 0.0
    price: float = 0.0
    running: bool = False
    alerts: list[PriceAlert]  = field(default_factory=list)
    logs: list[LogMessage]    = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)

    def get_currencies_image_urls(self) -> list[str]:
        image_path = '/static/icons'
        asset = self.name.replace('-OTC', '')
        currency1 = asset[0:3]
        currency2 = asset[3:]
        return [
            f'{image_path}/{currency1}.SVG', 
            f'{image_path}/{currency2}.SVG'
        ]

    def update_schedules(self, timestamps: list[list[float]]):
        self.schedules = self.parse_schedules(timestamps)

    @staticmethod
    def parse_schedules(timestamps: list[list[float]]) -> list[Schedule]:
        return [Schedule(start_time, end_time) for start_time, end_time in timestamps]

    @staticmethod
    def make_asset(data: dict[str, Any]):
        return Asset(
            name=data['name'],
            schedules=Asset.parse_schedules(data['schedule'])
        )

    @property
    def is_open(self) -> bool:
        any_open_schedule = any([schedule.is_open_now for schedule in self.schedules])
        return any_open_schedule

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