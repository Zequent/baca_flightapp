import logging
import os
import sys
import threading
import time, traceback
from logging import getLogger
import logging
from tools.py_files.widgets.zequenttoast import ZequentToast
import concurrent.futures
import multiprocessing, multiprocessing.process

PROJECT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))

log = getLogger(__name__)
log.setLevel(logging.DEBUG)


def execute_with_thread(name, method,  *args):
    thread = WorkerThread(name=name, method=method, args=(args))
    future = concurrent.futures.Future()
    future.set_running_or_notify_cancel()
    thread.set_future(future=future)
    #if callback_method is not None:
     #   thread.add_done_callback(callback=callback_method)
    thread.start()
    thread.join()
    return thread.result_future.result()

class Utils:
    @staticmethod
    def getSettingsFile():
        return os.path.abspath("tools/local/settings.json")
    @staticmethod
    def getTranslatorFolder():
        return ('tools/localization/')

    @staticmethod
    def abs_path(*path):
        return os.path.join(PROJECT_DIR, *path)

    @staticmethod
    def getNavigationDrawerItems(translator, sm):
        from kivymd.uix.navigationdrawer import MDNavigationDrawerItem, MDNavigationDrawerLabel, \
            MDNavigationDrawerDivider
        from functools import partial
        import json

        f = open(os.path.abspath('tools/local/navigationdrawer.json'))
        data = json.load(f)
        sm.transition.direction = 'down'

        navigationItems = []
        for key in data:
            match key:
                case 'main':
                    currentNavigationLabel = MDNavigationDrawerLabel()
                    currentNavigationLabel.text = translator.translate('coworker_translate')
                    navigationItems.append(currentNavigationLabel)
                    for currTranslateKey in data[key]:
                        currentNavigationItem = MDNavigationDrawerItem()
                        currentNavigationItem.icon = 'menu'
                        currentNavigationItem.text = translator.translate(currTranslateKey)
                        currentNavigationItem.bind(on_press=partial(sm.push_replacement, currTranslateKey))
                        navigationItems.append(currentNavigationItem)
                    navigationItems.append(MDNavigationDrawerDivider())

        return navigationItems

    @staticmethod
    def every(delay, task):
        next_time = time.time() + delay
        while True:
            time.sleep(max(0, next_time - time.time()))
            try:
                task()
            except Exception:
                traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
            # skip tasks if we are behind schedule:
            next_time += (time.time() - next_time) // delay * delay + delay

    @staticmethod
    def get_drone_icon(droneType):
        if droneType.lower() == 'vtol':
            return "./static/icons/drone/vtol.png"
        elif droneType.lower() == 'copter':
            return "./static/icons/drone/copter.png"

    @staticmethod
    def get_drone_icon_appbar(droneType):
        if droneType.lower() == 'vtol':
            return "./static/icons/drone/vtol_white.png"
        elif droneType.lower() == 'copter':
            return "./static/icons/drone/copter_white.png"
        


class MultiProcessor(multiprocessing.Process):

    def __init__(self, name, method, args):
        multiprocessing.Process.__init__(self)
        self.name = name
        self.method = method
        self.args = args

class WorkerThread(threading.Thread):
    def __init__(self, name, method, args):
        threading.Thread.__init__(self)
        self.name = name
        self.method = method
        self.response = None
        self.args = args
        self.result_future = None
        self.done_callbacks = []
        self.setDaemon(True)


    def set_future(self, future):
        self.result_future = future

    #def add_done_callback(self, callback):
     #   self.done_callbacks.append(callback)

    def run(self):
        try:
            if self.args is not ():
                result = self.method(self.args)
            else:
                result = self.method()
            if self.result_future:
                self.result_future.set_result(result)
        except Exception as e:
            if self.result_future:
                self.result_future.set_exception(e)
        finally:
            print("Thread finished")
         #   for callback in self.done_callbacks:
          #      callback(self.result_future)
