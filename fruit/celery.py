import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit.settings')
app = Celery('fruit')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# get_joke_periodic_task = PeriodicTask.objects.update_or_create(
#         name='Get joke',
#         defaults={
#             'name': 'Get joke',
#             'interval': IntervalSchedule.objects.get_or_create(
#                 every=10.0,
#                 period=IntervalSchedule.SECONDS)[0],
#             'task': 'fruit_admin.tasks.get_random_joke'
#         }
#     )


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
