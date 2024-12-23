from typing import Dict
import asyncio
from fastapi import BackgroundTasks
from config.LoggerConfig import logger

class TaskManagerService:

    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.loop = asyncio.get_event_loop()

    async def cancelCurrentTask(self, name: str):
        logger.info(f"Cancelling task: {name}")

        if name in self.tasks:
            task = self.tasks[name]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    def taskDoneCallback(self, name: str, task: asyncio.Task):
        if name in self.tasks:
            del self.tasks[name]
        logger.info(f"Removed task {name}")

    async def addTask(self, name: str, taskFunc, *args):
        logger.info(f"Adding task: {name}")
        if list(self.tasks):
            logger.info(f"Active tasks while creating {name} task: {', '.join(list(self.tasks))}")
        else:
            logger.info(f"No active tasks while creating {name} task")
        
        await self.cancelRunningTasks()

        task = self.loop.create_task(taskFunc(*args)) 
        self.tasks[name] = task
        task.add_done_callback(lambda task: self.taskDoneCallback(name, task))

    async def cancelRunningTasks(self):
        tasksToCancel = [task for task in self.tasks.values() if not task.done()]
        for task in tasksToCancel:
            activeTaskName = next(name for name, t in self.tasks.items() if t == task)
            await self.cancelCurrentTask(activeTaskName)

    def runBackgroundTask(self, backgroundTasks: BackgroundTasks, taskFunc, *args):
        backgroundTasks.add_task(taskFunc, *args)

taskManagerService = TaskManagerService()