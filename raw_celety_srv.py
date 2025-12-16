from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", backend="redis://localhost", broker="redis://localhost:6379/0")


@app.task(bind=True)
def add(self, x, y):
    print(f"Adding {x} + {y}, request id: {self.request.id}")
    return x + y


app.conf.beat_schedule = {
    "add-every-monday-morning": {
        "task": "tasks.add",
        "schedule": crontab(minute="*/1"),
        "args": (1, 1),
    },
}
