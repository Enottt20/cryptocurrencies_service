from locust import HttpUser, TaskSet, task, between

class MyUser(HttpUser):
    wait_time = between(5, 15)  # Время ожидания между запросами

    @task
    def empty(self):
        self.client.get(f"/hi/")

    @task
    def read_courses(self):
        self.client.get(f"/api/v1/courses/")
