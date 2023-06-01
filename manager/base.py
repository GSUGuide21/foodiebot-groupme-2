import requests
from util import EventEmitter, urljoin

class Manager(EventEmitter):
    def __init__(self, **options):
        super(Manager, self).__init__()
        self.emit("create", **options)

        base_url = options.get("base_url", "")
        if base_url == "":
            raise Exception("All managers must have a base URL.")
        
        self.base_url = base_url
        self.path = options.get("path", "")

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        return setattr(self, key, value)
    
    def get(self, **params):
        path = params.get("path", self.path)
        url = urljoin(self.base_url, path)
        del params.path
        return requests.get(url, **params)

    def get_json(self, **params):
        return self.get(**params).json()
    
    def post(self, **params):
        path = params.get("path", self.path)
        url = urljoin(self.base_url, path)
        del params.path
        return requests.post(url, **params)