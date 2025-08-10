import os
import subprocess
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
file_lists = []
for file in os.listdir(current_dir):
	entry = file.split('_')
	entry = entry[0]
	if entry == 'tests':
		print(f'running {file}')
		subprocess.run([sys.executable, file])