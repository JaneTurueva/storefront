from aiohttp.web_urldispatcher import View
from asyncpgsa import PG


class BaseView(View):
    URL_PATH: str

    @property
    def postgres(self) -> PG:
        return self.request.app['postgres']

    @property
    def redis(self):
        return self.request.app['redis']
