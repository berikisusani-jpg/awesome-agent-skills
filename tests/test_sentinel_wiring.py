import pytest
from core.ledger import ActionLedger

def test_sentinel_blocks_destructive_action():
    ledger = ActionLedger()
    # "delete" is a blocked keyword in EthicalSentinel
    action_id = ledger.queue_action("file_manager", "delete_all_files", {"path": "/"})

    assert action_id is None
    assert len(ledger.pending_actions) == 0

def test_sentinel_allows_normal_action():
    ledger = ActionLedger()
    action_id = ledger.queue_action("file_manager", "list_files", {"path": "."})

    assert action_id is not None
    assert action_id in ledger.pending_actions
