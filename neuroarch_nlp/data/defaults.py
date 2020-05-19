# TODO: Support other valid spellings of terms? e.g. "centre" for "center"
#       The basic spelling correction, with its current parameters,
#       should accept most of these alternate valid spellings.
neuropils = [
        (['AL', 'al'],
            ['antennal lobe', 'al']),
        ('AL',
            ['right antennal lobe', 'right al', 'al_r']),
        ('al',
            ['left antennal lobe', 'left al', 'al_l']),
        (['AN', 'an'],
            ['antenna', 'an']),
        ('AN',
            ['right antenna', 'right an', 'an_r']),
        ('an',
            ['left antenna', 'left an', 'an_l']),
        (['LH', 'lh'],
            ['lateral horn', 'lh']),
        ('LH',
            ['right lateral horn', 'right lh', 'lh_r']),
        ('lh',
            ['left lateral horn', 'left lh', 'lh_l']),
        (['MB', 'mb'],
            ['mushroom body', 'mb']),
        ('MB',
            ['right mushroom body', 'right mb', 'mb_r']),
        ('mb',
            ['left mushroom body', 'left mb', 'mb_l']),
         (['AL', 'al', 'LH', 'lh', 'MB', 'mb'],
            ['olfactory']),
        ('SEZ',
            ['right subesophageal zone', 'right sez', 'sez_r']),
        ('sez',
            ['left subesophageal zone', 'left sez', 'sez_l']),
        (['SEZ', 'sez'],['subesophageal zone', 'SEZ', 'sez'])
        ('VNC',
            ['right ventral nerve cord', 'right vnc', 'vnc_r']),
        ('vnc',
            ['left ventral nerve cord', 'left vnc', 'vnc_l']),
        (['VNC', 'vnc'],['ventral nerve cord', 'VNC', 'vnc'])
        ('LON',
            ['right larval optic neuropil', 'right lon', 'lon_r']),
        ('lon',
            ['left larval optic neuropil', 'left lon', 'lon_l']),
        (['LON', 'lon'],['larval optic neuropil', 'LON', 'lon'])
]

arborization_regions = [('M1', ['medulla layer 1', 'm1', 'layer m1']),
                        ('M2', ['medulla layer 2', 'm2', 'layer m2']),
                        ('M3', ['medulla layer 3', 'm3', 'layer m3']),
                        ('M4', ['medulla layer 4', 'm4', 'layer m4']),
                        ('M5', ['medulla layer 5', 'm5', 'layer m5']),
                        ('M6', ['medulla layer 6', 'm6', 'layer m6']),
                        ('M7', ['medulla layer 7', 'm7', 'layer m7']),
                        ('M8', ['medulla layer 8', 'm8', 'layer m8']),
                        ('M9', ['medulla layer 9', 'm9', 'layer m9']),
                        ('M10', ['medulla layer 10', 'm10', 'layer m10'])]

