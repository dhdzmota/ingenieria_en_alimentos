import subprocess

command_list = [
    'python src/data/read_human_processed_information.py',
    'python src/data/food_information_to_dataset.py',
]

for command in command_list:
    subprocess.run(command.split(' '))


