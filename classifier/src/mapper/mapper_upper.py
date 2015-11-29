__author__ = 'Naleen'


def upperzone_mapper(i):
    mapper = False
    label = ''

    if i == 7 or i == 8 or i == 10:
        mapper = True
        label = 'u0'

    if i == 4 or i == 9 or i == 13 or i == 16 or i == 20 or i == 22 or i == 25 or i == 28 or i == 33 or i == 35 or i == 40 or i== 47 or i == 49:
        mapper = True
        label = 'u1'


    if i == 38:
        mapper = True
        label = 'u2'

    if i == 5 or i == 6 or i == 19 or i == 21 or i == 23 or i == 32:
        mapper = True
        label = 'u3'

    if i == 14 or i == 15 or i == 18 or i == 24 or i == 37:
        mapper = True
        label = 'u4'

    if i == 70 or i == 80:
        mapper = True
        label = 'u5'

    if i == 69 or i == 78:
        mapper = True
        label = 'u6'

    if i == 77 or i == 79:
        mapper = True
        label = 'u7'

    if i == 83 or i == 84 or i == 108:
        mapper = True
        label = 'u8'

    if i == 71:
        mapper = True
        label = 'u9'

    if i == 72:
        mapper = True
        label = 'u10'

    if i == 76:
        mapper = True
        label = 'u11'

    if i == 65 or i == 67:
        mapper = True
        label = 'u12'

    if i == 66 or i == 68:
        mapper = True
        label = 'u13'

    if i == 73:
        mapper = True
        label = 'u14'

    if i == 74:
        mapper = True
        label = 'u15'

    if i == 75:
        mapper = True
        label = 'u16'


    return mapper, label