# 'subregion query name': (Class, Instance, Name)
subregions = {
    'alpha lobe': ('Subregion', '', 'aL(R)'),
    'alhpa1 compartment': ('Subregion', '', 'a1(R)'),
    'home cartridge': ('Cartridge','','home'),
    'single cartridge': ('Cartridge','','home'),
    'channel': ('Glomerulus','',''),
    'glomerulus':('Glomerulus','',''),
    'glomerular':('Glomerulus','',''),
    '13a':('Glomerulus','','13a'),
    '1a':('Glomerulus','','1a'),
    '22c':('Glomerulus','','22c'),
    '24a':('Glomerulus','','24a'),
    '30a':('Glomerulus','','30a'),
    '33a':('Glomerulus','','33a'),
    '35a':('Glomerulus','','35a'),
    '42a':('Glomerulus','','42a'),
    '42b':('Glomerulus','','42b'),
    '45a':('Glomerulus','','45a'),
    '45b':('Glomerulus','','45b'),
    '47a':('Glomerulus','','47a'),
    '49a':('Glomerulus','','49a'),
    '59a':('Glomerulus','','59a'),
    '63a':('Glomerulus','','63a'),
    '67b':('Glomerulus','','67b'),
    '74a':('Glomerulus','','74a'),
    '82a':('Glomerulus','','82a'),
    '83a':('Glomerulus','','83a'),
    '85c':('Glomerulus','','85c'),
    '94a':('Glomerulus','','94a'),
    '13a':('Glomerulus','','13a'),
    '1a glomerulus':('Glomerulus','','1a'),
    '22c glomerulus':('Glomerulus','','22c'),
    '24a glomerulus':('Glomerulus','','24a'),
    '30a glomerulus':('Glomerulus','','30a'),
    '33a glomerulus':('Glomerulus','','33a'),
    '35a glomerulus':('Glomerulus','','35a'),
    '42a glomerulus':('Glomerulus','','42a'),
    '42b glomerulus':('Glomerulus','','42b'),
    '45a glomerulus':('Glomerulus','','45a'),
    '45b glomerulus':('Glomerulus','','45b'),
    '47a glomerulus':('Glomerulus','','47a'),
    '49a glomerulus':('Glomerulus','','49a'),
    '59a glomerulus':('Glomerulus','','59a'),
    '63a glomerulus':('Glomerulus','','63a'),
    '67b glomerulus':('Glomerulus','','67b'),
    '74a glomerulus':('Glomerulus','','74a'),
    '82a glomerulus':('Glomerulus','','82a'),
    '83a glomerulus':('Glomerulus','','83a'),
    '85c glomerulus':('Glomerulus','','85c'),
    '94a glomerulus':('Glomerulus','','94a'),
    'glomerulus 1a':('Glomerulus','','1a'),
    'glomerulus 22c':('Glomerulus','','22c'),
    'glomerulus 24a':('Glomerulus','','24a'),
    'glomerulus 30a':('Glomerulus','','30a'),
    'glomerulus 33a':('Glomerulus','','33a'),
    'glomerulus 35a':('Glomerulus','','35a'),
    'glomerulus 42a':('Glomerulus','','42a'),
    'glomerulus 42b':('Glomerulus','','42b'),
    'glomerulus 45a':('Glomerulus','','45a'),
    'glomerulus 45b':('Glomerulus','','45b'),
    'glomerulus 47a':('Glomerulus','','47a'),
    'glomerulus 49a':('Glomerulus','','49a'),
    'glomerulus 59a':('Glomerulus','','59a'),
    'glomerulus 63a':('Glomerulus','','63a'),
    'glomerulus 67b':('Glomerulus','','67b'),
    'glomerulus 74a':('Glomerulus','','74a'),
    'glomerulus 82a':('Glomerulus','','82a'),
    'glomerulus 83a':('Glomerulus','','83a'),
    'glomerulus 85c':('Glomerulus','','85c'),
    'glomerulus 94a':('Glomerulus','','94a'),
    'lateral appendix': ('','Circuit','lateral appendix'),
    'calyx':('','Circuit','Calyx'),
    'intermediate peduncle': ('','Circuit','intermediate peduncle'),
    'lower vertical lobe': ('','Circuit','lower vertical lobe'),
    'upper vertical lobe': ('','Circuit','upper vertical lobe'),
    'intermediate toe': ('','Circuit','intermediate toe'),
    'lower peduncle':('','Circuit','lower peduncle'),
    'shaft': ('','Circuit', 'shaft'),
    'intermediate vertical lobe': ('','Circuit','intermediate vertical lobe'),
    'upper toe': ('','Circuit','upper toe'),
    'lower toe': ('','Circuit','lower toe'),
    'home column': ('','Circuit','home'),
    'column home': ('','Circuit','home'),
    'home': ('','Circuit','home'),
    'column a': ('','Circuit','A'),
    'column b': ('','Circuit','B'),
    'column c': ('','Circuit','C'),
    'column d': ('','Circuit','D'),
    'column e': ('','Circuit','E'),
    'column f': ('','Circuit','F'),
    'column g': ('','Circuit','G'),
    'column h': ('','Circuit','H'),
    'column i': ('','Circuit','I'),
    'column j': ('','Circuit','J'),
    'column k': ('','Circuit','K'),
    'column l': ('','Circuit','L'),
    'column m': ('','Circuit','M'),
    'column n': ('','Circuit','N'),
    'column o': ('','Circuit','O'),
    'column p': ('','Circuit','P'),
    'column q': ('','Circuit','Q'),
    'column s': ('','Circuit','S'),
    'column t': ('','Circuit','T'),
    'column u': ('','Circuit','U'),
    'column v': ('','Circuit','V'),
    'column w': ('','Circuit','W'),
    'column x': ('','Circuit','X'),
    'column y': ('','Circuit','Y'),
    'column z': ('','Circuit','Z'),
    'column 3a': ('','Circuit','3A'),
    'column 3b': ('','Circuit','3B'),
    'column 3c': ('','Circuit','3C'),
    'column 3d': ('','Circuit','3D'),
    'column 3e': ('','Circuit','3E'),
    'column 3f': ('','Circuit','3F'),
    'column 3g': ('','Circuit','3G'),
    'column 3h': ('','Circuit','3H'),
    'column 3i': ('','Circuit','3I'),
    'column 3j': ('','Circuit','3J'),
    'column 3k': ('','Circuit','3K'),
    'column 3l': ('','Circuit','3L'),
    'column 3m': ('','Circuit','3M'),
    'column 3n': ('','Circuit','3N'),
    'column 3o': ('','Circuit','3O'),
    'column 3p': ('','Circuit','3P'),
    'column 3q': ('','Circuit','3Q'),
    'column 3s': ('','Circuit','3S'),
    'column 3t': ('','Circuit','3T'),
    'column 3u': ('','Circuit','3U'),
    'column 3v': ('','Circuit','3V'),
    'column 3w': ('','Circuit','3W'),
    'column 3x': ('','Circuit','3X'),
    'column 3y': ('','Circuit','3Y'),
    'column 3z': ('','Circuit','3Z'),
    'ommatidium home': ('Ommatidium', '', 'home'),
    'ommatidium a': ('Ommatidium', '', 'A'),
    'ommatidium b': ('Ommatidium', '', 'B'),
    'ommatidium c': ('Ommatidium', '', 'C'),
    'ommatidium d': ('Ommatidium', '', 'D'),
    'ommatidium e': ('Ommatidium', '', 'E'),
    'ommatidium f': ('Ommatidium', '', 'F'),
    'ommatidium g': ('Ommatidium', '', 'G'),
    'ommatidium h': ('Ommatidium', '', 'H'),
    'ommatidium i': ('Ommatidium', '', 'I'),
    'ommatidium j': ('Ommatidium', '', 'J'),
    'ommatidium k': ('Ommatidium', '', 'K'),
    'ommatidium l': ('Ommatidium', '', 'L'),
    'ommatidium m': ('Ommatidium', '', 'M'),
    'ommatidium n': ('Ommatidium', '', 'N'),
    'ommatidium o': ('Ommatidium', '', 'O'),
    'ommatidium p': ('Ommatidium', '', 'P'),
    'ommatidium q': ('Ommatidium', '', 'Q'),
    'ommatidium r': ('Ommatidium', '', 'R'),
        'cartridge home': ('Cartridge','','home'),
    'cartridge a': ('Cartridge','','A'),
    'cartridge b': ('Cartridge','','B'),
    'cartridge c': ('Cartridge','','C'),
    'cartridge d': ('Cartridge','','D'),
    'cartridge e': ('Cartridge','','E'),
    'cartridge f': ('Cartridge','','F'),
    'cartridge g': ('Cartridge','','G'),
    'cartridge h': ('Cartridge','','H'),
    'cartridge i': ('Cartridge','','I'),
    'cartridge j': ('Cartridge','','J'),
    'cartridge k': ('Cartridge','','K'),
    'cartridge l': ('Cartridge','','L'),
    'cartridge m': ('Cartridge','','M'),
    'cartridge n': ('Cartridge','','N'),
    'cartridge o': ('Cartridge','','O'),
    'cartridge p': ('Cartridge','','P'),
    'cartridge q': ('Cartridge','','Q'),
    'cartridge s': ('Cartridge','','S'),
    'cartridge t': ('Cartridge','','T'),
    'cartridge u': ('Cartridge','','U'),
    'cartridge v': ('Cartridge','','V'),
    'cartridge w': ('Cartridge','','W'),
    'cartridge x': ('Cartridge','','X'),
    'cartridge y': ('Cartridge','','Y'),
    'cartridge z': ('Cartridge','','Z'),
    'cartridge 3a': ('Cartridge','','3A'),
    'cartridge 3b': ('Cartridge','','3B'),
    'cartridge 3c': ('Cartridge','','3C'),
    'cartridge 3d': ('Cartridge','','3D'),
    'cartridge 3e': ('Cartridge','','3E'),
    'cartridge 3f': ('Cartridge','','3F'),
    'cartridge 3g': ('Cartridge','','3G'),
    'cartridge 3h': ('Cartridge','','3H'),
    'cartridge 3i': ('Cartridge','','3I'),
    'cartridge 3j': ('Cartridge','','3J'),
    'cartridge 3k': ('Cartridge','','3K'),
    'cartridge 3l': ('Cartridge','','3L'),
    'cartridge 3m': ('Cartridge','','3M'),
    'cartridge 3n': ('Cartridge','','3N'),
    'cartridge 3o': ('Cartridge','','3O'),
    'cartridge 3p': ('Cartridge','','3P'),
    'cartridge 3q': ('Cartridge','','3Q'),
    'cartridge 3s': ('Cartridge','','3S'),
    'cartridge 3t': ('Cartridge','','3T'),
    'cartridge 3u': ('Cartridge','','3U'),
    'cartridge 3v': ('Cartridge','','3V'),
    'cartridge 3w': ('Cartridge','','3W'),
    'cartridge 3x': ('Cartridge','','3X'),
    'cartridge 3y': ('Cartridge','','3Y'),
    'cartridge 3z': ('Cartridge','','3Z'),
    'single column': ('Column','','home'),
    'single cartridge': ('Cartridge','','home'),
    'column': ('','Circuit',''),
    'columnar':('','Circuit','')
}

