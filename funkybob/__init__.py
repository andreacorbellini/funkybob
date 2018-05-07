import collections
import functools
import itertools
import random

from . import data


__all__ = [
    'NameGenerator',
    'RandomNameGenerator',
    'SimpleNameGenerator',
    'UniqueRandomNameGenerator',
]


@functools.lru_cache(maxsize=None)
def _binom(n, k):
    if n < k:
        return 0
    if k == 0 or n == k:
        return 1
    return _binom(n - 1, k - 1) + _binom(n - 1, k)


class Combinations(collections.Sequence):

    def __init__(self, seq, r):
        self.seq = seq
        self.r = r
        self._len = _binom(len(seq), r)

    def __len__(self, binom=_binom):
        return self._len

    def __iter__(self):
        return itertools.combinations(self.seq, self.r)

    def __getitem__(
            self, index, binom=_binom,
            isinstance=isinstance, slice=slice, range=range, len=len):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]

        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError('index out of range')

        def find_seq_offset(n, k):
            nonlocal index

            total = binom(n, k)

            for m in range(k, n + 1):
                diff = total - binom(m, k)
                if index >= diff:
                    break

            index -= diff
            return n - m + 1

        seq = self.seq
        r = self.r

        i = -1
        s = len(seq)
        result = [None] * r

        for j in range(r):
            i += find_seq_offset(s - i - 1, r - j)
            result[j] = seq[i]

        return tuple(result)


class Product(collections.Sequence):

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def __len__(self):
        return len(self.seq1) * len(self.seq2)

    def __iter__(self):
        return itertools.product(self.seq1, self.seq2)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]

        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError('index out of range')

        i, j = divmod(index, len(self.seq2))
        return self.seq1[i], self.seq2[j]


class RandomPermutation(collections.Sequence):

    # List of primes used for our quadratic residue PRGN. It's important that
    # these primes satisfy (p % 4) == 3.
    # For performance reason, it's also important that primes are higher and
    # close to the sizes that we are planning to support.
    _PRIMES = (
        179,  # 1 members
        16091,  # 2 members
        740099,  # 3 members
        22449671,  # 4 members
        505114223,  # 5 members
        8991032159,  # 6 members
    )

    def __init__(self, size, seed=None):
        if size <= 0:
            raise ValueError('size must be a positive integer')
        self.size = size

        if seed is None:
            seed = random.randrange(size)
        self.seed = seed

        for p in self._PRIMES:
            if p > size:
                self._prime = p
                break
        else:
            raise OverflowError('size too big: {}'.format(size))

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]

        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError('index out of range')

        # https://en.wikipedia.org/wiki/Blum_Blum_Shub
        # https://math.stackexchange.com/questions/30800/when-is-the-group-of-quadratic-residues-cyclic?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        p = self._prime
        size = self.size

        def residue(i):
            # Compute the quadratic residue modulo p. Quadratic residues are
            # guaranteed to be unique values in range(p), but only up to
            # 2 * i < p: after that point, values start repeating. The p - j
            # trick gives the missing values.
            j = i * i % p
            return j if 2 * i < p else p - j

        # It's very important that our starting point remains in range(size),
        # otherwise we may be trapped in a cyclic subgroup that doesn't have
        # any suitable values.
        res = residue((self.seed + index) % self.size)

        # residue() returned a value in range(prime), but we are interested
        # in range(size). Keep running the residue() algorithm until we find
        # a suitable value.
        # We are guaranteed to find a suitable values because quadratic
        # residues for a cyclic subgroup, so (in the worst case) we might
        # end up with the starting point, which is in range(size).
        while res >= size:
            res = residue(res)

        return res


class NameGenerator(collections.Iterable):

    def __init__(self, members=2, separator='_', names=None, adjectives=None):
        if members < 1:
            raise ValueError('members must be an integer greater than 0')

        self.members = members
        self.separator = separator

        if names is None:
            names = data.NAMES
        if not names:
            raise ValueError('empty names')
        self.names = names

        if members > 1:
            if adjectives is None:
                adjectives = data.ADJECTIVES
            if not adjectives:
                raise ValueError('empty adjectives')
        else:
            adjectives = []

        self.adjectives = adjectives

        self._sequence = self._make_sequence()
        self._get_name = self._make_name_func()

    def _make_sequence(self):
        if self.members == 1:
            return self.names
        if self.members == 2:
            adjectives = self.adjectives
        else:
            adjectives = Combinations(self.adjectives, self.members - 1)
        return Product(adjectives, self.names)

    def _make_name_func(self):
        if self.members == 1:
            return self._sequence.__getitem__
        elif self.members == 2:
            return self._name_single
        else:
            return self._name_multi

    def _name_single(self, index):
        item = self._sequence[index]
        return self.separator.join(item)

    def _name_multi(self, index):
        adjs, name = self._sequence[index]
        return self.separator.join((*adjs, name))

    @property
    def unique_count(self):
        return len(self._sequence)

    def __repr__(self):
        return '<{}: {} unique names>'.format(
            self.__class__.__name__, len(self._sequence))


class SimpleNameGenerator(NameGenerator):

    def __iter__(self):
        size = len(self._sequence)
        return (
            self._get_name(i)
            for i in itertools.cycle(range(size))
        )


class RandomNameGenerator(NameGenerator):

    def __iter__(self):
        size = len(self._sequence)
        while True:
            i = random.randrange(size)
            yield self._get_name(i)


class UniqueRandomNameGenerator(RandomNameGenerator, collections.Sequence):

    def __init__(
            self, members=2, separator='_', seed=None,
            names=None, adjectives=None):
        super().__init__(members, separator, names, adjectives)
        self._rnd_indices = RandomPermutation(len(self._sequence), seed)

    def __iter__(self):
        return (self._get_name(i) for i in self._rnd_indices)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self._get_name(i) for i in self._rnd_indices[index]]
        return self._get_name(self._rnd_indices[index])

    def __len__(self):
        return len(self._sequence)

    def __repr__(self):
        return '<{}: {!r}, {!r}, ... ({} total)>'.format(
            self.__class__.__name__, self[0], self[1], len(self))
