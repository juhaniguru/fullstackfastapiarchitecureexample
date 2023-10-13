import requests


class TodosService:
    def __init__(self, db):
        self.url = 'https://jsonplaceholder.typicode.com/todos'

    def get_all(self):
        res = requests.get(self.url)
        return res.json()
