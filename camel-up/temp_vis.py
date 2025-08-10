from rich.console import Console

console = Console()

console.print("\n[bold]Numbers 1-16 with Colored Circles[/bold]\n")

positions = []
circles = []

for i in range(1, 17):
    if i < 10:
        positions.append(f" {i} ")
    else:
        positions.append(f"{i} ")
    
    if i == 3:
        circles.append(" 🔴")
    elif i == 8:
        circles.append(" 🔵")
    elif i == 13:
        circles.append(" 🟢")
    else:
        circles.append("   ")

circles_line = "".join(circles).rstrip()
numbers_line = "".join(positions).rstrip()

console.print(f"[white]{circles_line}[/white]")
console.print(f"[white]{numbers_line}[/white]")
console.print()