import json, pathlib

# TODO: Support other valid spellings of terms? e.g. "centre" for "center"
#       The basic spelling correction, with its current parameters,
#       should accept most of these alternate valid spellings.
neuropils = [
        ('ME(R)',
            ['medulla', 'med', 'me', 'right medulla', 'me_r', 'right med', 'right me']),
        ('LO(R)',
            ['lobula', 'lo', 'right lobula', 'right lo', 'lo_r', 'lob', 'lob_r', 'right_lob']),
        ('LOP(R)',
            ['lobula plate', 'lop', 'right lobula plate', 'lop_r', 'right lop']),
        (['ME(R)', 'LO(R)', 'LOP(R)'],
            ['optic lobe', 'right optic lobe', 'right ol', 'ol', 'ol_r']),
        (['LO(R)', 'LOP(R)'],
            ['lobula complex', 'right lobula complex', 'right lx', 'lx', 'lc', 'lc_r', 'lx_r']),
        ]

arborization_regions = [] 
                        

for a, b in arborization_regions:
    for i in range(len(b)):
        b[i] = b[i].lower()

# 'subregion query name': (Class, Instance, Name)
subregions = {
    'home column': ('','Circuit','Column home'),
    'column home': ('','Circuit','Column home'),
    'home': ('','Circuit','Column home'),
    'column a': ('','Circuit','Column A'),
    'column b': ('','Circuit','Column B'),
    'column c': ('','Circuit','Column C'),
    'column d': ('','Circuit','Column D'),
    'column e': ('','Circuit','Column E'),
    'column f': ('','Circuit','Column F'),
    'column g': ('','Circuit','Column G'),
    'column h': ('','Circuit','Column H'),
    'column i': ('','Circuit','Column I'),
    'column j': ('','Circuit','Column J'),
    'column k': ('','Circuit','Column K'),
    'column l': ('','Circuit','Column L'),
    'column m': ('','Circuit','Column M'),
    'column n': ('','Circuit','Column N'),
    'column o': ('','Circuit','Column O'),
    'column p': ('','Circuit','Column P'),
    'column q': ('','Circuit','Column Q'),
    'column s': ('','Circuit','Column S'),
    'column t': ('','Circuit','Column T'),
    'column u': ('','Circuit','Column U'),
    'column v': ('','Circuit','Column V'),
    'column w': ('','Circuit','Column W'),
    'column x': ('','Circuit','Column X'),
    'column y': ('','Circuit','Column Y'),
    'column z': ('','Circuit','Column Z'),
    'column 3a': ('','Circuit','Column 3A'),
    'column 3b': ('','Circuit','Column 3B'),
    'column 3c': ('','Circuit','Column 3C'),
    'column 3d': ('','Circuit','Column 3D'),
    'column 3e': ('','Circuit','Column 3E'),
    'column 3f': ('','Circuit','Column 3F'),
    'column 3g': ('','Circuit','Column 3G'),
    'column 3h': ('','Circuit','Column 3H'),
    'column 3i': ('','Circuit','Column 3I'),
    'column 3j': ('','Circuit','Column 3J'),
    'column 3k': ('','Circuit','Column 3K'),
    'column 3l': ('','Circuit','Column 3L'),
    'column 3m': ('','Circuit','Column 3M'),
    'column 3n': ('','Circuit','Column 3N'),
    'column 3o': ('','Circuit','Column 3O'),
    'column 3p': ('','Circuit','Column 3P'),
    'column 3q': ('','Circuit','Column 3Q'),
    'column 3s': ('','Circuit','Column 3S'),
    'column 3t': ('','Circuit','Column 3T'),
    'column 3u': ('','Circuit','Column 3U'),
    'column 3v': ('','Circuit','Column 3V'),
    'column 3w': ('','Circuit','Column 3W'),
    'column 3x': ('','Circuit','Column 3X'),
    'column 3y': ('','Circuit','Column 3Y'),
    'column 3z': ('','Circuit','Column 3Z'),
}
subregions.update(
    {'ommatidium {}'.format(i): \
        ('', 'Circuit', 'Ommatidium {}'.format(i)) \
     for i in range(721)})

subregions = {k.lower(): v for k, v in subregions.items()}

path = pathlib.Path(__file__).parent.resolve()
with open('{}/neuron_types.json'.format(path), 'r') as f:
    all_types = json.load(f)

neuron_types = {k.lower().replace('+', ''): "/r(?i){}{}(.*)".format(k.split('(')[0].replace('+', '\\\+'), "[^0-9Y]" if k[-1].isnumeric() else '[^Y]') for k in all_types}

neuron_types.update({'r{}'.format(i): '/r(?i)R{}[^0-9](.*)'.format(i) for i in range(1,9)})
neuron_types.update({'l{}'.format(i): '/r(?i)L{}[^0-9](.*)'.format(i) for i in range(1,6)})
neuron_types['photoreceptors'] = '/rR[1-9](.*)'
neuron_types['lamina monopolar cell'] = '/rL[1-5](.*)'
neuron_types['lmc'] = '/rL[1-5](.*)'
neuron_types.update({'lawf{}'.format(i): '/r(?i)Lawf{}(.*)'.format(i) for i in range(1,3)})
neuron_types['lamina wide field'] = '/r(?i)Lawf[1-2](.*)'
neuron_types['lawf'] = '/r(?i)Lawf[1-2](.*)'
# neuron_types.update({'t4{}'.format(i): '/rT4{}(.*)'.format(i) for i in ['a', 'b', 'c', 'd']})
neuron_types.update({'mi{}'.format(i): '/rMi{}-(.*)'.format(i) for i in range(1,20)})
neuron_types.update({'dm{}'.format(i): '/rDm{}-(.*)'.format(i) for i in range(1,30)})
neuron_types.update({'pm{}'.format(i): '/rPm{}-(.*)'.format(i) for i in range(1,30)})
neuron_types.update({'tm{}'.format(i): '/rTm{}-(.*)'.format(i) for i in range(1,40)})
neuron_types['tm5'] = '/rTm5[abc]-(.*)'
neuron_types['tm5a'] = '/rTm5a-(.*)'
neuron_types['tm5b'] = '/rTm5b-(.*)'
neuron_types['tm5c'] = '/rTm5c-(.*)'
neuron_types['tm3 ant'] = '/rTm3-(.*)-ant'
neuron_types['tm3 post'] = '/rTm3-(.*)-post'
neuron_types['tm3a'] = '/rTm3-(.*)-ant'
neuron_types['tm3p'] = '/rTm3-(.*)-post'
neuron_types['tm4 ant'] = '/rTm4-(.*)-ant'
neuron_types['tm4 post'] = '/rTm4-(.*)-post'
neuron_types['tm4a'] = '/rTm4-(.*)-ant'
neuron_types['tm4p'] = '/rTm4-(.*)-post'
neuron_types.update({'tmy{}'.format(i): '/rTmY{}-(.*)'.format(i) for i in range(1,30)})
neuron_types['y3'] = '/rY3_Y6(.*)'
neuron_types['y6'] = '/rY3_Y6(.*)'
neuron_types['tangential'] = '/rtan-(.*)'
neuron_types['mt'] = '/rMt(.*)'
neuron_types['all'] = '/r(.*)'
neuron_types.update({'regex{}'.format(i): 'regex{}'.format(i) for i in range(100)})

