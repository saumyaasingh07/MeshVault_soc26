"""
Unit tests for Interactive Terminal UI Dashboard (Issue #10).
"""

import pytest
from cli.dashboard import PeerDashboard


def test_dashboard_initialization():
    dash = PeerDashboard(mode="recover", threshold_k=3, shares_n=5)
    assert dash.mode == "recover"
    assert dash.threshold_k == 3
    assert dash.shares_n == 5
    assert dash.completed_shares == 0
    assert len(dash.peers) == 0


def test_dashboard_update_peer():
    dash = PeerDashboard(mode="split", threshold_k=2, shares_n=3)
    dash.update_peer("192.168.1.10", "Discovered", "Pending", alias="alice")

    assert "192.168.1.10" in dash.peers
    peer = dash.peers["192.168.1.10"]
    assert peer["alias"] == "alice"
    assert peer["status"] == "Discovered"
    assert peer["ecdh_status"] == "Pending"

    # Update handshake state
    dash.update_peer("192.168.1.10", "Handshake", "Keys Exchanged", shares_count=1)
    peer_updated = dash.peers["192.168.1.10"]
    assert peer_updated["status"] == "Handshake"
    assert peer_updated["ecdh_status"] == "Keys Exchanged"
    assert peer_updated["shares_count"] == 1


def test_dashboard_update_progress():
    dash = PeerDashboard(mode="recover", threshold_k=3, shares_n=5)
    dash.update_progress(3)
    assert dash.completed_shares == 3


def test_dashboard_add_log():
    dash = PeerDashboard()
    dash.add_log("Peer connected")
    assert len(dash.logs) == 1
    assert "Peer connected" in dash.logs[0]


def test_dashboard_generate_layout_and_table():
    dash = PeerDashboard(mode="recover", threshold_k=3, shares_n=5)
    dash.update_peer(
        "192.168.1.50", "Completed", "Derived", shares_count=1, alias="bob"
    )
    dash.update_progress(1)

    table = dash.generate_peer_table()
    assert table is not None

    layout = dash.generate_layout()
    assert layout is not None


def test_dashboard_context_manager():
    with PeerDashboard(mode="split", threshold_k=2, shares_n=4) as dash:
        dash.update_peer("10.0.0.1", "Connecting", "Initiated")
        dash.update_progress(1)
        assert "10.0.0.1" in dash.peers
