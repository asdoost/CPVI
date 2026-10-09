#!/usr/bin/env python3
from collections import namedtuple
from itertools import product

from .loader import load

PERSONS = ('s1', 's2', 's3', 'p1', 'p2', 'p3')
IPA_VOWELS = 'ɒæoeiu'

Prefixes = namedtuple('Prefixes', 'continuous negative subjunctive')
Spaces = namedtuple('Spaces', 'prefix suffix word')


def concatenate(*args):
    """Concatenate strings and person-dictionaries into one person-dictionary.

    Every dict contributes ``dict[person]``; a list value means "alternative
    forms" and yields the cartesian product.
    """
    template = ''.join(
        '{}' if isinstance(a, dict) else a.replace('{', '{{').replace('}', '}}')
        for a in args)
    paradigm = {}
    for person in PERSONS:
        options = []
        for a in args:
            if isinstance(a, dict):
                value = a[person]              # KeyError beats silent misalignment
                options.append(value if isinstance(value, list) else [value])
        forms = [template.format(*combo) for combo in product(*options)]
        paradigm[person] = forms[0] if len(forms) == 1 else forms
    return paradigm


def prefix(negative, IPA):
    """Return the (continuous, negative, subjunctive) prefixes."""
    if IPA:
        return Prefixes('nemi', 'næ', 'næ') if negative else Prefixes('mi', '', 'be')
    return Prefixes('نمی', 'ن', 'ن') if negative else Prefixes('می', '', 'ب')


def conj(formality, alphabet):
    """Return [past, present, perfect, imperative] conjugation dicts."""
    c = load('conjugations')['subjective'][formality][alphabet]
    return [c['past'], c['present'], c['perfect'], c['imperative']]


def auxiliary(formality, alphabet):
    """Return [past-perfect, subjunctive, present-progressive,
    past-progressive, future] auxiliaries."""
    data = load('irregulars')

    def aux(verb, tense, kind):
        return data[verb]['paradigm'][formality][alphabet]['affirmative'][tense][kind]

    return [aux('بودن', 'past', 'simple'), aux('بودن', 'present', 'subjunctive'),
            aux('داشتن', 'present', 'simple'), aux('داشتن', 'past', 'simple'),
            aux('خواستن', 'present', 'simple')]


def add_glide(stem):
    """Vowel-final present stems take a glide before vowel-initial suffixes."""
    if stem and stem[-1] in 'اوآ':
        return stem + 'ی'
    if stem and stem[-1] in 'ɒui':
        return stem + 'j'
    return stem


def stemming(profile, formality, alphabet, glide=True):
    """Return (present_stems, past_stems) as lists. Empty strings are kept so
    the caller can detect missing IPA. ``glide=False`` returns bare stems."""
    key = f'{formality} {alphabet}'
    present = profile[f'{key} present stem']
    past = profile[f'{key} past stem']
    present = present if profile['present dual'] else [present]
    past = past if profile['past dual'] else [past]

    present_stems = [add_glide(s) if glide else s for s in present]
    return present_stems, list(past)


def spacing(space, IPA):
    """Return Spaces(prefix, suffix, word)."""
    if IPA:
        return Spaces('', '', ' ')
    if space in (' ', '\u200c'):
        return Spaces(space, space, space)
    if space == '':
        return Spaces('', '\u200c', '\u200c')
    raise ValueError(f'Invalid space: {space!r}')


def _ipa_attach(pfx, stem):
    """IPA: a vowel-initial stem (optionally ?-initial) takes a glide: mi+j+ɒ."""
    if stem.startswith('ʔ'):
        stem = stem[1:]
    if stem and stem[0] in IPA_VOWELS:
        return f'{pfx}j{stem}'
    return f'{pfx}{stem}'


def prefixing(pfx, stem, space):
    """Attach a prefix to a stem following Persian / IPA orthographic rules."""
    if pfx == '':
        return stem
    if pfx in ('می', 'نمی'):
        if space in ('\u200c', ' '):
            return f'{pfx}{space}{stem}'
        if space == '':
            if stem.startswith('آ'):
                return f'{pfx}ا{stem[1:]}'
            if stem.startswith('ا'):
                return f'{pfx}{stem[1:]}'
            return f'{pfx}{stem}'
        raise ValueError(f'Invalid space: {space!r}')
    if pfx in ('mi', 'nemi', 'næ'):
        return _ipa_attach(pfx, stem)
    if pfx == 'be':
        if stem.startswith('ʔ'):
            stem = stem[1:]
        return f'bij{stem}' if stem and stem[0] in IPA_VOWELS else f'be{stem}'
    if pfx in ('ب', 'ن'):
        if stem.startswith('آ'):
            return f'{pfx}یا{stem[1:]}'
        if stem.startswith('ای'):
            return f'{pfx}{stem}'
        if stem.startswith('ا'):
            return f'{pfx}ی{stem[1:]}'
        return f'{pfx}{stem}'
    raise ValueError(f'Unknown prefix: {pfx!r}')


def unpack(dic):
    """Unwrap one-element lists; empty lists become None."""
    if dic is None:
        return None
    return {k: (v[0] if isinstance(v, list) and len(v) == 1
                else None if v == [] else v) for k, v in dic.items()}
