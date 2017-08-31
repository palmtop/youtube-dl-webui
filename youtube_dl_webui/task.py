#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import sha1

from .config import ydl_conf
from .utils import TaskInexistenceError
from .utils import TaskRunningError
from .utils import TaskExistenceError
from .utils import TaskPausedError

def url2tid(url):
    return sha1(url.encode()).hexdigest()

class Task(object):

    def __init__(self, tid, db, ydl_opts={}, info={}, status={}):
        self.tid = tid
        self._db = db
        self.ydl_conf = ydl_conf(ydl_opts)
        self.info = info
        self.status = status

    def start(self):
        pass

    def pause(self):
        pass

    def halt(self):
        pass

    def finish(self):
        pass


class TaskManager(object):
    """
    Tasks are categorized into two types, active type and inactive type.

    Tasks in active type are which in downloading, pausing state. These tasks
    associate with a Task instance in memory. However, inactive type tasks
    are in invalid state or finished state, which only have database recoards
    but memory instance.
    """

    def __init__(self, db):
        self._db = db

        # all the active type tasks can be referenced from self._tasks_dict or
        # self._tasks_set.
        self._tasks_dict = {}
        self._tasks_set = set(())

    def new_task(self, url, ydl_opts={}):
        """Create a new task and put it in inactive type"""

        return self._db.new_task(url, ydl_opts)

    def start_task(self, tid, ignore_state=False, first_run=False):
        """make an inactive type task into active type"""

        if tid in self._tasks_set:
            task = self._tasks_dict[tid]
            task.start()
            return task

        try:
            ydl_opts = self._db.get_ydl_opts(tid)
            info     = self._db.get_info(tid)
            status   = self._db.get_stat(tid)
        except TaskInexistenceError as e:
            raise TaskInexistenceError(e.msg)

        task = Task(tid, self._db, ydl_opts=ydl_opts, info=info, status=status)
        self._tasks_set.add(task)
        self._tasks_dict[tid] = task

        task.start()

        return task

    def pause_task(self, tid):
        task = self._tasks_dict[tid]
        task.pause()

    def halt_task(self, tid):
        task = self._tasks_dict[tid]
        task.stop()

    def finish_task(self, tid):
        task = self._tasks_dict[tid]
        task.finish()






