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
        file_name = ''
        file_size = 0
        try:
            file_name = path.join(root, snapshot + '.snapshot')
            file_size = path.getsize(file_name)
        except FileNotFoundError:
            if len(files) == 0:
                stderr.write('Could not find any crawl for ' + root + '\n')
                continue

            failure = False
            broke_early = False
            for idx, f in enumerate(sorted(files)):
                file_is_more_recent = int(f.split('.')[0]) > int(snapshot)
                #stderr.write('debug: Comparing ' + f + ' with ' + snapshot + '\n')
                if idx == 0 and file_is_more_recent:
                    stderr.write('Could not find any crawl for ' + root + '\n')
                    failure = True
                    break
                elif file_is_more_recent:
                    file_name = files[idx - 1]
                    file_size = path.getsize(path.join(root, file_name))
                    broke_early = True
                    break

            if failure:
                continue

            if not broke_early:
                file_name = files[-1]
                file_size = path.getsize(path.join(root, file_name))

        root = path.relpath(root, base_dir)
        stderr.write('debug: getting file ' + file_name + '\n')

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
