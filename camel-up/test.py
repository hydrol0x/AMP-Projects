from rich.table import Column, Table
from rich.console import Console
from rich import print
console = Console()

table = Table(title="Position of Camels", box=None)
track = [str(i) for i in range(1, 17)]

positions = []

for i in range(len(track)):
	positions.append('_')

for i in range(len(track)):
	print(track[i], positions[i])
