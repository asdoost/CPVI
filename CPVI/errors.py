
def custom_errors(IPA, space=''):
    """
    raise TypeError if the characters of IPA is not Persian IPA alphabets 
    and ValueError if the space argument is niether space, ZWNJ (\\u200c),
    or empty string

    Parameters
    ----------
    IPA : str
        a string in Persian IPA alphabet
    space : str, optional
        either space (" "), ZWNJ (\\u200c), or empty string ("")
    
    Returns
    -------
    TypeError
        if the characters of IPA is not Persian IPA alphabets
    ValueError
        if the space argument is niether space, ZWNJ, or empty string
    """
    for letter in IPA:
        if letter not in 'ɒuiæeobpfvtdszʃʒʤʧcɈxGhʔmnrlj':
            raise TypeError(f'''The letter "{letter}" is not a Persian IPA letter. 
            Use "CPVI.IPA" to see the mapping between Persian and IPA alphabet''')
    if space not in ['', ' ', '\u200c']:
        raise ValueError(f'''The "space" argument could not be a "{space}".
        Use space, \\u200c, or empty string as the space argument''')