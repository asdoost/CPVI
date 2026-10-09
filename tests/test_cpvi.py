import copy
import json
import pytest

from CPVI import CPVI, IPAError
from CPVI.loader import load
from CPVI.utils import concatenate, prefixing, stemming

ZWNJ = '\u200c'


def leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from leaves(v)
    else:
        yield o


def test_concatenate_aligns_list_valued_dicts():
    aux = {'s1': 'a', 's2': 'a', 's3': 'a', 'p1': 'a', 'p2': ['x', 'y'], 'p3': 'a'}
    tail = {k: 'T' for k in ('s1', 's2', 's3', 'p1', 'p2', 'p3')}
    out = concatenate(aux, '-', tail)
    assert out['p2'] == ['x-T', 'y-T']
    assert out['s1'] == 'a-T'


def test_stemming_dual_has_no_duplicates():
    prof = load('irregulars')['بودن']
    assert stemming(prof, 'formal', 'IPA')[0] == ['æst', 'hæst', 'bɒʃ']


@pytest.mark.parametrize('pfx,stem,expected', [
    ('mi', 'ɒmæd', 'mijɒmæd'), ('mi', 'ʔɒ', 'mijɒ'), ('mi', 'gu', 'migu'),
    ('be', 'ɒmæd', 'bijɒmæd'), ('næ', 'ʔɒ', 'næjɒ'),
    ('می', 'آ', 'می\u200cآ'), ('ب', 'آ', 'بیا')])
def test_prefixing(pfx, stem, expected):
    assert prefixing(pfx, stem, ZWNJ) == expected


def test_prefixing_unknown_prefix_raises():
    with pytest.raises(ValueError):
        prefixing('zzz', 'x', ZWNJ)


def test_readme_example_amad():
    p = CPVI.profiling('آمد', 'ʔɒmæd', ZWNJ)['paradigm']['formal']['IPA']['affirmative']
    assert p['present']['simple']['s1'] == 'ʔɒjæm'
    assert p['present']['continuous']['p3'] == 'mijɒjænd'


def test_negative_future_has_single_negation():
    f = CPVI.profiling('آمد')['paradigm']['formal']['Persian']['negative']['future']['simple']
    assert f['s1'] == 'نخواهم' + ZWNJ + 'آمد'


def test_gerund_is_stripped():
    p = CPVI.profiling('خندیدن')
    assert p['formal Persian present stem'] == 'خند'
    assert p['formal Persian past stem'] == 'خندید'


def test_space_argument_changes_generated_forms():
    a = CPVI.profiling('خند', '', ZWNJ)['paradigm']['formal']['Persian']['affirmative']['present']['continuous']['s1']
    b = CPVI.profiling('خند', '', ' ')['paradigm']['formal']['Persian']['affirmative']['present']['continuous']['s1']
    assert a != b


def test_no_shared_state_mutation():
    before = copy.deepcopy(load('irregulars'))
    CPVI.profiling('گسل', 'ɟosæl', ZWNJ)
    CPVI.profiling('گفت', '', ' ')
    assert load('irregulars') == before


def test_past_stem_lookup_for_double_dual_verb():
    assert CPVI.profiling('سپارد')['regularity'] == 'irregular'


def test_empty_word_rejected():
    with pytest.raises(ValueError):
        CPVI.profiling('')


def test_bad_ipa_and_space():
    with pytest.raises(TypeError):
        CPVI.profiling('خند', 'xænd!')
    with pytest.raises(IPAError):
        CPVI.profiling('خند', 'xænd!')
    with pytest.raises(ValueError):
        CPVI.profiling('خند', 'xænd', '-')


def test_legacy_and_data_ipa_glyph_both_accepted():
    assert CPVI.profiling('گسل', 'Ɉosæl') and CPVI.profiling('گسل', 'ɟosæl')


@pytest.mark.parametrize('verb', list(load('irregulars')))
def test_every_irregular_inflects_without_stringified_lists(verb):
    for sp in (ZWNJ, ' ', ''):
        p = CPVI.profiling(verb, '', sp)
        for leaf in leaves(p['paradigm']):
            assert not (isinstance(leaf, str) and "['" in leaf)


def test_imperative_2sg_has_no_glide_but_plural_does():
    imp = CPVI.profiling('شنو', 'ʃeno')['paradigm']['formal']['Persian']['affirmative']['present']['imperative']
    assert imp == {'s2': 'بشنو', 'p2': 'بشنویید'}


def test_save_to_writes_utf8_json_roundtrip(tmp_path=None):
    import tempfile, pathlib
    d = pathlib.Path(tempfile.mkdtemp())
    p = CPVI.profiling('گفت', 'ɟoft', ZWNJ, save_to=d / 'sub' / 'verb')   # suffix added, dirs created
    out = d / 'sub' / 'verb.json'
    assert out.exists()
    text = out.read_text(encoding='utf-8')
    assert 'گفت' in text and '\\u06' not in text          # not escaped
    assert json.loads(text) == p                             # lossless round trip


def test_save_method_and_ascii_option():
    import tempfile, pathlib
    d = pathlib.Path(tempfile.mkdtemp())
    p = CPVI.profiling('خند', 'xænd')
    out = CPVI.save(p, d / 'a.json', indent=None, ensure_ascii=True)
    assert out.read_text(encoding='utf-8').isascii()
    assert json.loads(out.read_text(encoding='utf-8')) == p
