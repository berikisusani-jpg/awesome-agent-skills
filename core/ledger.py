import asyncio
import uuid
import datetime
import logging
from config.settings import AUTONOMY_PROFILE
from core.sentinel import EthicalSentinel

class ActionLedger:
    def __init__(self):
        self.pending_actions = {}
        self.audit_log = "action_ledger_audit.log"
        self.profile = AUTONOMY_PROFILE
        self.sentinel = EthicalSentinel()

    def _log_audit(self, action_data, approved_by="human"):
        audit_logger = logging.getLogger("FridayAudit")
        audit_logger.info({
            "event": "ACTION_AUDIT",
            "approved_by": approved_by,
            "component": action_data['component'],
            "action": action_data['action'],
            "params": action_data['params'],
            "risk_level": action_data['risk_level'],
            "timestamp": datetime.datetime.now().isoformat()
        })

    def queue_action(self, component, action, params, risk_level="high"):
        action_id = str(uuid.uuid4())

        # Real wiring of EthicalSentinel
        alignment = self.sentinel.evaluate_action(action)
        if not alignment["aligned"]:
            risk_level = "critical" # Force review for non-aligned actions
            logging.warning(f"Sentinel flagged action {action}: {alignment['reason']}")

        action_data = {
            "id": action_id,
            "component": component,
            "action": action,
            "params": params,
            "risk_level": risk_level,
            "status": "pending",
            "timestamp": datetime.datetime.now().isoformat(),
            "sentinel_reason": alignment.get("reason", "N/A")
        }

        # FIXED: Power Levels & Auto-approval
        if self._should_auto_approve(component, risk_level):
            action_data["status"] = "approved"
            self._log_audit(action_data, approved_by="auto")
            self.pending_actions[action_id] = action_data
            return action_id

        self.pending_actions[action_id] = action_data
        return action_id

    def _should_auto_approve(self, component, risk_level):
        # STANDING CONSTITUTION: Physical-world and financial actions never auto-approve.
        if component in ["Printer", "Printer3D", "Finance", "Commerce"]:
            return False

        if self.profile == "GUEST": return False

        if self.profile == "STANDARD":
            if risk_level == "low": return True

        if self.profile == "POWER":
            if component in ["PCControl", "BrowserControl"] and risk_level != "critical":
                return True
            if risk_level == "low": return True

        return False

    async def wait_for_approval(self, action_id, timeout=300):
        if self.pending_actions[action_id]["status"] == "approved":
            return True

        # Voice-native action approval trigger
        from voice.speaker import FridaySpeaker
        from voice.listener import FridayListener
        speaker = FridaySpeaker()
        listener = FridayListener()

        action = self.pending_actions[action_id]
        msg = f"Sir, I have a pending {action['action']} action for {action['component']}. Should I proceed?"
        speaker.speak(msg)

        print(f"Friday: Action {action_id} awaiting manual approval (Profile: {self.profile})...")
        start_time = datetime.datetime.now()

        # Non-blocking voice check could be here, but we'll use a task for it
        # For simplicity in this build, we check transcription in the loop

        while (datetime.datetime.now() - start_time).total_seconds() < timeout:
            if self.pending_actions[action_id]["status"] == "approved":
                self._log_audit(self.pending_actions[action_id], approved_by="human")
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
