from celery import Celery, Task
from flask import current_app as app

def celery_init_app():
    class FlaskTask(Task):
        def __call__(self, *args:object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app= Celery()
    return celery_app

celery = celery_init_app()


# from celery import Celery
# from flask import Flask

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         broker=app.config['CELERY_BROKER_URL'],
#         backend=app.config['CELERY_RESULT_BACKEND']
#     )
#     celery.conf.update(app.config)
#     return celery
