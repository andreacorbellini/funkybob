from funkybob import UniqueRandomNameGenerator


def print_names(generator, count=8):
    for name in generator[:count]:
        print('  -', name)
    print('  ({} more...)'.format(len(generator) - count))
    print()


print('Random names:')
generator = UniqueRandomNameGenerator(members=1)
print_names(generator)


print('Random names preceeded by an adjective:')
generator = UniqueRandomNameGenerator()
print_names(generator)

print('Random names preceeded by two adjectives:')
generator = UniqueRandomNameGenerator(members=3)
print_names(generator)

print('Random names preceeded by three adjectives:')
generator = UniqueRandomNameGenerator(members=4)
print_names(generator)
