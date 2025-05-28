import os
from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]


def load_config() -> BotConfig:
    token = os.getenv('TOKEN', '')
    admins = os.getenv('ADMIN_IDS', '')
    admin_ids = [int(a) for a in admins.split(',') if a]
    return BotConfig(token=token, admin_ids=admin_ids)
