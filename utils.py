import string


def strip(words):
    '''
    name: strip
    parameter: string
    return: input string but without all the punctuations and spaces
    '''
    # strip the punctuation out
    for c in words:
        if c in string.punctuation:
            words = words.replace(c, '')

    # strip the space out
    return words.replace(' ', '')
