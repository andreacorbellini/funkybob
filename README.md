# Random name generator in Python

funkybob is a Python library for generating Docker-style random names,
like these:

    ecstatic_ritchie, kind_beaver, sharp_heisenberg, angry_nightingale, ...

funkybob supports generating names preceeded by an arbirary number of
adjectives, in order to increase the number of unique names that can
be generated:

    Random names with no adjectives:
        swirles, khorana, blackwell, ...

    Random names preceeded by an adjective:
        ecstatic_ritchie, kind_beaver, sharp_heisenberg, ...

    Random names preceeded by two adjectives:
        admiring_dazzling_noether, thirsty_wonderful_agnesi, silly_wizardly_feynman, ...

    Random names preceeded by three adjectives:
        cranky_goofy_hopeful_wright, competent_jolly_suspicious_kare, cocky_competent_gifted_yalow, ...

When using more than one adjective, funkybob ensures that two names with the
same set of adjectives cannot occur, even if the order is different. So, for
example, if the name `inspiring_stupefied_payne` was generated, then you can
be sure that the name `stupefied_inspiring_payne` won't be generated later.
This makes names much more easier to distinguish and less likely to generate
confusion.


## Installation

The package is hosted on [PyPI](https://pypi.org/project/funkybob/),
to install use:

```shell
$ pip install funkybob
```


## Generators

funkybob ships three different name generators:

* **SimpleNameGenerator**: this provides a deterministic sequence of names --
  no randomness involved. This will return duplicate names once all
  combinations have been yielded. Useful if all you care about is performance.

* **RandomNameGenerator**: returns randomly generated names. It may return
  duplicate names at any point.

* **UniqueRandomNameGenerator**: returns randomly generated names, but unlike
  RandomNameGenerator, no duplicates are returned. Unlike the other two
  generators, this one has a limited size and will stop yielding values once
  all unique names have been returned.

This table sumarizes the features of all three generators:

| Generator                 | Infinite | Random | Duplicates |
|---------------------------|----------|--------|------------|
| SimpleNameGenerator       | Yes      | No     | Yes        |
| RandomNameGenerator       | Yes      | Yes    | Yes        |
| UniqueRandomNameGenerator | No       | Yes    | No         |


## Usage

All three generators are iterables, which means that you can simply use
`iter()` and `next()` on them in order to retrieve names:

```python
>>> import funkybob
>>> generator = funkybob.RandomNameGenerator()
>>> it = iter(generator)
>>> next(it)
'practical_hoover'
>>> next(it)
'stupefied_ramanujan'
>>> next(it)
'zealous_aryabhata'
```

You can pass the `members` and `separator` parameters to change the number of
adjectives or the formatting of names:

```python
>>> # This will generate names with 3 members (2 adjectives + 1 last name),
>>> # separated by a colon
>>> generator = funkybob.RandomNameGenerator(members=3, separator=':')
>>> it = iter(generator)
>>> next(it)
'friendly:hopeful:neumann'
>>> next(it)
'admiring:trusting:montalcini'
>>> next(it)
'practical:suspicious:blackwell'
```

Generators have an `unique_count` attribute that you can use to check
the number of unique names that can be generated:

```python
>>> generator.unique_count
740094
```


### UniqueRandomNameGenerator

In addition to all of the above, UniqueRandomNameGenerator privides a
[sequence](https://docs.python.org/3/glossary.html#term-sequence)-like
interfance, which means, for example, that you can use indexing or the
`len()` method (which is the same as accessing the `unique_count`
attribute):

```python
>>> generator = funkybob.UniqueRandomNameGenerator()
>>> generator[0]
'xenodochial_yalow'
>>> generator[1]
'kind_mccarthy'
>>> generator[2]
'happy_hawking'
>>> len(generator)
16089
```

You can increase the number of `members` in order to increase the size,
at the expense of having longer names.

UniqueRandomNameGenerator also supports an additional parameter: `seed`.
This can be used to initialize the pseudo-random generator. If you pass
always the same value, the same sequence of names will be generated. This
can be useful in tests when you need predictable names.
