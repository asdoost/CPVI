#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .inflection import inflector
from .errors import custom_errors
from pathlib import Path
import json
import re

class CPVI():
    """
    A class used to identify and inflect a given verb stem (present or past) 
    and gerund.

    Attributes
    ----------
    word : str
        a string in Persian alphabet used to return the Persian form of stems
    API_form : str, optional
        a string in API alphabet used to return the API form of stems
    profile : dict of dicts
        a nested dictionary containing properties and inflected forms of 
        a given verb
    """
    API = {'b': 'ب', 'p': 'پ', 'f': 'ف', 'v': 'و', 't': ['ت', 'ط'], 'd': 'د',
            's': ['س', 'ص', 'ث'], 'z': ['ز', 'ض', 'ظ', 'ذ'], 'ʃ': 'ش', 'ʒ': 'ژ',
            'ʤ': 'ج', 'ʧ': 'چ', 'c': 'ک', 'Ɉ': 'گ', 'x': 'خ', 'G': ['ق', 'غ'],
            'h': ['ه', 'ح'], 'ʔ': ['ع', 'همزه'], 'm': 'م', 'n': 'ن', 'r': 'ر',
            'l': 'ل', 'j': 'ی', 'ɒ': ['آ', 'ا'], 'u': 'او', 'i': 'ی',
            'æ': 'فتحه', 'e': 'کسره', 'o': 'ضمه'}
    
    def __init__(self) -> None:
        pass
    
    def profiling(self, word, API_form='', space='\u200c'):
        """
        Get the properties of the verb passed as the word

        Parameters
        ----------
        word : str
            a string in Persian alphabet used to return the Persian form of stems
        API_form : str, optional
            a string in API alphabet used to return the API form of stems
        
        Returns
        -------
        dict
            a dictionary containing the properties of the verb passed as word
        """
        # raise errors
        custom_errors(API_form, space)

        # get the directory path
        dir_path = Path(__file__).parents[1]
        path = f'{dir_path}/data/irregulars.json'

        # open & load irregulars
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # make shorthands for the dictionary keys
        fp_past = 'formal Persian past stem'
        fp_pres = 'formal Persian present stem'
        ip_past = 'informal Persian past stem'
        ip_pres = 'informal Persian present stem'
        fa_past = 'formal API past stem'
        fa_pres = 'formal API present stem'
        ia_past = 'informal API past stem'
        ia_pres = 'informal API present stem'

        # search through irregulars and return the word's profile
        for entry in data:
            if (word == entry or
                word == data[entry][fp_past] or
                word == data[entry][fp_pres] or
                word == data[entry][ip_past] or
                word == data[entry][ip_pres]):
                return inflector(data[entry], space)
            # if the entry is a dual verb look for the word in lists
            elif data[entry]['present dual']:
                if (word in data[entry][fp_pres] or
                    word in data[entry][ip_pres]):
                    return inflector(data[entry], space)
            elif data[entry]['past dual']:
                if (word in data[entry][fp_past] or
                    word in data[entry][ip_past]):
                    return inflector(data[entry], space)
        
        # make a profile frame
        profile = {key: '' for key in data['دانستن'].keys()}

        # regex patterns for Persian and API alternative and 
        # regular forms, respectively
        pat = [re.compile(r'(\w{2,}ان)(ی)?(د)?(ن)?'),
                re.compile(r'(.+)(ید)?(ن)?\b'),
                re.compile(r'(\w+[ɒuiæeo]?[bpfvtdszʃʒʤʧcɈxGhʔ\
                                mnrlj]{1,3}ɒn)i?d?(æn)?\b'),
                re.compile(r'(.+)(id)?(æn)?\b')]

        # Alternative Persian form
        if pat[0].search(word):
            profile['regularity'] = 'Alternative'
            profile['transitivity'] = 'transitive'
            profile['lexical aspect'] = 'action'
            profile['present dual'] = False
            profile['past dual'] = True
            # Persian
            profile[fp_pres] = pat[0].sub(r'\1', word)
            profile[fp_past] = [pat[0].sub(r'\1د', word), 
                                pat[0].sub(r'\1ید', word)]
            profile[ip_pres] = f'{profile[fp_pres][:-2]}ون'
            profile[ip_past] = [f'{profile[ip_pres]}د',
                                f'{profile[ip_pres]}ید']

        # Regular Persian form
        elif pat[1].search(word):
            profile['regularity'] = 'Regular'
            profile['transitivity'] = 'unknown'
            profile['lexical aspect'] = 'unknown'
            profile['past dual'] = False
            profile['present dual'] = False

            profile[fp_pres] = pat[1].sub(r'\1', word)
            # stems ended in vowels
            if profile[fp_pres][-1] in 'اوی':
                profile[fp_past] = pat[1].sub(r'\1ئید', word)
            else:
                profile[fp_past] = pat[1].sub(r'\1ید', word)
            profile[ip_pres] = profile[fp_pres]
            profile[ip_past] = profile[fp_past]

        # Alternative API form
        if API_form == '':
            return inflector(profile, space)

        elif pat[2].search(API_form):
            # API
            profile[fa_pres] = pat[2].sub(r'\1', API_form)
            profile[fa_past] = [pat[2].sub(r'\1d', API_form),
                                pat[2].sub(r'\1id', API_form)]
            profile[ia_pres] = f'{profile[fa_pres][:-2]}un'
            profile[ia_past] = [f'{profile[ia_pres]}d', 
                                f'{profile[ia_pres]}id']

        # Regular API form
        elif pat[3].search(API_form):
            profile[fa_pres] = pat[3].sub(r'\1', API_form)
            # stems ended in vowels
            if profile[fa_pres][-1] in 'æɒouie':
                profile[fa_past] = pat[3].sub(r'\1ʔid', API_form)
            else:
                profile[fa_past] = pat[3].sub(r'\1id', API_form)
            profile[ia_pres] = profile[fa_pres]
            profile[ia_past] = profile[fa_past]
        return inflector(profile, space)


if __name__ == '__main__':
    p = CPVI()
    profile = p.profiling('گسل', 'Ɉosæl', '\u200c')
    print(profile['paradigm']['formal']['Persian']['affirmative']['present']['progressive'])
    profile = p.profiling('گفت', 'Ɉoft', '\u200c')
    print(profile['paradigm']['formal']['Persian']['affirmative']['present']['progressive'])
    #print(CPVI.API)