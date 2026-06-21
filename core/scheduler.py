import asyncio
import datetime
import logging
import uuid
from typing import Dict, Any, Callable, List

class FridayScheduler:
    def __init__(self):
        self.tasks = {}
        self.running = False
        self.logger = logging.getLogger("FridayScheduler")

    async def add_task(self, name: str, coroutine_func: Callable, interval_seconds: int = None, run_at: datetime.datetime = None, params: Dict = None):
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "func": coroutine_func,
            "interval": interval_seconds,
            "run_at": run_at,
            "params": params or {},
            "last_run": None,
            "status": "scheduled"
        }
        self.logger.info(f"Scheduled task '{name}' (ID: {task_id})")
        return task_id

    async def start(self):
        if self.running: return
        self.running = True
        asyncio.create_task(self._loop())

    async def stop(self):
        self.running = False

    async def _loop(self):
        while self.running:
            now = datetime.datetime.now()
            for tid, task in list(self.tasks.items()):
                should_run = False

                if task["run_at"] and now >= task["run_at"]:
                    should_run = True
                    task["run_at"] = None # Run once at specific time
                elif task["interval"]:
                    if not task["last_run"] or (now - task["last_run"]).total_seconds() >= task["interval"]:
                        should_run = True

                if should_run:
                    task["status"] = "running"
                    try:
                        self.logger.info(f"Executing scheduled task: {task['name']}")
                        await task["func"](**task["params"])
                        task["last_run"] = datetime.datetime.now()
                        task["status"] = "scheduled" if task["interval"] else "completed"
                        if task["status"] == "completed":
                            del self.tasks[tid]
                    except Exception as e:
                        self.logger.error(f"Error in scheduled task '{task['name']}': {e}")
                        task["status"] = "failed"

            await asyncio.sleep(10) # Check every 10 seconds

    def get_tasks(self):
        return list(self.tasks.values())

    def remove_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

_scheduler = FridayScheduler()
def get_scheduler():
    return _scheduler
