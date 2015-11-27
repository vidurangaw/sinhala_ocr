__author__ = 'Naleen'


def lowerzone_mapper(i):
    mapper = False
    label = ''

    if i == 4 or i == 37 or i == 43:
        mapper = True
        label = 'l0'

    if i == 7:
        mapper = True
        label = 'l1'

    if i == 17 or i == 27 or i == 48 or i == 55:
        mapper = True
        label = 'l2'

    if i == 1:
        mapper = True
        label = 'l3'

    if i == 50 or i == 62:
        mapper = True
        label = 'l4'
        
    if i == 51 or i == 63:
        mapper = True
        label = 'l5'

    if i == 52 or i == 58 or i == 61 or i == 64:
        mapper = True
        label = 'l6'
        
    if i == 53 or i == 56 or i == 59:
        mapper = True
        label = 'l7'
        
    if i == 54 or i == 57 or i == 60:
        mapper = True
        label = 'l8'
        
    if i == 2 or i == 39:
        mapper = True
        label = 'l9'

    if i == 106:
        mapper = True
        label = 'l10'

    if i == 107:
        mapper = True
        label = 'l11'

    return mapper, label