colors_values = {
    'aliceblue': 'f0f8ff',
    'alice blue': 'f0f8ff',
    'antiquewhite': 'faebd7',
    'antique white': 'faebd7',
    'aqua': '00ffff',
    'aquamarine': '7fffd4',
    'aqua marine': '7fffd4',
    'azure': 'f0ffff',
    'beige': 'f5f5dc',
    'bisque': 'ffe4c4',
    'black': '000000',
    'blanchedalmond': 'ffebcd',
    'blanched almond': 'ffebcd',
    'blue': '0000ff',
    'blueviolet': '8a2be2',
    'blue violet': '8a2be2',
    'brown': 'a52a2a',
    'burlywood': 'deb887',
    'burly wood': 'deb887',
    'cadetblue': '5f9ea0',
    'cadet blue': '5f9ea0',
    'chartreuse': '7fff00',
    'chocolate': 'd2691e',
    'coral': 'ff7f50',
    'cornflowerblue': '6495ed',
    'cornflower blue': '6495ed',
    'cornsilk': 'fff8dc',
    'crimson': 'dc143c',
    'cyan': '00ffff',
    'darkblue': '00008b',
    'dark blue': '00008b',
    'darkcyan': '008b8b',
    'dark cyan': '008b8b',
    'darkgoldenrod': 'b8860b',
    'dark golden rod': 'b8860b',
    'darkgray': 'a9a9a9',
    'dark gray': 'a9a9a9',
    'darkgrey': 'a9a9a9',
    'dark grey': 'a9a9a9',
    'darkgreen': '006400',
    'dark green': '006400',
    'darkkhaki': 'bdb76b',
    'dark khaki': 'bdb76b',
    'darkmagenta': '8b008b',
    'dark magenta': '8b008b',
    'darkolivegreen': '556b2f',
    'dark olive green': '556b2f',
    'darkorange': 'ff8c00',
    'dark orange': 'ff8c00',
    'darkorchid': '9932cc',
    'dark orchid': '9932cc',
    'darkred': '8b0000',
    'dark red': '8b0000',
    'darksalmon': 'e9967a',
    'dark salmon': 'e9967a',
    'darkseagreen': '8fbc8f',
    'dark sea green': '8fbc8f',
    'darkslateblue': '483d8b',
    'dark slate blue': '483d8b',
    'darkslategray': '2f4f4f',
    'dark slate gray': '2f4f4f',
    'darkslategrey': '2f4f4f',
    'dark slate grey': '2f4f4f',
    'darkturquoise': '00ced1',
    'dark turquoise': '00ced1',
    'darkviolet': '9400d3',
    'dark violet': '9400d3',
    'deeppink': 'ff1493',
    'deep pink': 'ff1493',
    'deepskyblue': '00bfff',
    'deep sky blue': '00bfff',
    'dimgray': '696969',
    'dim gray': '696969',
    'dimgrey': '696969',
    'dim grey': '696969',
    'dodgerblue': '1e90ff',
    'dodger blue': '1e90ff',
    'firebrick': 'b22222',
    'fire brick': 'b22222',
    'floralwhite': 'fffaf0',
    'floral white': 'fffaf0',
    'forestgreen': '228b22',
    'forest green': '228b22',
    'fuchsia': 'ff00ff',
    'gainsboro': 'dcdcdc',
    'ghostwhite': 'f8f8ff',
    'ghost white': 'f8f8ff',
    'gold': 'ffd700',
    'goldenrod': 'daa520',
    'golden rod': 'daa520',
    'gray': '808080',
    'grey': '808080',
    'green': '008000',
    'greenyellow': 'adff2f',
    'green yellow': 'adff2f',
    'honeydew': 'f0fff0',
    'honey dew': 'f0fff0',
    'hotpink': 'ff69b4',
    'hot pink': 'ff69b4',
    'indianred': 'cd5c5c',
    'indian red': 'cd5c5c',
    'indigo': '4b0082',
    'ivory': 'fffff0',
    'khaki': 'f0e68c',
    'lavender': 'e6e6fa',
    'lavenderblush': 'fff0f5',
    'lavender blush': 'fff0f5',
    'lawngreen': '7cfc00',
    'lawn green': '7cfc00',
    'lemonchiffon': 'fffacd',
    'lemon chiffon': 'fffacd',
    'lightblue': 'add8e6',
    'light blue': 'add8e6',
    'lightcoral': 'f08080',
    'light coral': 'f08080',
    'lightcyan': 'e0ffff',
    'light cyan': 'e0ffff',
    'lightgoldenrodyellow': 'fafad2',
    'light golden rod yellow': 'fafad2',
    'lightgray': 'd3d3d3',
    'light gray': 'd3d3d3',
    'lightgrey': 'd3d3d3',
    'light grey': 'd3d3d3',
    'lightgreen': '90ee90',
    'light green': '90ee90',
    'lightpink': 'ffb6c1',
    'light pink': 'ffb6c1',
    'lightsalmon': 'ffa07a',
    'light salmon': 'ffa07a',
    'lightseagreen': '20b2aa',
    'light sea green': '20b2aa',
    'lightskyblue': '87cefa',
    'light sky blue': '87cefa',
    'lightslategray': '778899',
    'light slate gray': '778899',
    'lightslategrey': '778899',
    'light slate grey': '778899',
    'lightsteelblue': 'b0c4de',
    'light steel blue': 'b0c4de',
    'lightyellow': 'ffffe0',
    'light yellow': 'ffffe0',
    'lime': '00ff00',
    'limegreen': '32cd32',
    'lime green': '32cd32',
    'linen': 'faf0e6',
    'magenta': 'ff00ff',
    'maroon': '800000',
    'mediumaquamarine': '66cdaa',
    'medium aqua marine': '66cdaa',
    'mediumblue': '0000cd',
    'medium blue': '0000cd',
    'mediumorchid': 'ba55d3',
    'medium orchid': 'ba55d3',
    'mediumpurple': '9370db',
    'medium purple': '9370db',
    'mediumseagreen': '3cb371',
    'medium sea green': '3cb371',
    'mediumslateblue': '7b68ee',
    'medium slate blue': '7b68ee',
    'mediumspringgreen': '00fa9a',
    'medium spring green': '00fa9a',
    'mediumturquoise': '48d1cc',
    'medium turquoise': '48d1cc',
    'mediumvioletred': 'c71585',
    'medium violet red': 'c71585',
    'midnightblue': '191970',
    'midnight blue': '191970',
    'mintcream': 'f5fffa',
    'mint cream': 'f5fffa',
    'mistyrose': 'ffe4e1',
    'misty rose': 'ffe4e1',
    'moccasin': 'ffe4b5',
    'navajowhite': 'ffdead',
    'navajo white': 'ffdead',
    'navy': '000080',
    'oldlace': 'fdf5e6',
    'old lace': 'fdf5e6',
    'olive': '808000',
    'olivedrab': '6b8e23',
    'olive drab': '6b8e23',
    'orange': 'ffa500',
    'orangered': 'ff4500',
    'orange red': 'ff4500',
    'orchid': 'da70d6',
    'palegoldenrod': 'eee8aa',
    'pale golden rod': 'eee8aa',
    'palegreen': '98fb98',
    'pale green': '98fb98',
    'paleturquoise': 'afeeee',
    'pale turquoise': 'afeeee',
    'palevioletred': 'db7093',
    'pale violet red': 'db7093',
    'papayawhip': 'ffefd5',
    'papaya whip': 'ffefd5',
    'peachpuff': 'ffdab9',
    'peach puff': 'ffdab9',
    'peru': 'cd853f',
    'pink': 'ffc0cb',
    'plum': 'dda0dd',
    'powderblue': 'b0e0e6',
    'powder blue': 'b0e0e6',
    'purple': '800080',
    'rebeccapurple': '663399',
    'rebecca purple': '663399',
    'red': 'ff0000',
    'rosybrown': 'bc8f8f',
    'rosy brown': 'bc8f8f',
    'royalblue': '4169e1',
    'royal blue': '4169e1',
    'saddlebrown': '8b4513',
    'saddle brown': '8b4513',
    'salmon': 'fa8072',
    'sandybrown': 'f4a460',
    'sandy brown': 'f4a460',
    'seagreen': '2e8b57',
    'sea green': '2e8b57',
    'seashell': 'fff5ee',
    'sea shell': 'fff5ee',
    'sienna': 'a0522d',
    'silver': 'c0c0c0',
    'skyblue': '87ceeb',
    'sky blue': '87ceeb',
    'slateblue': '6a5acd',
    'slate blue': '6a5acd',
    'slategray': '708090',
    'slate gray': '708090',
    'slategrey': '708090',
    'slate grey': '708090',
    'snow': 'fffafa',
    'springgreen': '00ff7f',
    'spring green': '00ff7f',
    'steelblue': '4682b4',
    'steel blue': '4682b4',
    'tan': 'd2b48c',
    'teal': '008080',
    'thistle': 'd8bfd8',
    'tomato': 'ff6347',
    'turquoise': '40e0d0',
    'violet': 'ee82ee',
    'wheat': 'f5deb3',
    'white': 'ffffff',
    'whitesmoke': 'f5f5f5',
    'white smoke': 'f5f5f5',
    'yellow': 'ffff00',
    'yellowgreen': '9acd32',
    'yellow green': '9acd32'
}

