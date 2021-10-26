#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
from pathlib import Path
import json

def concatenate(*args):
    """
    Concatenate the string with string or with every value of the dictionary

    Parameters
    ----------
    *args : str, dict
        (a) string(s) or dictionar(ies)
    
    Returns
    -------
    dict
        a nested dictionary containing concatenated forms of args
    """
    paradigm = {'s1': '', 's2': '', 's3': '',
                'p1': '', 'p2': '', 'p3': ''}
    # make a string by replacing every dictionary with curly bracket
    form = ''.join(i if isinstance(i, str) else '{}' for i in args)

    # enclose every value of dictionary in args with bracket and
    # add it to the paradigm
    for key in paradigm:
        lst = []
        for arg in args:
            if isinstance(arg, dict) and key in arg:
                if isinstance(arg[key], list):
                    lst.append(arg[key])
                lst.append([arg[key]])
        paradigm[key] = lst

    # fill with every items in paradigm
    for key, val in paradigm.items():
        l = [form.format(*element) for element in product(*val)]
        paradigm[key] = l[0] if len(l) == 1 else l

    return paradigm

def prefix(neg, API):
    """
    Retrieve appropriate forms of prefixes based on polarity and alphabet

    Parameters
    ----------
    neg : bool
        A flag used to determine the polarity
    API : bool
        A flag used to determine the type of alphabet

    Returns
    -------
    list
        a list of appropriate prefixes
    """
    cont = [[f'می', 'mi'], [f'نمی', 'nemi']][neg][API]
    negt = 'næ' if neg and API else 'ن' if neg else ''
    sub = [['ب', 'be'], ['ن', 'næ']][neg][API]
    return [cont, negt, sub]

def conj(frm, alph):
    """
    Retrieve appropriate conjugation dictionaries

    Parameters
    ----------
    frm : str
        A string used to determine the formality
    alph : str
        A string used to determine the type of alphabet

    Returns
    -------
    list of dicts
        a list of dictionaries containing appropriate conjugations
    """

    dir_path = Path(__file__).parents[0]
    path = f'{dir_path}/data/conjugations.json'

    with open(path, 'r', encoding='utf-8') as file:
        conjugations = json.load(file)['subjective']

    # retrieve conjugations
    past = conjugations[frm][alph]['past']
    present = conjugations[frm][alph]['present']
    perfect = conjugations[frm][alph]['perfect']
    imperative = conjugations[frm][alph]['imperative']
    return [past, present, perfect, imperative]

def auxiliary(frm, alph):
    """
    Retrieve appropriate auxiliaries

    Parameters
    ----------
    frm : str
        A string used to determine the formality
    alph : str
        A string used to determine the type of alphabet

    Returns
    -------
    list
        a list of auxiliaries
    """
    dir_path = Path(__file__).parents[0]
    path = f'{dir_path}/data/irregulars.json'

    # load irregulars and conjugations files
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # retrieve past perfect auxiliary
    prf_aux = data['بودن']['paradigm'][frm][alph]['affirmative']['past']['simple']
    # retrieve past subjunctive auxiliary
    sub_aux = data['بودن']['paradigm'][frm][alph]['affirmative']['present']['subjunctive']
    # retrieve present progressive auxiliary
    prg_prs_aux = data['داشتن']['paradigm'][frm][alph]['affirmative']['present']['simple']
    # retrieve past progressive auxiliary
    prg_pst_aux = data['داشتن']['paradigm'][frm][alph]['affirmative']['past']['simple']
    # retrieve future auxiliary
    ftr_aux = data['خواستن']['paradigm'][frm][alph]['affirmative']['present']['simple']
    return [prf_aux, sub_aux, prg_prs_aux, prg_pst_aux, ftr_aux]

