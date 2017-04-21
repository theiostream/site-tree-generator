import os
from os import path
from sys import argv
from sys import stderr
import re
from random import randint

def build_csv(base_dir, snapshot):
    csv_lines = []
    passed = []

    for root, dirs, files in os.walk(base_dir):
        file_size = 0
        try:
            file_size = path.getsize(path.join(root, snapshot + '.snapshot'))
        except FileNotFoundError:
            success = False
            for idx, f in enumerate(files):
                if idx > 0 and int(f.split('.')[0]) > int(snapshot):
                    fallback = files[idx - 1]
                    file_size = path.getsize(path.join(root, fallback))

                    success = True
                    break
            if not success:
                stderr.write('Could not find any crawl for ' + root + '\n')
                continue

        root = path.relpath(root, base_dir)
        #print('=== DEBUG: ' + root)
        path_components = root.split('/')
        path_components[:] = [re.sub(r'[^a-zA-Z0-9 _]', '', p) for p in path_components]
        csv_path = '-'.join(path_components)

        if len(dirs) > 0:
            csv_path += '-end'

        csv_lines.append(csv_path + ',' + str(file_size))

    return csv_lines

base_dir = argv[1]
snapshot = argv[2]

print('\n'.join(build_csv(base_dir, snapshot)))