# NOTE: This list of transmitters includes adjectives (and neurotransmitter they map to)
#       and nouns. Consider how that impacts its usage in matching queries.
# A mapping of tokens we expect (lower-cased) to their canonical NeuroArch representations.
transmitters = {
    'glutaminergic': 'glutamate',
    'glutamergic':   'glutamate',
    'glutamatergic': 'glutamate',
    'glutamate':     'glutamate',
    'cholinergic':   'acetylcholine',
    'acetylcholine': 'acetylcholine',
    'dopaminergic':  'dopamine',
    'dopamine':      'dopamine',
    'gabaergic':     'GABA',
    'gaba':          'GABA',
    'GABAergic':     'GABA',
    'GABA':          'GABA',
    'serotonergic':  'serotonin',
    'serotonin':     'serotonin',
    'octopaminergic':'octopamine',
    'octopamine':    'octopamine',
    'dan':           'dopamine',
    'dans':           'dopamine',
    'oa':            'octopamine',
    'oan':           'octopamine'
}

query_str = dict(
    OSN =['/rOSN-(.*)', 'OSN'],
    PN =['/rPN-(.*)', 'PN'],
    PR =['/rRh5PR_(.*)', '/rRh6PR_(.*)', 'Photoreceptor'],
    mPN =['/rmPN-(.*)', 'mPN'],
    MBON =['/rMBON-(.*)', 'MBON'],
    KC =['/rKC_(.*)', 'KC'],
    APL =['/rAPL_(.*)', 'APL'],
    pickyLN =['/rpicky-(.*)'],
    choosyLN =['/rchoosy-(.*)'],
    keystoneLN =['/rkeystone(.*)', 'keystone'],
    broadLN =['/rbroad-(.*)'],
    PMN = ['/rPMN_(.*)', 'PMN'],
    CN = ['/r(.*)CN(.*)', 'CN'],
    MB2ON = ['/r(.*)MB2ON(.*)', 'MB2ON'],
    FFN = ['/r(.*)FFN(.*)', 'FFN'],
    FBN = ['/r(.*)FBN(.*)', 'FBN'],
    FAN = ['/r(.*)FAN(.*)', 'FAN'],
    LHN =['/r(.*)LHN(.*)', 'LHN'],
    LHON =['/r(.*)LHON(.*)', 'LHON'],
    Motor=['/rMotor_(.*)', 'Motor'],
    VPN=['.*VPLN|PDF|(.*)LaN(.*)|PVL09|5th-LaN.*', 'VPN'] # visual projection neuron
)
query_str['LN'] = query_str['pickyLN']+query_str['choosyLN']+query_str['broadLN']+query_str['keystoneLN']

