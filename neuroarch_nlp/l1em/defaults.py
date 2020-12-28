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
        (['SEZ', 'sez'],
            ['subesophageal zone', 'SEZ', 'sez']),
        ('VNC',
            ['right ventral nerve cord', 'right vnc', 'vnc_r']),
        ('vnc',
            ['left ventral nerve cord', 'left vnc', 'vnc_l']),
        (['VNC', 'vnc'],
            ['ventral nerve cord', 'VNC', 'vnc']),
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


query_str = dict(
    OSN ='/rOSN-(.*)',
    PN ='/rPN-(.*)|mPN-(.*)',
    uPN='/rPN-(.*)',
    PR ='/rRh5PR_(.*)|Rh6PR_(.*)',
    mPN ='/rmPN-(.*)',
    MBON ='/rMBON-(.*)',
    MBIN ='/rMBIN-(.*)',
    DAN ='/rDAN-(.*)',
    OAN ='/rOAN-(.*)',
    KC ='/rKC_(.*)',
    APL ='/rAPL_(.*)',
    pickyLN ='/rpicky-(.*)',
    choosyLN ='/rchoosy-(.*)',
    keystoneLN ='/rkeystone(.*)',
    broadLN ='/rbroad-(.*)',
    PMN = '/rPMN_(.*)',
    CN = '/r(.*)CN(.*)',
    MB2ON = '/r(.*)MB2ON(.*)',
    FFN = '/r(.*)FFN(.*)',
    FBN = '/r(.*)FBN(.*)',
    FAN = '/r(.*)FAN(.*)',
    LHN ='/r(.*)LHN(.*)',
    LHON ='/r(.*)LHON(.*)',
    Motor='/rMotor_(.*)',
    VPN='/r(.*)VPLN|PDF|(.*)LaN(.*)|PVL09|5th-LaN(.*)',
)
query_str['LN'] = '/rpicky-(.*)|choosy-(.*)|keystone(.*)|broad-(.*)'

neuron_types = {
    'osn':query_str['OSN'],
    'orn':query_str['OSN'],
    'olfactory sensory neurons':query_str['OSN'],
    'olfactory sensory neuron':query_str['OSN'],
    'olfactory receptor neuron':query_str['OSN'],
    'olfactory receptor neurons':query_str['OSN'],
     # 'pn':['PN','mPN'],
    'pn': query_str['PN'],
    'principal neuron': query_str['PN'],
    'pns':query_str['PN'],
    'upn': query_str['uPN'],'upns': query_str['uPN'],
    'mpn': query_str['mPN'], 'multipn':query_str['mPN'],'multi-pn':query_str['mPN'],'mpns': query_str['mPN'],
    'ln':query_str['LN'],
    'lns':query_str['LN'],
    'picky ln':query_str['pickyLN'],'picky lns':query_str['pickyLN'],'picky':query_str['pickyLN'],
    'broad ln':query_str['broadLN'],'broad lns':query_str['broadLN'],'broad':query_str['broadLN'],
    'choosy ln':query_str['choosyLN'],'choosy lns':query_str['choosyLN'],'choosy':query_str['choosyLN'],
    'keystone ln':query_str['keystoneLN'],'keystone lns':query_str['keystoneLN'],'keystone':query_str['keystoneLN'],
    'kenyon cells':query_str['KC'],'kc':query_str['KC'],'kenyon':query_str['KC'],'kcs':query_str['KC'],
    'mbon': query_str['MBON'], 'mushroom body output neurons': query_str['MBON'],'mbons':query_str['MBON'],
    'mbin': query_str['MBIN'], 'mbins':query_str['MBIN'],
    'dan': query_str['DAN'], 'dans':query_str['DAN'],
    'oan': query_str['OAN'], 'oans':query_str['OAN'],
    'apl': query_str['APL'], 'apls':query_str['APL'],
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
}

neuron_types.update({'regex{}'.format(i): 'regex{}'.format(i) for i in range(100)})
