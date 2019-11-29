import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from irekua_dev_tools.repositories import REPOSITORY_INFO
from .install import install_dependency


class UpdateAppHandler(FileSystemEventHandler):
    def __init__(self, target, name, app, venvs_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.name = name
        self.venvs_dir = venvs_dir
        self.app = app

    def on_any_event(self, event):
        install_dependency(
            self.target,
            self.name,
            self.app,
            venvs_dir=self.venvs_dir,
            stderr=False,
            stdout=False)


def observe_app(target, name, app, venvs_dir=None):
    app_path = os.path.join(
        target,
        app,
        app.replace('-', '_'))
    event_handler = UpdateAppHandler(
        target=target,
        name=name,
        app=app,
        venvs_dir=venvs_dir)
    observer = Observer()
    observer.schedule(event_handler, app_path, recursive=True)
    observer.start()
    return observer


def observe_app_dependencies(target, name, venvs_dir=None):
    dependencies = REPOSITORY_INFO[name]['dependencies']
    return [
        observe_app(target, name, dependency, venvs_dir=venvs_dir)
        for dependency in dependencies]
