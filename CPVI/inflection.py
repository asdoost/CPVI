#!/usr/bin/env python3
import copy
from itertools import product

from .utils import (concatenate, prefix, conj, auxiliary, stemming, spacing,
                    prefixing, add_glide)

PRESENT_TENSES = ('simple', 'continuous', 'subjunctive', 'progressive',
                  'perfect', 'perfect past', 'imperative')
PAST_TENSES = ('simple', 'continuous', 'subjunctive', 'progressive',
               'perfect', 'perfect subjunctive')


def _missing():
    """Shape returned when a form cannot be built (e.g. IPA not provided)."""
    return {'present': {k: None for k in PRESENT_TENSES},
            'past': {k: None for k in PAST_TENSES},
            'future': {'simple': None}}


def _inflect_one(profile, formal, IPA, negative, space):
    """Build the present/past/future block for one
    (formality, alphabet, polarity) combination."""
    frmlty = 'formal' if formal else 'informal'
    alphabet = 'IPA' if IPA else 'Persian'

    bare_stems, past_stems = stemming(profile, frmlty, alphabet, glide=False)
    bare_stems = [s for s in bare_stems if s]
    if not bare_stems or not all(past_stems):
        return _missing()

    pres, sufs, wrds = spacing(space, IPA)
    prf_aux, sub_aux, prg_prs_aux, prg_pst_aux, ftr_aux = auxiliary(frmlty, alphabet)
    part_aux = 'bude' if IPA else 'بوده'
    past_conj, present_conj, perfect_conj, imperative_conj = conj(frmlty, alphabet)
    contix, neg, sub = prefix(negative, IPA)

    present = {k: [] for k in PRESENT_TENSES}
    past = {k: [] for k in PAST_TENSES}
    future = {'simple': []}

    for bare in bare_stems:
        raw = add_glide(bare)
        stem = prefixing(neg, raw, pres)
        sub_stem = prefixing(sub, raw, pres)
        cont_stem = prefixing(contix, raw, pres)

        present['simple'].append(concatenate(stem, present_conj))
        present['subjunctive'].append(concatenate(sub_stem, present_conj))
        present['continuous'].append(concatenate(cont_stem, present_conj))
        # s2 is the bare stem (no suffix to glide into); p2 takes the glide
        imperative = concatenate(sub_stem, imperative_conj)
        present['imperative'].append({
            's2': prefixing(sub, bare, pres) + imperative_conj['s2'],
            'p2': imperative['p2']})
        if not negative:                       # no negative progressive
            present['progressive'].append(
                concatenate(prg_prs_aux, wrds, present['continuous'][-1]))

    for raw in past_stems:
        stem = prefixing(neg, raw, pres)
        cont_stem = prefixing(contix, raw, pres)
        part = f'{stem}{"e" if IPA else "ه"}'   # past participle

        past['simple'].append(concatenate(stem, past_conj))
        past['continuous'].append(concatenate(cont_stem, past_conj))
        past['subjunctive'].append(concatenate(part, wrds, sub_aux))
        past['perfect'].append(concatenate(part, wrds, prf_aux))
        past['perfect subjunctive'].append(
            concatenate(part, wrds, part_aux, wrds, sub_aux))
        if not negative:                       # no negative progressive
            past['progressive'].append(
                concatenate(prg_pst_aux, wrds, past['continuous'][-1]))

        if formal:
            present['perfect past'].append(
                concatenate(part, wrds, part_aux, sufs, perfect_conj))
            present['perfect'].append(concatenate(part, sufs, perfect_conj))
            # negation goes on the auxiliary, the stem stays bare
            future['simple'].append(concatenate(neg, ftr_aux, wrds, raw))
        elif not IPA:                          # informal Persian
            present['perfect'].append(concatenate(stem, present_conj))
            present['perfect past'].append(dict(past['perfect'][-1]))
        else:                                  # informal IPA
            present['perfect past'].append(
                concatenate(part, wrds, part_aux[:-1], sufs, perfect_conj))
            present['perfect'].append(concatenate(part, sufs, perfect_conj))

    return {'present': unpack_all(present), 'past': unpack_all(past),
            'future': unpack_all(future)}


def unpack_all(tenses):
    """unpack() each tense: [dict] -> dict, [] -> None."""
    return {k: (None if not v else v[0] if len(v) == 1 else v)
            for k, v in tenses.items()}


def inflector(profile, space):
    """Inflect a verb profile. Does not mutate ``profile``.

    Returns a deep copy of the profile with ``paradigm`` filled in. A profile
    whose paradigm is already filled (hand-curated irregulars) is returned as
    is (copied) and ``space`` has no effect on it.
    """
    profile = copy.deepcopy(profile)
    if profile['paradigm']:
        return profile

    paradigm = {f: {a: {'affirmative': {}, 'negative': {}} for a in ('IPA', 'Persian')}
                for f in ('formal', 'informal')}
    for negative, formal, IPA in product((True, False), repeat=3):
        block = _inflect_one(profile, formal, IPA, negative, space)
        paradigm['formal' if formal else 'informal'][
            'IPA' if IPA else 'Persian'][
            'negative' if negative else 'affirmative'] = block
    profile['paradigm'] = paradigm
    return profile
