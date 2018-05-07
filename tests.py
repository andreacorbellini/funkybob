import itertools
import string

import pytest

import funkybob


@pytest.mark.parametrize('sequence,r', [
    (string.ascii_uppercase[:s], r)
    for s in range(16)
    for r in range(16)
])
def test_combinations(sequence, r):
    combos = funkybob.Combinations(sequence, r)
    expected = list(itertools.combinations(sequence, r))

    assert len(combos) == len(expected)
    assert list(combos) == expected
    assert [combos[i] for i in range(len(expected))] == expected
    assert combos[:] == expected
    assert combos[2:5] == expected[2:5]


@pytest.mark.parametrize('seq1,seq2', [
    (string.ascii_uppercase[:s], string.ascii_uppercase[:t])
    for s in range(16)
    for t in range(16)
])
def test_product(seq1, seq2):
    prod = funkybob.Product(seq1, seq2)
    expected = list(itertools.product(seq1, seq2))

    assert len(prod) == len(expected)
    assert list(prod) == expected
    assert [prod[i] for i in range(len(expected))] == expected
    assert prod[:] == expected
    assert prod[2:5] == expected[2:5]


@pytest.mark.parametrize('size', [
    2 ** n for n in range(3, 18)
])
def test_random_permutation(size):
    perm = funkybob.RandomPermutation(size, seed=0)

    # Fixed points
    assert perm[0] == 0
    assert perm[1] == 1

    nums = list(perm)
    assert len(nums) == len(perm)
    assert sorted(nums) == list(range(size))
    assert nums != sorted(nums)


@pytest.mark.parametrize('members', range(1, 5))
@pytest.mark.parametrize('cls', [
    funkybob.SimpleNameGenerator,
    funkybob.RandomNameGenerator,
    funkybob.UniqueRandomNameGenerator,
])
def test_generator(cls, members):
    gen = cls(members)

    it = iter(gen)
    sample = [next(it) for i in range(64)]

    for name in sample:
        assert name.islower()
        assert name.isidentifier()
        parts = name.split('_')
        assert len(parts) == members
        assert all(part.isalpha() for part in parts)


@pytest.mark.parametrize('members', range(1, 4))
def test_unique_generator(members):
    gen = funkybob.UniqueRandomNameGenerator(members)

    names = list(gen)

    assert len(names) == len(gen)
    assert len(names) == len(set(names))
    assert names == gen[:]
