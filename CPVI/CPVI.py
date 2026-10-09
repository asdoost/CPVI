#!/usr/bin/env python3
import json
import re
from pathlib import Path
from functools import lru_cache

from .loader import load
from .errors import IPAError, normalize_ipa, validate_input
from .inflection import inflector

FP_PAST, FP_PRES = 'formal Persian past stem', 'formal Persian present stem'
IP_PAST, IP_PRES = 'informal Persian past stem', 'informal Persian present stem'
FA_PAST, FA_PRES = 'formal IPA past stem', 'formal IPA present stem'
IA_PAST, IA_PRES = 'informal IPA past stem', 'informal IPA present stem'
_STEM_FIELDS = (FP_PRES, FP_PAST, IP_PRES, IP_PAST)

# Alternative verbs (e.g. رساندن / رسان+د|ید): present stem ends in "ان".
_ALT_FA = re.compile(r'(\w{2,}ان)(?:ی?د)?(?:ن)?')
_ALT_IPA = re.compile(r'(\w{2,}ɒn)(?:i?d)?(?:æn)?')


@lru_cache(maxsize=None)
def _irregular_index():
    """Map every infinitive / stem string to its entry key (first entry wins,
    same precedence as the old linear scan)."""
    index = {}
    for key, entry in load('irregulars').items():
        index.setdefault(key, key)
        for field in _STEM_FIELDS:
            value = entry[field]
            for stem in (value if isinstance(value, list) else [value]):
                if stem:                       # '' means "no informal form"
                    index.setdefault(stem, key)
    return index


def save_json(profile, path, indent=2, ensure_ascii=False):
    """
    Write a profile (as returned by ``CPVI.profiling``) to a JSON file.

    Parameters
    ----------
    profile : dict
        The profile to save.
    path : str or pathlib.Path
        Destination file. Missing parent directories are created and an
        existing file is overwritten. A ``.json`` suffix is added if the path
        has no suffix.
    indent : int or None, optional
        JSON indentation (``None`` gives a compact single line).
    ensure_ascii : bool, optional
        If False (default) Persian/IPA letters are written as-is (UTF-8);
        if True they are written as ``\\uXXXX`` escapes.

    Returns
    -------
    pathlib.Path
        The path that was written.
    """
    path = Path(path)
    if not path.suffix:
        path = path.with_suffix('.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(profile, file, ensure_ascii=ensure_ascii, indent=indent)
    return path


def _strip_regular(word, past_suffix, gerund_suffix):
    """Regular verbs: gerund = stem + id + n, past = stem + id."""
    if word.endswith(past_suffix + gerund_suffix):
        return word[:-len(past_suffix + gerund_suffix)]
    if word.endswith(past_suffix):
        return word[:-len(past_suffix)]
    return word


class CPVI():
    """
    Identify and inflect a Persian verb given its present stem, past stem or
    gerund.
    """
    IPA = {'b': 'ب', 'p': 'پ', 'f': 'ف', 'v': 'و', 't': ['ت', 'ط'], 'd': 'د',
           's': ['س', 'ص', 'ث'], 'z': ['ز', 'ض', 'ظ', 'ذ'], 'ʃ': 'ش', 'ʒ': 'ژ',
           'ʤ': 'ج', 'ʧ': 'چ', 'c': 'ک', 'ɟ': 'گ', 'x': 'خ', 'G': ['ق', 'غ'],
           'h': ['ه', 'ح'], 'ʔ': ['ع', 'همزه'], 'm': 'م', 'n': 'ن', 'r': 'ر',
           'l': 'ل', 'j': 'ی', 'ɒ': ['آ', 'ا'], 'u': 'او', 'i': 'ی',
           'æ': 'فتحه', 'e': 'کسره', 'o': 'ضمه'}

    @staticmethod
    def profiling(word, API_form='', space='\u200c', save_to=None):
        """
        Return the profile (properties + full paradigm) of a verb.

        Parameters
        ----------
        word : str
            Persian present stem, past stem or gerund.
        API_form : str, optional
            The same word in Persian IPA ('Ɉ' is accepted for 'ɟ').
            Ignored for irregular verbs (their IPA comes from the data file).
        space : str, optional
            '', ' ' or ZWNJ. Has no effect on the few hand-curated irregular
            paradigms (see README).
        save_to : str or pathlib.Path, optional
            If given, the profile is also written to this JSON file
            (see ``CPVI.save``). The profile is still returned.
        """
        validate_input(word, API_form, space)
        API_form = normalize_ipa(API_form)

        key = _irregular_index().get(word)
        if key is not None:
            return CPVI._finish(inflector(load('irregulars')[key], space), save_to)

        profile = {k: '' for k in load('irregulars')['دانستن']}
        alternative = bool(_ALT_FA.fullmatch(word))

        if alternative:
            m = _ALT_FA.fullmatch(word)
            pres = m.group(1)
            profile.update({'regularity': 'Alternative', 'transitivity': 'transitive',
                            'lexical aspect': 'action', 'present dual': False,
                            'past dual': True})
            profile[FP_PRES] = pres
            profile[FP_PAST] = [f'{pres}د', f'{pres}ید']
            profile[IP_PRES] = f'{pres[:-2]}ون'
            profile[IP_PAST] = [f'{profile[IP_PRES]}د', f'{profile[IP_PRES]}ید']
        else:
            pres = _strip_regular(word, 'ید', 'ن')
            profile.update({'regularity': 'Regular', 'transitivity': 'unknown',
                            'lexical aspect': 'unknown', 'present dual': False,
                            'past dual': False})
            profile[FP_PRES] = pres
            profile[FP_PAST] = pres + ('ئید' if pres[-1] in 'اوی' else 'ید')
            profile[IP_PRES], profile[IP_PAST] = profile[FP_PRES], profile[FP_PAST]

        if API_form:
            if alternative:
                m = _ALT_IPA.fullmatch(API_form)
                if not m:
                    raise IPAError('"word" is an alternative verb but "API_form" '
                                   'does not look like one (expected ...ɒn[i]d[æn])')
                pres = m.group(1)
                profile[FA_PRES] = pres
                profile[FA_PAST] = [f'{pres}d', f'{pres}id']
                profile[IA_PRES] = f'{pres[:-2]}un'
                profile[IA_PAST] = [f'{profile[IA_PRES]}d', f'{profile[IA_PRES]}id']
            else:
                pres = _strip_regular(API_form, 'id', 'æn')
                profile[FA_PRES] = pres
                profile[FA_PAST] = pres + ('ʔid' if pres[-1] in 'æɒouie' else 'id')
                profile[IA_PRES], profile[IA_PAST] = profile[FA_PRES], profile[FA_PAST]
        return CPVI._finish(inflector(profile, space), save_to)

    @staticmethod
    def _finish(profile, save_to):
        if save_to is not None:
            save_json(profile, save_to)
        return profile

    @staticmethod
    def save(profile, path, indent=2, ensure_ascii=False):
        """Save an existing profile to a JSON file; see ``save_json``."""
        return save_json(profile, path, indent=indent, ensure_ascii=ensure_ascii)
