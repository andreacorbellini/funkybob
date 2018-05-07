from datetime import datetime

import requests


DOCKER_NAMEGEN_URL = 'https://raw.githubusercontent.com/moby/moby/master/pkg/namesgenerator/names-generator.go'


def fetch_docker_name_generator():
    response = requests.get(DOCKER_NAMEGEN_URL)
    response.raise_for_status()
    return response.text


def parse_docker_name_generator(content):
    lines = iter(content.split('\n'))

    def iter_strings():
        for line in lines:
            if line == '\t}':
                break
            if line.startswith('\t\t"'):
                yield line.strip('\t ",')

    names = []
    adjectives = []

    for line in lines:
        if line == '\tleft = [...]string{':
            adjectives += iter_strings()
        if line == '\tright = [...]string{':
            names += iter_strings()

    return names, adjectives


def write_file(names, adjectives):
    def iter_strings(lst):
        return ('    {!r},\n'.format(s) for s in lst)

    with open('funkybob/data.py', 'w') as fp:
        fp.write('# List of names and adjectives from\n')
        fp.write('# {}\n'.format(DOCKER_NAMEGEN_URL))
        fp.write('# Retrieved {:%c}\n'.format(datetime.utcnow()))
        fp.write('\n')
        fp.write('NAMES = [\n')
        fp.writelines(iter_strings(names))
        fp.write(']\n')
        fp.write('\n')
        fp.write('ADJECTIVES = [\n')
        fp.writelines(iter_strings(adjectives))
        fp.write(']\n')


def main():
    content = fetch_docker_name_generator()
    names, adjectives = parse_docker_name_generator(content)
    write_file(names, adjectives)


if __name__ == '__main__':
    main()
