import asyncio
import uuid
import datetime
import logging
from core.sentinel import EthicalSentinel

class ActionLedger:
    def __init__(self):
        self.pending_actions = {}
        self.sentinel = EthicalSentinel()

    def queue_action(self, component, action, params):
        # Pre-queue screening
        evaluation = self.sentinel.evaluate_action(f"{component}:{action}")
        if not evaluation.get("aligned", True):
            logging.warning(f"Action blocked by Sentinel. Component: {component}, Action: {action}, Reason: {evaluation.get('reason')}")
            return None

        action_id = str(uuid.uuid4())
        self.pending_actions[action_id] = {
            "id": action_id,
            "component": component,
            "action": action,
            "params": params,
            "status": "pending",
            "timestamp": datetime.datetime.now().isoformat()
        }
        return action_id

    async def wait_for_approval(self, action_id, timeout=300):
        if action_id is None:
            return False

        logging.info(f"Action {action_id} queued for approval. System on standby...")
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).total_seconds() < timeout:
            if self.pending_actions[action_id]["status"] == "approved":
                return True
            if self.pending_actions[action_id]["status"] == "rejected":
                return False
            await asyncio.sleep(1)
        return False

    def approve_action(self, action_id):
        if action_id in self.pending_actions:
            self.pending_actions[action_id]["status"] = "approved"
            return True
        return False

    def reject_action(self, action_id):
        if action_id in self.pending_actions:
            self.pending_actions[action_id]["status"] = "rejected"
            return True
        return False

_ledger = ActionLedger()
def get_ledger():
    return _ledger
