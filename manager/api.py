from .base import Manager

class APIManager(Manager):
    def __init__(self, **options):
        super(APIManager, self).__init__(base_url="https://api.groupme.com/",
                                         **options)