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

        from voice.speaker import FridaySpeaker
        from voice.listener import FridayListener
        from voice.transcriber import FridayTranscriber

        speaker = FridaySpeaker()
        listener = FridayListener()
        transcriber = FridayTranscriber()

        action = self.pending_actions[action_id]
        prompt = f"Sir, I have a pending {action['action']} action for {action['component']}. Should I proceed?"
        speaker.speak(prompt)

        print(f"Friday: Action {action_id} awaiting manual approval (Profile: {self.profile})...")
        start_time = datetime.datetime.now()

        retry_count = 0
        while (datetime.datetime.now() - start_time).total_seconds() < timeout:
            # Check if approved externally (API)
            if self.pending_actions[action_id]["status"] == "approved":
                self._log_audit(self.pending_actions[action_id], approved_by="human")
                return True
            if self.pending_actions[action_id]["status"] == "rejected":
                return False

            # Real Voice Approval implementation
            audio_path = await listener.listen()
            if audio_path:
                 text = transcriber.transcribe(audio_path).lower()
                 print(f"Friday: Transcribed approval intent: '{text}'")

                 if any(word in text for word in ["yes", "approve", "proceed", "go ahead", "do it"]):
                      speaker.speak("Understood, Sir. Proceeding.")
                      self.approve_action(action_id)
                      self._log_audit(self.pending_actions[action_id], approved_by="voice")
                      return True
                 elif any(word in text for word in ["no", "stop", "reject", "cancel"]):
                      speaker.speak("Action rejected.")
                      self.reject_action(action_id)
                      return False
                 else:
                      if retry_count == 0:
                           speaker.speak("I'm sorry Sir, I didn't catch that. Should I proceed?")
                           retry_count += 1
                      else:
                           speaker.speak("Still unclear. Action rejected.")
                           self.reject_action(action_id)
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
