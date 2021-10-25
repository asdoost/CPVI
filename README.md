# CPVI (Comprehensive Persian Verb Inflector)

<div dir="rtl">
CPVI تصریف‌گر جامع افعال فارسی است که از مدل مکانیسم دوگانه (dual-route) برای تصریف استفاده می‌کند.
</div>
CPVI (Comprehensive Persian Verb Inflector) is a Persian Verb Inflector. PVI uses Dual Mechanism theory (Words &amp; Rules theory) to inflect Persian verbs.

## Usage

`CPVI` class has only a `profiling`method.

The `profiling` method returns the profile of the verb passed as a argument. The profile consists of these properties:

* lexical aspect (action/state/accomplishment/achievement)(just for irregular verbs)
* regularity (regular/irregular/alternative);
* transitivity (transitive/intransitive);
* present dual (True/False);
* past dual (True/False);
* formal API present stem;
* formal API past stem;
* formal Persian present stem;
* formal Persian past stem;
* informal API present stem;
* informal API past stem;
* informal Persian present stem;
* informal Persian past stem;
* paradigm (inflected forms of the verb)

`profiling` accepts 3 arguments:

* `word`: The Persian form of the word that you want to be inflected as a verb. The main assumption here is that users pass either present stem, past stem, or gerund.
* `API_form`: The API form of the word; it is optional and the default value is an empty string. Non-Persian-API characters raise TypeError.
* `space`: The type of space you want to be placed between inflected words and affixes; it is optional and the default value is ZWNJ (\u200c).

```python
>>> from CPVI import CPVI
>>> profile = CPVI()
>>> profile.profiling(word='آمد', API_form='ʔɒmæd', space='\u200c')
{'lexical aspect': 'accomplishment', 
'regularity': 'irregular', 
'transitivity': 'intransitive', 
'present dual': False, 
'past dual': False, 
'formal API present stem': 'ʔɒ',
'formal API past stem': 'ʔɒmæd',
'formal Persian present stem': 'آ',
'formal Persian past stem': 'آمد',
'informal API present stem': 'ʔɒ',
'informal API past stem': 'ʔumæd',
'informal Persian present stem': 'آ',
'informal Persian past stem': 'اومد',
'paradigm': {
    'formal': {
        'API': {
            'affirmative': {
                'present': {
                    'simple': {
                        's1': 'ʔɒjæm', 
                        's2': 'ʔɒji', 
                        's3': 'ʔɒjæd', 
                        'p1': 'ʔɒjim', 
                        'p2': 'ʔɒjid', 
                        'p3': 'ʔɒjænd'
                        },
                    'continuous': {
                        's1': 'mijɒjæm',
                        's2': 'mijɒji', 
                        's3': 'mijɒjæd',
                        'p1': 'mijɒjim',
                        'p2': 'mijɒjid',
                        'p3': 'mijɒjænd'
                        },
                    'subjunctive': {...},
                    'progressive': {...},
                    'perfect': {...}, 
                    'perfect past': {...}, 
                    'imperative': {...}
                    }, 
                'past': {
                    'simple': {...},
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': {...}, 
                    'perfect': {...}, 
                    'perfect subjunctive': {...}
                    },
                'future': {
                    'simple': {...}
                    }
                }, 
            'negative': {
                'present': {
                    'simple': {...}, 
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': None, 
                    'perfect': {...},
                    'perfect past': {...}, 
                    'imperative': {...}
                    }, 
                'past': {
                    'simple': {...}, 
                    'continuous': {...}, 
                    'subjunctive': {...},
                    'progressive': None, 
                    'perfect': {...},
                    'perfect subjunctive': {...}
                    },
                'future': {
                    'simple': {...}
                    }
                }
            }, 
        'Persian': {
            'affirmative': {
                'present': {
                    'simple': {...}, 
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': {...}, 
                    'perfect': {...}, 
                    'perfect past': {...}, 
                    'imperative': {...}}, 
                'past': {
                    'simple': {...},
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': {...},
                    'perfect': {...},
                    'perfect subjunctive': {...}
                    },
                'future': {
                    'simple': {...}
                    }
                },
            'negative': {
                'present': {
                    'simple': {...},
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': None,
                    'perfect': {...}, 
                    'perfect past': {...}, 
                    'imperative': {...}
                    }, 
                'past': {
                    'simple': {...}, 
                    'continuous': {...}, 
                    'subjunctive': {...}, 
                    'progressive': None, 
                    'perfect': {...}, 
                    'perfect subjunctive': {...}
                    },
                'future': {
                    'simple': {...}
                    }
                }
            }
        },
    'informal': {...}
    }

```

`profiling` returns a nested dictionary. The `paradigm` key is a nested hierarchical dictionary containing all the inflected forms. The hierarchy consists of 6 layers. Use the hierarchy to navigate through the dictionary.

* The first layer is formality which is either `formal` or `informal`.
* The second layer is the type of alphabet which is either `Persian` or `API`.
* The third layer is polarity which is either `affirmative` or `negative`.
* The fourth layer is tense which is either `past`, `present`, or `future`.
* The fifth layer for past tense is either `simple`, `continuous`, `subjunctive`, `progressive`, `perfect`, or `perfect subjunctive`.
The fifth layer for present tense is either `simple`, `continuous`, `subjunctive`, `progressive`, `perfect`, `perfect past`, or `imperative`.
The fifth layer for future tense is just `simple`.
* The sixth layer is Person and number which is either `s1`, `s2`, `s3`, `p1`, `p2`, or `p3`.

