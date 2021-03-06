#!/usr/bin/env python3

from itertools import product
from .utils import *


def inflector(profile, space):
    """
    Inflect the verb that its stems passed as the profile

    Parameters
    ----------
    profile : dict
        a dictionary containing the properties of the verb
    space : str
        a string that is either space (" "), ZWNJ (\\u200c), or 
        empty string ("")
    
    Returns
    -------
    dict
        a nested dictionary containing the properties and inflected forms of 
        the verb
    """

    # return profile if paradigm is already filled
    if profile['paradigm']:
        return profile

    # make an empty paradigm frame
    paradigm = {'formal': {
                    'IPA': {'affirmative': {}, 'negative': {}}, 
                    'Persian': {'affirmative': {}, 'negative': {}}},
                'informal': {
                    'IPA': {'affirmative': {}, 'negative': {}}, 
                    'Persian': {'affirmative': {}, 'negative': {}}}}
    
    # make a list of tuples for iteration
    comb = product([True, False], repeat=3)

    # iterate through negation, formality, and IPA
    for negation, formality, IPA in comb:

        # make empty dictionaries for past, present, and future
        past = {'simple': [], 'continuous': [], 'subjunctive': [], 
        'progressive': [], 'perfect': [], 'perfect subjunctive': []}
        present = {'simple': [], 'continuous': [], 'subjunctive': [], 
        'progressive': [], 'perfect': [], 'perfect past': [], 'imperative': []}
        future = {'simple': []}

        # turn booleans to string
        frmlty = ['informal', 'formal'][formality]
        alphabet = ['Persian', 'IPA'][IPA]
        polarity = ['affirmative', 'negative'][negation]

        # retrieve present and past stems
        present_stem, past_stem = steming(profile, frmlty, alphabet)

        # assign suffix and word spaces
        pres, sufs, wrds = spacing(space, IPA)

        # retrieve auxiliaries
        prf_aux, sub_aux, prg_prs_aux, prg_pst_aux, ftr_aux = auxiliary(frmlty, alphabet)

        # the participle form of the perfect auxiliary
        part_aux = ["????????", "bude"][IPA]

        # retrieve conjugations
        past_conj, present_conj, perfect_conj, imperative_conj = conj(frmlty, alphabet)

        # retrieve continuous, negation, and subjunctive prefixes
        contix, neg, sub =  prefix(negation, IPA)

        # inflect present stem
        for stem in present_stem:

            # prevent execution if the IPA form of the stem is not provided
            if stem == '':
                present = None
                break

            stem, sub_stem, cont_stem = (prefixing(neg, stem, space),
                                        prefixing(sub, stem, space),
                                        prefixing(contix, stem, space))
            # ???????????
            present['simple'].append(concatenate(stem, present_conj))

            # ??????????
            present['subjunctive'].append(concatenate(sub_stem, present_conj))

            # ?????????????????
            present['continuous'].append(concatenate(cont_stem, present_conj))

            # ??????
            imperative = concatenate(sub_stem, imperative_conj)
            imperative = {'s2': imperative['s2'], 'p2': imperative['p2']}
            present['imperative'].append(imperative)

            # exclude the negative conjugation of present progressives
            if not negation:
                # ???????? ??????????????????
                present['progressive'].append(concatenate(
                    prg_prs_aux, wrds, present['continuous'][-1]))

        # inflect past stem
        for stem in past_stem:

            # prevent execution if the IPA from of the stem is not provided
            if stem == '':
                past = None
                break

            stem, sub_stem, cont_stem = (prefixing(neg, stem, pres),
                                        prefixing(sub, stem, pres),
                                        prefixing(contix, stem, pres))

            # past participle
            part = prefixing('', f'{stem}{["??", "e"][IPA]}', space)

            # ??????????
            past['simple'].append(concatenate(stem, past_conj))

            # ?????????????????
            past['continuous'].append(concatenate(cont_stem, past_conj))

            # ?????????? ????????
            past['subjunctive'].append(concatenate(part, wrds, sub_aux))

            # ?????????? ????????
            past['perfect'].append(concatenate(part, wrds, prf_aux))

            # ?????????? ???????? ????????
            past['perfect subjunctive'].append(concatenate(
                part, wrds, part_aux, wrds, sub_aux))

            # exclude the negative conjugation of past progressives
            if not negation:
                # ?????????? ???????????????
                past['progressive'].append(concatenate(prg_pst_aux, 
                                            wrds, past['continuous'][-1]))

            # exclude the informal conjugation of the simple future
            if formality:
                # ????????????? ???????????????
                present['perfect past'].append(concatenate(
                    part, wrds, part_aux, sufs, perfect_conj))
                # ?????????????????
                present['perfect'].append(concatenate(
                    part, sufs, perfect_conj))
                # ???????????? ??????
                future['simple'].append(concatenate(neg, ftr_aux, wrds, stem))
            elif not formality and not IPA:
                # ??????????
                present['perfect'].append(concatenate(stem, present_conj))
                # ????????????? ????????
                present['perfect past'].append(past['perfect'][-1])
            else:
                # ????????????? ???????????????
                present['perfect past'].append(concatenate(
                    part, wrds, part_aux[:-1], sufs, perfect_conj))
                # ?????????????????
                present['perfect'].append(concatenate(
                    part, sufs, perfect_conj))

        paradigm[frmlty][alphabet][polarity] = {'present': unpack(
            present), 'past': unpack(past), 'future': unpack(future)}

    profile['paradigm'] = paradigm
    return profile


profile = {
    'lexical aspect': 'action',
    'regularity': 'Alternative',
    'transitivity': 'transitive',
    'present dual': False,
    'past dual': True,
    'formal IPA present stem': 'res??n',
    'formal IPA past stem': ['res??nd', 'res??nid'],
    'formal Persian present stem': '????????',
    'formal Persian past stem': ['??????????', '????????????'],
    'informal IPA present stem': 'resun',
    'informal IPA past stem': ['resund', 'resunid'],
    'informal Persian present stem': '????????',
    'informal Persian past stem': ['??????????', '????????????'],
    'paradigm': ''}
profile = {
    'lexical aspect': 'accomplishment',
    'regularity': 'irregular',
    'transitivity': 'intransitive',
    'present dual': False,
    'past dual': False,
    'formal IPA present stem': '????',
    'formal IPA past stem': '????m??d',
    'formal Persian present stem': '??',
    'formal Persian past stem': '??????',
    'informal IPA present stem': '????',
    'informal IPA past stem': '??um??d',
    'informal Persian present stem': '??',
    'informal Persian past stem': '????????',
    'paradigm': ''}

if __name__ == '__main__':
    p = inflector(profile, ' ')
    print(p['paradigm']['formal']['IPA']['affirmative']['present']['subjunctive']['s1'])
