class ApiClient:
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def request(self, method, endpoint, **kwargs):
        url = self.base_url + endpoint
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)