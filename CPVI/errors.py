
def custom_errors(API, space=''):
    """
    raise TypeError if the characters of API is not Persian API alphabets 
    and ValueError if the space argument is niether space, ZWNJ (\\u200c),
    or empty string

    Parameters
    ----------
    API : str
        a string in Persian API alphabet
    space : str, optional
        either space (" "), ZWNJ (\\u200c), or empty string ("")
    
    Returns
    -------
    TypeError
        if the characters of API is not Persian API alphabets
    ValueError
        if the space argument is niether space, ZWNJ, or empty string
    """
    for letter in API:
        if letter not in 'ɒuiæeobpfvtdszʃʒʤʧcɈxGhʔmnrlj':
            raise TypeError(f'''The letter "{letter}" is not a Persian API letter. 
            Use "CPVI.API" to see the mapping between Persian and API alphabet''')
    if space not in ['', ' ', '\u200c']:
        raise ValueError(f'''The "space" argument could not be a "{space}".
        Use space, \\u200c, or empty string as the space argument''')