```python
>>> p = CPVI()
>>> profile = p.profiling('گفت', 'Ɉoft', '\u200c')
# navigate to informal inflections
>>> profile['paradigm']['informal']
{'API': {
    'affirmative': {
        'present': {
            'simple':{
                's1'
                ...
                ...
                ...

# navigate to informal Persian alphabet inflections
>>> profile['paradigm']['informal']['Persian']
{'affirmative': {
    'present': {
        'simple':{
            's1'
            ...
            ...
            ...

# navigate to informal Persian negative inflections
>>> profile['paradigm']['informal']['Persian']['negative']
{'present': {
    'simple':{
        's1'
        ...
        ...
        ...

# navigate to informal Persian negative present inflections
>>> profile['paradigm']['informal']['Persian']['negative']['present']
{'simple':{
    's1'
    ...
    ...
    ...

# navigate to informal Persian negative simple present inflections
>>> profile['paradigm']['informal']['Persian']['negative']['present']['simple']
{'s1': 'نگم', 
's2': 'نگی', 
's3': 'نگه', 
'p1': 'نگیم', 
'p2': ['نگین', 'نگید'], 
'p3': 'نگن'}

# navigate to the plural second person of informal Persian negative simple presents inflections
>>> profile['paradigm']['informal']['Persian']['negative']['present']['simple']['p2']
['نگین', 'نگید']
```

Because of the gramatical restrictions, some inflectional paradigms do not have inflected form, as demonstrated in the following code:

```python
>>> profile['paradigm']['informal']['Persian']['negative']['past']['progressive']
None
```

In dual verbs, each paradigm has two set of inflected forms enclosed in a list, as demonstrated in the following:

```python
>>> p = CPVI()
>>> profile = p.profiling('گسل', 'Ɉosæl', '\u200c')
>>> profile['paradigm']['informal']['Persian']['affirmative']['past']['simple']
[
    {
    's1': 'گسستم', 
    's2': 'گسستی', 
    's3': ['گسست', 'گسستش'], 
    'p1': 'گسستیم', 
    'p2': ['گسستین', 'گسستید'], 
    'p3': 'گسستن'
    }, 
    {
    's1': 'گسیختم', 
    's2': 'گسیختی', 
    's3': ['گسیخت', 'گسیختش'], 
    'p1': 'گسیختیم', 
    'p2': ['گسیختین', 'گسیختید'], 
    'p3': 'گسیختن'
    }
]
```

The `API_form` argument only accepts Persian API alphabet. If you are not familiar with API alphabet, use `CPVI.API` to see the mapping between API and Persian alphabet:

```python
>>> CPVI.API
{
    'b': 'ب', 
    'p': 'پ', 
    'f': 'ف', 
    'v': 'و', 
    't': ['ت', 'ط'], 
    'd': 'د', 
    's': ['س', 'ص', 'ث'], 
    'z': ['ز', 'ض', 'ظ', 'ذ'], 
    'ʃ': 'ش', 
    'ʒ': 'ژ', 
    'ʤ': 'ج', 
    'ʧ': 'چ', 
    'c': 'ک', 
    'Ɉ': 'گ', 
    'x': 'خ', 
    'G': ['ق', 'غ'], 
    'h': ['ه', 'ح'], 
    'ʔ': ['ع', 'همزه'], 
    'm': 'م', 
    'n': 'ن', 
    'r': 'ر', 
    'l': 'ل', 
    'j': 'ی', 
    'ɒ': ['آ', 'ا'], 
    'u': 'او', 
    'i': 'ی', 
    'æ': 'فتحه', 
    'e': 'کسره', 
    'o': 'ضمه'
    }
```

None-API characters raise `TypeError`.

The space between words and affixes could be adjusted by passing either space, ZWNJ (\u200c), or empty string as the `space` argument:

```python
# demostrate ZWNJ as the space argument
>>> p = CPVI()
>>> profile = p.profiling('گفت', 'Ɉoft', '\u200c')
>>> profile['paradigm']['formal']['Persian']['negative']['present']['perfect past']
{
    's1': 'نگفته‌بوده‌ام',
    's2': 'نگفته‌بوده‌ای',
    's3': 'نگفته‌بوده‌است',
    'p1': 'نگفته‌بوده‌ایم',
    'p2': 'نگفته‌بوده‌اید',
    'p3': 'نگفته‌بوده‌اند'
    }

# demostrate space as the space argument
>>> profile = p.profiling('گفت', 'Ɉoft', ' ')
>>> profile['paradigm']['formal']['Persian']['negative']['present']['perfect past']
{
    's1': 'نگفته بوده ام',
    's2': 'نگفته بوده ای',
    's3': 'نگفته بوده است',
    'p1': 'نگفته بوده ایم',
    'p2': 'نگفته بوده اید',
    'p3': 'نگفته بوده اند'
    }

# demostrate empty string as the space argument
>>> profile = p.profiling('گفت', 'Ɉoft', '')
>>> profile['paradigm']['formal']['Persian']['affirmative']['present']['progressive']
{
    's1': 'دارم‌میگویم',
    's2': 'داری‌میگویی',
    's3': 'داردمیگوید',
    'p1': 'داریم‌میگوییم',
    'p2': 'داریدمیگویید',
    'p3': 'دارندمیگویند'
    }
```

Passing strings other than space, ZWNJ (`\u200c`), or empty string raise `ValueError`.
