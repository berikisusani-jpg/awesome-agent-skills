class TaskAgent:
    def break_down_task(self, task):
        return [f"Step 1 for {task}", f"Step 2 for {task}", "Final review"]

    def execute_task(self, task):
        steps = self.break_down_task(task)
        for step in steps:
            print(f"Executing: {step}")
        return f"Task '{task}' completed successfully."
