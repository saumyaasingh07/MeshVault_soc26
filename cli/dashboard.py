"""
Interactive Terminal UI Dashboard for Peer Tracking and Share Collection.
Issue #10 Deliverable using rich.live, rich.table, rich.progress, and rich.layout.
"""

from typing import Dict, Optional, List
import time
from rich.console import RenderableType
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.style import Style


class PeerDashboard:
    """
    Live-updating terminal dashboard for monitoring MeshVault LAN peer discovery,
    ECDH handshake progress, share transfers, and overall recovery/split progress.
    """

    def __init__(
        self,
        mode: str = "split",
        threshold_k: int = 3,
        shares_n: int = 5,
        refresh_per_second: int = 10,
    ):
        self.mode = mode.lower()
        self.threshold_k = threshold_k
        self.shares_n = shares_n
        self.refresh_per_second = refresh_per_second

        # Peer tracking data store
        self.peers: Dict[str, Dict] = {}
        self.completed_shares: int = 0
        self.logs: List[str] = []

        # Progress bar setup
        self.progress = Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(
                bar_width=30, complete_style="green", finished_style="bold green"
            ),
            TaskProgressColumn(),
            TextColumn("[yellow]({task.completed}/{task.total} shares)"),
        )
        task_label = (
            "Shares Collected" if self.mode == "recover" else "Shares Distributed"
        )
        self.task_id = self.progress.add_task(
            task_label, total=self.shares_n, completed=0
        )

        self._live: Optional[Live] = None

    def update_peer(
        self,
        address: str,
        status: str,
        ecdh_status: str = "Pending",
        shares_count: int = 0,
        alias: Optional[str] = None,
    ) -> None:
        """
        Add or update a peer's connection status, ECDH handshake state, and share count.
        """
        existing = self.peers.get(address, {})
        display_name = alias or existing.get("alias") or address

        self.peers[address] = {
            "address": address,
            "alias": display_name,
            "status": status,
            "ecdh_status": ecdh_status,
            "shares_count": shares_count,
            "last_updated": time.strftime("%H:%M:%S"),
        }
        self.add_log(f"Peer {display_name} -> {status} ({ecdh_status})")
        if self._live:
            self._live.update(self.generate_layout())

    def update_progress(self, completed_shares: int) -> None:
        """
        Update the overall progress bar for collected/distributed shares.
        """
        self.completed_shares = completed_shares
        self.progress.update(self.task_id, completed=completed_shares)
        if self._live:
            self._live.update(self.generate_layout())

    def add_log(self, message: str) -> None:
        """
        Append a message to the live activity log panel.
        """
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        if len(self.logs) > 6:
            self.logs.pop(0)

    def _status_style(self, status: str) -> Text:
        """Format peer status with visual badges and colors."""
        s = status.lower()
        if "completed" in s or "connected" in s or "done" in s:
            return Text(f"● {status}", style="bold green")
        elif "transferring" in s or "handshake" in s or "connecting" in s:
            return Text(f"⚡ {status}", style="bold yellow")
        elif "discovered" in s:
            return Text(f"🔍 {status}", style="bold cyan")
        elif "failed" in s or "error" in s:
            return Text(f"✖ {status}", style="bold red")
        return Text(status, style="white")

    def generate_peer_table(self) -> Table:
        """Generate the live peer tracking table."""
        table = Table(title="Discovered LAN Peers & Handshake State", expand=True)
        table.add_column("Peer / Alias", style="cyan", no_wrap=True)
        table.add_column("IP Address", style="dim")
        table.add_column("Status", justify="center")
        table.add_column("ECDH Handshake", justify="center", style="magenta")
        table.add_column("Shares", justify="right", style="green")
        table.add_column("Last Activity", justify="center", style="dim")

        if not self.peers:
            table.add_row(
                "Searching...",
                "-",
                Text("🔍 Scanning LAN...", style="italic dim"),
                "Pending",
                "0",
                time.strftime("%H:%M:%S"),
            )

        for addr, info in self.peers.items():
            table.add_row(
                info["alias"],
                addr,
                self._status_style(info["status"]),
                info["ecdh_status"],
                str(info["shares_count"]),
                info["last_updated"],
            )

        return table

    def generate_layout(self) -> Layout:
        """Construct the rich layout combining header, peer table, progress bar, and log panel."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=2),
            Layout(name="progress", size=3),
            Layout(name="footer", size=5),
        )

        header_text = Text.assemble(
            ("MeshVault P2P Dashboard ", "bold white on blue"),
            (f" [{self.mode.upper()} MODE] ", "bold yellow on black"),
            (
                f" (Threshold K={self.threshold_k}, Total N={self.shares_n})",
                "dim white",
            ),
        )
        layout["header"].update(Panel(header_text, style="blue"))

        layout["main"].update(Panel(self.generate_peer_table(), border_style="cyan"))

        layout["progress"].update(
            Panel(
                self.progress, title="Overall Operation Progress", border_style="green"
            )
        )

        log_text = "\n".join(self.logs) if self.logs else "Waiting for activity..."
        layout["footer"].update(
            Panel(
                Text(log_text, style="dim white"),
                title="Recent Activity Log",
                border_style="dim",
            )
        )

        return layout

    def __enter__(self):
        self._live = Live(
            self.generate_layout(),
            refresh_per_second=self.refresh_per_second,
            screen=False,
        )
        self._live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._live:
            self._live.stop()
            self._live = None