neuron_types = {
    'osn':query_str['OSN'],
    'orn':query_str['OSN'],
    'olfactory sensory neurons':query_str['OSN'],
    'olfactory sensory neuron':query_str['OSN'],
    'olfactory receptor neuron':query_str['OSN'],
    'olfactory receptor neurons':query_str['OSN'],
     # 'pn':['PN','mPN'],
    'pn': query_str['PN'] + query_str['mPN'],
    'principal neuron': query_str['PN'] + query_str['mPN'],
    'pns':query_str['PN'] + query_str['mPN'],
    'mpn': query_str['mPN'], 'multipn':query_str['mPN'],'multi-pn':query_str['mPN'],'mpns': query_str['mPN'],
    'ln':query_str['LN'],
    'lns':query_str['LN'],
    'picky ln':query_str['pickyLN'],'picky lns':query_str['pickyLN'],'picky':query_str['pickyLN'],
    'broad ln':query_str['broadLN'],'broad lns':query_str['broadLN'],'broad':query_str['broadLN'],
    'choosy ln':query_str['choosyLN'],'choosy lns':query_str['choosyLN'],'choosy':query_str['choosyLN'],
    'keystone ln':query_str['keystoneLN'],'keystone lns':query_str['keystoneLN'],'keystone':query_str['keystoneLN'],
    'kenyon cells':query_str['KC'],'kc':query_str['KC'],'kenyon':query_str['KC'],'kcs':query_str['KC'],
    'mbon': query_str['MBON'], 'mushroom body output neurons': query_str['MBON'],'mbons':query_str['MBON'],
    'mbin': query_str['MBIN'], 'apl': query_str['APL'], 'apls':query_str['APL'],'mbins':query_str['MBIN'],
    'photoreceptors': query_str['PR'],
    'vpns': query_str['VPN'], 'vpn': query_str['VPN'], 'visual projection': query_str['VPN'],
    'lhn': query_str['LHN'], 'lhns': query_str['LHN'], 'lateral horn neurons': query_str['LHN'],
    'lhon': query_str['LHON'], 'lhons': query_str['LHON'], 'lateral horn output neurons': query_str['LHON'],
    'mb2on': query_str['MB2ON'], 'mb2ons': query_str['MB2ON'], 
    'ffn': query_str['FFN'], 'ffns': query_str['FFN'], 'feedforward neurons': query_str['FFN'],
    'motor': query_str['Motor'], 'motors': query_str['Motor'], 'motor neurons': query_str['Motor'],
    'pmn': query_str['PMN'], 'pmns': query_str['PMN'], 'premotor neurons': query_str['PMN'], 'pre-motor neurons': query_str['PMN'],
    'cn': query_str['CN'], 'cns': query_str['CN'], 'convergence neurons': query_str['CN'],
    'r1': 'R1', 'r2': 'R2', 'r3': 'R3', 'r4': 'R4', 'r5': 'R5', 'r6': 'R6',
    'r7': 'R7', 'r8': 'R8',
    'lamina wide field': ['Lawf1_0','Lawf1_1','Lawf1_2','Lawf2_0','Lawf2_1'],
    'lamina monopolar': ['L1', 'L2', 'L3', 'L4', 'L5'],
    'l1': 'L1', 'l2': 'L2', 'l3': 'L3', 'l4': 'L4', 'l5': 'L5', 'l6': 'L6',
    'm1': 'M1', 'm2': 'M2',
    'lawf1_0': 'Lawf1_0',
    'lawf1_1': 'Lawf1_1',
    'lawf1_2': 'Lawf1_2',
    'lawf2_0': 'Lawf2_0',
    'lawf2_1': 'Lawf2_1',
    'lawf1': ['Lawf1_0','Lawf1_1','Lawf1_2'],
    'lawf2': ['Lawf2_0','Lawf2_1'],
    'lawf': ['Lawf1_0','Lawf1_1','Lawf1_2','Lawf2_0','Lawf2_1'],
    'c2': 'C2', 'c3': 'C3',
    't1': 'T1',
    't2a': 'T2a',
    't2_d_2nd': 'T2_D_2nd',
    't2': ['T2','T2a','T2_D_2nd'],
    't3_out': 'T3_out',
    't3': ['T3','T3_out'],
    't4a_fb_x1': 'T4a_fb_X1',
    't4a_fb_x2': 'T4a_fb_X2',
    't4a_fb': ['T4a_fb','T4a_fb_X1','T4a_fb_X2'],
    't4b_bf_x1': 'T4b_bf_X1',
    't4b_bf_x2': 'T4b_bf_X2',
    't4b_bf': ['T4b_bf','T4b_bf_X1','T4b_bf_X2'],
    't4c_du_x1': 'T4c_du_X1',
    't4c_du_x2': 'T4c_du_X2',
    't4c_du': ['T4c_du','T4c_du_X1','T4c_du_X2'],
    't4d_ud_x1': 'T4d_ud_X1',
    't4d_ud_x2': 'T4d_ud_X2',
    't4d_ud': ['T4d_ud','T4d_ud_X1','T4d_ud_X2'],
    't4a': '/rT4a_?[a-z]*_?(_X)?[0-9]?',
    't4b': '/rT4b_?[a-z]*_?(_X)?[0-9]?',
    't4c': '/rT4c_?[a-z]*_?(_X)?[0-9]?',
    't4d': '/rT4d_?[a-z]*_?(_X)?[0-9]?',
    't4': '/rT4[abcd]_?[a-z]*_?(_X)?[0-9]?',
    'mi': ['Mi1', 'Mi3', 'Mi5', 'Mi6', 'Mi7', 'Mi8', 'Mi9', 'Mi10_like'],
    'mi1': 'Mi1', 'mi3': 'Mi3', 'mi5': 'Mi5',
    'mi6': 'Mi6', 'mi7': 'Mi7', 'mi8': 'Mi8', 'mi9': 'Mi9',
    'mi10_like': 'Mi10_like',
    'mi10': 'Mi10_like',
    'mi2_0': 'Mi2_0',
    'mi2_1': 'Mi2_1',
    'mi2_2': 'Mi2_2',
    'mi2': ['Mi2_0','Mi2_1','Mi2_2'],
    'mi4': 'Mi4',
    'lt7': 'Lt7',
    'dm': '/rDm[0-9]?[xy]?_?[0-9]*(_B_home)?',
    'dm1': '/rDm1_?[0-9]*',
    'dm2': '/rDm2_?[0-9]*',
    'dm3': '/rDm3[xy]?_?[0-9]*',
    'dm4': '/rDm4_?[0-9]*',
    'dm5': '/rDm5_?(like)?_?[0-9]*',
    'dm6': '/rDm6_?[0-9]*',
    'dm7': '/rDm7_?[0-9]*',
    'dm8': '/rDm8(_B_home)?',
    'dm9': '/rDm9_?[0-9]*',
    #'pm1_0': 'Pm1_0',
    #'pm1_1': 'Pm1_1',
    #'pm1_2': 'Pm1_2',
    'pm': '/rPm[0-9]?_?[0-9]*',
    'pm1': '/rPm1_?[0-9]*',
    'pm2': '/rPm2_?[0-9]*',
    'pm3': '/rPm3_?[0-9]*',
    'pm4': '/rPm4_?[0-9]*',
    'pm5': '/rPm5_?[0-9]*',
    'pm6': '/rPm6_?[0-9]*',
    'tm1': 'Tm1', 'tm2': 'Tm2',
    'tm3_ant': 'Tm3a',
    'tm3_post': 'Tm3p',
    'tm3a': 'Tm3a',
    'tm3p': 'Tm3p',
    #'tm3': ['Tm3_ant','Tm3_post'],
    'tm4_ant': 'Tm4_ant',
    'tm4_post': 'Tm4_post',
    'tm4': '/rTm4_?(ant)?(post)?',
    'tm3': '/rTm3[ap]?_?(ant)?(post)?',
    'tm5a': 'Tm5a',
    'tm5b': 'Tm5b',
    'tm5c': '/rTm5c_?[0-9]*(like)?',
    'tm5c_0': 'Tm5c_0',
    'tm5c_1': 'Tm5c_1',
    'tm5c_2': 'Tm5c_2',
    'tm5c_3': 'Tm5c_3',
    'tm5c_like': 'Tm5c_like',
    'tm5': ['Tm5a','Tm5b','Tm5c'],
    'tm6_14': 'Tm6_14',
    'tm6': 'Tm6_14',
    'tm7': 'Tm7',
    'tm8_like': 'Tm8_like',
    'tm8': 'Tm8_like',
    'tm9': 'Tm9', 'tm10': 'Tm10',
    'tm11': 'Tm11', 'tm12': 'Tm12', 'tm13': 'Tm13', 'tm14': 'Tm14', 'tm15': 'Tm15',
    'tm16_like_0': 'Tm16_like_0',
    'tm16_like_1': 'Tm16_like_1',
    'tm16_like_2': 'Tm16_like_2',
    'tm16_like_3': 'Tm16_like_3',
    'tm16_like': ['Tm16_like_0','Tm16_like_1','Tm16_like_2','Tm16_like_3'],
    'tm16': ['Tm16_like_0','Tm16_like_1','Tm16_like_2','Tm16_like_3'],
    'tm17': 'Tm17', 'tm18': 'Tm18', 'tm19': 'Tm19', 'tm20': 'Tm20',
    'tm21': 'Tm21',
    'tm22_like': 'Tm22_like',
    'tm22': 'Tm22_like',
    'tm23': 'Tm23', 'tm24': 'Tm24',
    'tm25_y1': 'Tm25_Y1',
    'tm25': 'Tm25_Y1',
    'tm26': 'Tm26',
    'tm28_tmy9_0': 'Tm28_TmY9_0',
    'tm28_tmy9_1': 'Tm28_TmY9_1',
    'tm28_tmy9_2': 'Tm28_TmY9_2',
    'tm28_tmy9_3': 'Tm28_TmY9_3',
    'tm28_tmy9_4': 'Tm28_TmY9_4',
    'tm28_tmy9': ['Tm28_TmY9_0','Tm28_TmY9_1','Tm28_TmY9_2','Tm28_TmY9_3','Tm28_TmY9_4'],
    'tm28': ['Tm28_TmY9_0','Tm28_TmY9_1','Tm28_TmY9_2','Tm28_TmY9_3','Tm28_TmY9_4'],
    'tmy1': 'TmY1',  'tmy2': 'TmY2', 'tmy3': 'TmY3',
    'tmy4_like_0': 'TmY4_like_0',
    'tmy4_like_1': 'TmY4_like_1',
    'tmy4_like_2': 'TmY4_like_2',
    'tmy4_like_3': 'TmY4_like_3',
    'tmy4_like_4': 'TmY4_like_4',
    'tmy4_like': ['TmY4_like_0','TmY4_like_1','TmY4_like_2','TmY4_like_3','TmY4_like_4'],
    'tmy4': ['TmY4_like_0','TmY4_like_1','TmY4_like_2','TmY4_like_3','TmY4_like_4'],
    'tmy5a_0': 'TmY5a_0',
    'tmy5a': ['TmY5a','TmY5a_0'],
    'tmy5': ['TmY5a','TmY5a_0'],
    'tmy6': 'TmY6',  'tmy7': 'TmY7', 'tmy8': 'TmY8', 'tmy9': 'TmY9',
    'tmy10_like_0': 'TmY10_like_0',
    'tmy10_like_1': 'TmY10_like_1',
    'tmy10_like': ['TmY10_like_0','TmY10_like_1'],
    'tmy10': ['TmY10_like_0','TmY10_like_1'],
    'tmy11': 'TmY11', 'tmy12': 'TmY12',
    'tmy13_like_0': 'TmY13_like_0',
    'tmy13_like_1': 'TmY13_like_1',
    'tmy13_like': ['TmY13_like_0','TmY13_like_1'],
    'tmy13': ['TmY13_like_0','TmY13_like_1'],
    'y3_y6_0': 'Y3_Y6_0',
    'y3_y6_1': 'Y3_Y6_1',
    'y3_y6_2': 'Y3_Y6_2',
    'y3_y6_3': 'Y3_Y6_3',
    'y3_y6_4': 'Y3_Y6_4',
    'y3_y6_5': 'Y3_Y6_5',
    'y3_y6': ['Y3_Y6_0','Y3_Y6_1','Y3_Y6_2','Y3_Y6_3','Y3_Y6_4','Y3_Y6_5'],
    'y3': ['Y3_Y6_0','Y3_Y6_1','Y3_Y6_2','Y3_Y6_3','Y3_Y6_4','Y3_Y6_5'],
    'fru': '/rfru-F-[0-9]+',
    'fruitless': '/rfru-F-[0-9]+',
    'regex': '',
}

localities = {
    'local':         'True',
    'projection':    'False',
    'output':        'False'
}
# TODO: Change any of these?
synapticities = {
    'presynaptic':   'PresynapticTo',
    'postsynaptic':   'PostsynapticTo'
}
ownerinstances = {
#    'columnar':      'Circuit',
#    'column':        'Circuit',
#    'glomerulus':    'Glomerulus'
}
# TODO: Change this.
othermods = {
    'inhibitory':    'inhibitory',
    'excitatory':    'excitatory'
}
