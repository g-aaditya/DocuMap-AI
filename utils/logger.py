from rich.console import Console
console = Console()
def info(msg): console.print(f"[INFO] {msg}")
def warn(msg): console.print(f"[WARN] {msg}")
def error(msg): console.print(f"[ERROR] {msg}")
