# TODO: Support other valid spellings of terms? e.g. "centre" for "center"
#       The basic spelling correction, with its current parameters,
#       should accept most of these alternate valid spellings.
neuropils = [
        (['MED(R)', 'MED(L)'],
            ['medulla', 'med', 'me']),
        ('MED(L)',
            ['left medulla', 'left med', 'left me', 'med_l', 'me_l', 'medulla']),
        ]

arborization_regions = [('MED(L)', ['left medulla', 'left med', 'left me', 'med_l', 'me_l']),
                        (['MED(R)', 'MED(L)'], ['medulla', 'med', 'me']),
                        ('MED-M1(L)', ['medulla stratum 1', 'm1', 'stratum m1']),
                        ('MED-M2(L)', ['medulla stratum 2', 'm2', 'stratum m2']),
                        ('MED-M3(L)', ['medulla stratum 3', 'm3', 'stratum m3']),
                        ('MED-M4(L)', ['medulla stratum 4', 'm4', 'stratum m4']),
                        ('MED-M5(L)', ['medulla stratum 5', 'm5', 'stratum m5']),
                        ('MED-M6(L)', ['medulla stratum 6', 'm6', 'stratum m6']),
                        ('MED-M7(L)', ['medulla stratum 7', 'm7', 'stratum m7']),
                        ('MED-M8(L)', ['medulla stratum 8', 'm8', 'stratum m8']),
                        ('MED-M9(L)', ['medulla stratum 9', 'm9', 'stratum m9']),
                        ('MED-M10(L)', ['medulla stratum 10', 'm10', 'stratum m10'])]

# 'subregion query name': (Class, Instance, Name)
subregions = {
    'm1': ('Subregion', '', 'MED-M1(L)'),
    'left m1': ('Subregion', '', 'MED-M1(L)'),
    'stratum m1': ('Subregion', '', 'MED-M1(L)'),
    'm2': ('Subregion', '', 'MED-M2(L)'),
    'left m2': ('Subregion', '', 'MED-M2(L)'),
    'stratum m2': ('Subregion', '', 'MED-M2(L)'),
    'm3': ('Subregion', '', 'MED-M3(L)'),
    'left m3': ('Subregion', '', 'MED-M3(L)'),
    'stratum m3': ('Subregion', '', 'MED-M3(L)'),
    'm4': ('Subregion', '', 'MED-M4(L)'),
    'left m4': ('Subregion', '', 'MED-M4(L)'),
    'stratum m4': ('Subregion', '', 'MED-M4(L)'),
    'm5': ('Subregion', '', 'MED-M5(L)'),
    'left m5': ('Subregion', '', 'MED-M5(L)'),
    'stratum m5': ('Subregion', '', 'MED-M5(L)'),
    'm6': ('Subregion', '', 'MED-M6(L)'),
    'left m6': ('Subregion', '', 'MED-M6(L)'),
    'stratum m6': ('Subregion', '', 'MED-M6(L)'),
    'm7': ('Subregion', '', 'MED-M7(L)'),
    'left m7': ('Subregion', '', 'MED-M7(L)'),
    'stratum m7': ('Subregion', '', 'MED-M7(L)'),
    'm8': ('Subregion', '', 'MED-M8(L)'),
    'left m8': ('Subregion', '', 'MED-M8(L)'),
    'stratum m8': ('Subregion', '', 'MED-M8(L)'),
    'm9': ('Subregion', '', 'MED-M9(L)'),
    'left m9': ('Subregion', '', 'MED-M9(L)'),
    'stratum m9': ('Subregion', '', 'MED-M9(L)'),
    'm10': ('Subregion', '', 'MED-M10(L)'),
    'left m10': ('Subregion', '', 'MED-M10(L)'),
    'stratum m10': ('Subregion', '', 'MED-M10(L)'),
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

neuron_types = {}
neuron_types.update({'r{}'.format(i): '/rR{}(.*)'.format(i) for i in range(1,9)})
neuron_types.update({'l{}'.format(i): '/rL{}(.*)'.format(i) for i in range(1,6)})
neuron_types['photoreceptors'] = '/rR[1-9](.*)'
neuron_types['lamina_monopolar'] = '/rL[1-5](.*)'
neuron_types.update({'lawf{}'.format(i): '/rLawf{}(.*)'.format(i) for i in range(1,3)})
neuron_types['lamina_wide_field'] = '/rLawf[1-2](.*)'
neuron_types['lawf'] = '/rLawf[1-2](.*)'
neuron_types.update({'c{}'.format(i): '/rC{}(.*)'.format(i) for i in range(2,4)})
neuron_types.update({'t{}'.format(i): '/rT{}(.*)'.format(i) for i in range(1,5)})
neuron_types['t2a'] = '/rT2a(.*)'
neuron_types.update({'t4{}'.format(i): '/rT4{}(.*)'.format(i) for i in ['a', 'b', 'c', 'd']})
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
