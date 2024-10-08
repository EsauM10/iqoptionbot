import logging

from iqoptionbot.api.entities import Asset
from iqoptionbot.api.repository import Repository
from iqoptionbot.api.events import FrontendChannels

class FrontendLogHandler(logging.Handler):
    def __init__(self, asset: Asset, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(level=logging.INFO)
        self.asset      = asset
        self.frontend   = frontend
        self.repository = repository
    
    def emit(self, record: logging.LogRecord) -> None:
        self.repository.create_log(self.asset, record.getMessage())
        self.frontend.update_asset_logs(self.asset)