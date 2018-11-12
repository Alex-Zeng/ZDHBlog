from locust import HttpLocust, TaskSet, task
import json
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        res = self.client.post("/?s=api/login/index", {"userName":"15220094541", "password":"qwe123"})
        # token = json.dumps(res.raw).data.token
        dato=(json.loads(res.content.decode()))
        token=dato.get('data').get('token')
        self.client.cookies['_token']=token


    @task(2)
    def index(self):
        self.client.get("/?s=api/goods/getFavoriteType")

    @task(1)
    def profile(self):
        self.client.get("/?s=api/mall_cart/getNumber")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000

