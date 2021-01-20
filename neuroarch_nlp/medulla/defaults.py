# TODO: Support other valid spellings of terms? e.g. "centre" for "center"
#       The basic spelling correction, with its current parameters,
#       should accept most of these alternate valid spellings.
neuropils = [
        ('MED(L)',
            ['left medulla', 'left med', 'left me', 'med_l', 'me_l']),
        ]

arborization_regions = [('MED(L)', ['left medulla', 'left med', 'left me', 'med_l', 'me_l']),
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
}

neuron_types = {}
neuron_types.update({'r{}'.format(i): '/rR{}(.*)'.format(i) for i in range(1,9)})
neuron_types.update({'l{}'.format(i): '/rL{}(.*)'.format(i) for i in range(1,5)})
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
neuron_types['tm5b'] = '/rTm5a-(.*)'
neuron_types['tm5c'] = '/rTm5a-(.*)'
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