def steming(profile, frmlty, alphabet):
    """
    Retrieve stems from the dictionary

    Parameters
    ----------
    profile : dict
        A dictionary containing properties of a verb
    frmlty : str
        A string used to determine the formality
    alphabet : str
        A string used to determine the type of alphabet

    Returns
    -------
    list
        a list of past and present stems
    """
    path = f'{frmlty} {alphabet}'
    if profile['present dual']:
        present = profile[f'{path} present stem']
    else:
        present = [profile[f'{path} present stem']]
    if profile['past dual']:
        past = profile[f'{path} past stem']
    else:
        past = [profile[f'{path} past stem']]
    
    present_stem = []
    for stem in present:
        if stem:
            if stem[-1] in 'اوآ':
                present_stem.append(f'{stem}ی')
            elif stem[-1] in 'ɒui':
                present_stem.append(f'{stem}j')
    return [present_stem, past]

def spacing(space, API):
    """
    Assign space based on its location

    Parameters
    ----------
    API : bool
        A flag used to determine the type of alphabet
    space : str
        The type of space chosen by user

    Returns
    -------
    list
        a list of spaces for prefixes, suffixes, and words
    """
    if API:
        return ['', '', ' ']
    elif space == ' ' or space == '\u200c':
        return [space, space, space]
    elif space == '':
        return ['', '\u200c', '\u200c']

def prefixing(prefix, stem, space):
    """
    Add the prefix to the stem based on the space that has been chosen

    Parameters
    ----------
    prefix : str
        A prefix string
    stem : str
        A stem string
    space : str
        The type of space chosen by user

    Returns
    -------
    list
        The concatenated form of prefix and stem
    """
    if prefix == '':
        return stem
    elif prefix in ['می', 'نمی']:
        if space in ['\u200c', ' ']:
            return f'{prefix}{space}{stem}'
        elif space == '':
            if stem.startswith('آ'):
                return f'{prefix}ا{stem[1:]}'
            elif stem.startswith('ا'):
                return f'{prefix}{stem[1:]}'
            return f'{prefix}{stem}'
    elif prefix in ['mi', 'nemi']:
        if stem[:2] in ['ʔɒ', 'ʔæ', 'ʔo', 'ʔe', 'ʔi', 'ʔu'] or stem[0] in 'ɒæoeiu':
            return f'{prefix}j{stem[1:]}'
        return f'{prefix}{stem}'
    elif prefix in ['ب', 'ن']:
        if stem.startswith('آ'):
            return f'{prefix}یا{stem[1:]}'
        elif stem.startswith('ای'):
            return f'{prefix}{stem}'
        elif stem.startswith('ا'):
            return f'{prefix}ی{stem[1:]}'
        return f'{prefix}{stem}'
    elif prefix == 'be':
        if stem[:2] in ['ʔɒ', 'ʔæ', 'ʔo', 'ʔe', 'ʔi', 'ʔu'] or stem[0] in 'ɒæoeiu':
            return f'bij{stem[1:]}'
        return f'{prefix}{stem}'
    elif prefix == 'næ':
        if stem[:2] in ['ʔɒ', 'ʔæ', 'ʔo', 'ʔe', 'ʔi', 'ʔu'] or stem[0] in 'ɒæoeiu':
            return f'{prefix}j{stem[1:]}'
        return f'{prefix}{stem}'
    else:
        print('>>>>>>>>>>', "Please contact us to tell what did you get wrong")
        

def unpack(dic):
    """
    Unpack lists with only one member

    Parameters
    ----------
    dic : dict
        A nested dictionary

    Returns
    -------
    dict
        A dictionary that its value unlisted
    """
    if dic == None:
        return None
    dix = dict()
    for x, y in dic.items():
        if isinstance(y, list) and len(y) == 1:
            dix[x] = y[0]
        elif y == []:
            dix[x] = None
        else:
            dix[x] = y
    return dix

if __name__=='__main__':
    print(concatenate('a', {'s1': 'x', 's2': 'x', 's3': 'x', 
                            'p1': 'x', 'p2': 'x', 'p3': 'x'}))
    print(prefixing('نمی', 'ایست', ''))
    print(auxiliary('formal', 'API'))
