import os

from typing import (
    Dict,
    Optional,
    OrderedDict,
    Any
)
from manager import APIManager

class Client(APIManager):
    def __init__(self, **options):
        super(Client. self).__init__()
        self.name = options.get("name")

        self.token = os.environ.get("access_token")
        self.base_group_id = os.environ.get("group_id")
        self.bot_id = os.environ.get("bot_id")

        self.state: OrderedDict[Any, Any] = OrderedDict()

    def get_state(self, key):
        result = self.state.get(key, None)
        return result

    def set_state(self, key, value):
        try:
            self.state[key] = value
        except Exception as e:
            print(e)
            return False
        else:
            return True