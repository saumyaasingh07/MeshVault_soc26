"""
MeshVault CLI Entrypoint with Typer framework, auto-completion, and advanced UX.
"""

import sys
import traceback
from typing import Optional
import typer

from cli.config import load_config

app = typer.Typer(
    name="meshvault",
    help="MeshVault: Encrypted P2P Secret Sharing over LAN — No Server, No Cloud, No Trust Required.",
    add_completion=True,
)


class CLIState:
    debug: bool = False


state = CLIState()


def complete_interface(incomplete: str):
    """Dynamically complete network interface names."""
    interfaces = ["eth0", "wlan0", "lo", "en0", "adapter"]
    return [i for i in interfaces if i.startswith(incomplete)]


def complete_alias(incomplete: str):
    """Dynamically complete peer aliases from config file."""
    try:
        cfg = load_config()
        aliases = list(cfg.get("peers", {}).values()) + list(
            cfg.get("peers", {}).keys()
        )
        return [a for a in aliases if a.startswith(incomplete)]
    except Exception:
        return []


def handle_error(e: Exception):
    """Clean error handling helper respecting --debug flag."""
    if state.debug:
        traceback.print_exc()
        raise e
    else:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        typer.echo("Run with --debug to see full stack traceback.", err=True)
        raise typer.Exit(code=1)


@app.callback()
def main_callback(
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable verbose debug logging and full tracebacks.",
    ),
):
    state.debug = debug


@app.command()
def split(
    threshold: int = typer.Option(
        ...,
        "-k",
        "--threshold",
        help="Threshold number of shares required to reconstruct (K)",
    ),
    shares: int = typer.Option(
        ...,
        "-n",
        "--shares",
        help="Total number of shares to distribute (N)",
    ),
    secret: Optional[str] = typer.Option(
        None,
        "-s",
        "--secret",
        help="Secret text (if omitted, will prompt)",
    ),
    interface: Optional[str] = typer.Option(
        None,
        "-i",
        "--interface",
        autocompletion=complete_interface,
        help="Network interface to use (e.g. eth0, wlan0)",
    ),
):
    """Split a secret and distribute shares to LAN peers."""
    try:
        typer.echo("MeshVault Command Line Interface")
        typer.echo("Command selected: split")
        typer.echo(f"Threshold (K): {threshold}, Shares (N): {shares}")
        if interface:
            typer.echo(f"Interface: {interface}")
        typer.echo("Implementation is currently in progress.")
    except Exception as e:
        handle_error(e)


@app.command()
def recover(
    threshold: int = typer.Option(
        ...,
        "-k",
        "--threshold",
        help="Threshold number of shares required to reconstruct (K)",
    ),
    port: int = typer.Option(
        5000,
        "-p",
        "--port",
        help="Listening port for share collection",
    ),
    interface: Optional[str] = typer.Option(
        None,
        "-i",
        "--interface",
        autocompletion=complete_interface,
        help="Network interface to listen on",
    ),
):
    """Collect shares from LAN peers and recover the secret."""
    try:
        typer.echo("MeshVault Command Line Interface")
        typer.echo("Command selected: recover")
        typer.echo(f"Threshold (K): {threshold}, Port: {port}")
        if interface:
            typer.echo(f"Interface: {interface}")
        typer.echo("Implementation is currently in progress.")
    except Exception as e:
        handle_error(e)


@app.command()
def completion(
    shell: str = typer.Argument(
        ...,
        help="Target shell for completion script (bash, zsh, fish, powershell)",
    ),
):
    """Output auto-completion configuration script for specified shell."""
    shell_lower = shell.lower()
    if shell_lower == "bash":
        typer.echo(
            "# MeshVault Bash Completion\n"
            "_meshvault_completion() {\n"
            '    local cur="${COMP_WORDS[COMP_CWORD]}"\n'
            '    local prev="${COMP_WORDS[COMP_CWORD-1]}"\n'
            '    case "$prev" in\n'
            "        -i|--interface)\n"
            '            COMPREPLY=( $(compgen -W "eth0 wlan0 lo en0" -- "$cur") )\n'
            "            return 0\n"
            "            ;;\n"
            "    esac\n"
            '    COMPREPLY=( $(compgen -W "split recover --threshold --shares --secret --interface --debug --help" -- "$cur") )\n'
            "}\n"
            "complete -F _meshvault_completion meshvault"
        )
    elif shell_lower == "zsh":
        typer.echo(
            "#compdef meshvault\n"
            "# MeshVault Zsh Completion\n"
            "_meshvault() {\n"
            "    local -a commands\n"
            "    commands=(\n"
            '        "split:Split a secret and distribute shares to LAN peers"\n'
            '        "recover:Collect shares from LAN peers and recover the secret"\n'
            '        "completion:Output auto-completion configuration script"\n'
            "    )\n"
            '    _describe -t commands "meshvault command" commands\n'
            "}\n"
            '_meshvault "$@"'
        )
    elif shell_lower == "fish":
        typer.echo(
            "# MeshVault Fish Completion\n"
            "complete -c meshvault -f\n"
            'complete -c meshvault -n "__fish_use_subcommand" -a "split recover completion"'
        )
    elif shell_lower == "powershell":
        typer.echo(
            "# MeshVault PowerShell Completion\n"
            "Register-ArgumentCompleter -Native -CommandName meshvault -ScriptBlock {\n"
            "    param($wordToComplete, $commandAst, $cursorPosition)\n"
            '    $subcommands = @("split", "recover", "completion")\n'
            '    $subcommands | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, "ParameterValue", $_) }\n'
            "}"
        )
    else:
        typer.secho(
            f"Error: Unsupported shell '{shell}'. Supported: bash, zsh, fish, powershell",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)


def main():
    try:
        app()
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    main()
