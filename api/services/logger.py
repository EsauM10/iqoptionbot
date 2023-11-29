import logging

from api.repository import Repository
from api.services.events import FrontendChannels

class FrontendLogger(logging.Handler):
    def __init__(self, frontend: FrontendChannels, repository: Repository) -> None:
        super().__init__(level=logging.INFO)
        self.frontend = frontend
        self.repository = repository
    
    def emit(self, record: logging.LogRecord) -> None:
        name  = self.repository.selected_asset
        asset = self.repository.get_asset_by_name(name)
        self.repository.create_log(record.getMessage())
        self.frontend.update_asset_data(asset)