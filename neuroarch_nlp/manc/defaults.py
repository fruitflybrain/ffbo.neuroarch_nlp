
import json, pathlib

# TODO: Support other valid spellings of terms? e.g. "centre" for "center"
#       The basic spelling correction, with its current parameters,
#       should accept most of these alternate valid spellings.

# using, e.g., ME(R), is not supported, but leaving it here
neuropils = [
    (['ADMN(L)', 'ADMN(R)'], ['anterior dorsal mesothoracic nerve', 'admn']),
    ('ADMN(L)', ['left anterior dorsal mesothoracic nerve',  'left admn',  'admn_l']),
    ('ADMN(R)', ['right anterior dorsal mesothoracic nerve', 'right admn', 'admn_r']),
    (['Ov(L)', 'Ov(R)'], ['ovoid neuropil', 'ov', 'ovoid']),
    ('Ov(L)', ['left ovoid',  'left ovoid neuropil',  'left ov',  'ovoid_l',  'ov_l']),
    ('Ov(R)', ['right ovoid', 'right ovoid neuropil', 'right ov', 'ovoid_r', 'ov_r']),
    ('ANm', ['abdominal neuromeres', 'abdominal neuromere', 'anm']),
    (['AbN1(L)', 'AbN1(R)', 'AbN2(L)', 'AbN2(R)', 'AbN3(L)', 'AbN3(R)', 'AbN4(L)', 'AbN4(R)'], ['abdominal nerve', 'abn']),
    (['AbN1(L)', 'AbN1(R)'], ['first abdominal nerve', 'abn1', 'first abn', '1st abn']),
    ('AbN1(L)', ['left first abdominal nerve',  'left first abn',  'left 1st abn',  'left anb1',  'abn1_l']),
    ('AbN1(R)', ['right first abdominal nerve', 'right first abn', 'right 1st abn', 'right anb1', 'abn1_r']),
    (['AbN2(L)', 'AbN2(R)'], ['second abdominal nerve', 'abn2', 'second abn', '2nd abn']),
    ('AbN2(L)', ['left second abdominal nerve',  'left second abn',  'left 2nd abn',  'left anb2',  'abn2_l']),
    ('AbN2(R)', ['right second abdominal nerve', 'right second abn', 'right 2nd abn', 'right anb2', 'abn2_r']),
    (['AbN3(L)', 'AbN3(R)'], ['third abdominal nerve', 'abn3', 'third abn', '3rd abn']),
    ('AbN3(L)', ['left third abdominal nerve',  'left third abn',  'left 3rd abn',  'left anb3',  'abn3_l']),
    ('AbN3(R)', ['right third abdominal nerve', 'right third abn', 'right 3rd abn', 'right anb3', 'abn3_r']),
    (['AbN4(L)', 'AbN4(R)'], ['fourth abdominal nerve', 'abn4', 'fourth abn', '4th abn']),
    ('AbN4(L)', ['left fourth abdominal nerve',  'left fourth abn',  'left 4th abn',  'left anb4',  'abn4_l']),
    ('AbN4(R)', ['right fourth abdominal nerve', 'right fourth abn', 'right 4th abn', 'right anb4', 'abn4_r']),
    ('AbNT', ['abdominal nerve trunk', 'abnt']),
    ('CV', ['cervical connective', 'cv']),
    (['CvN(L)', 'CvN(R)'], ['cervical nerve', 'cvn']),
    ('CvN(L)', ['left cervical nerve',  'left cvn',  'cvn_l']),
    ('CvN(R)', ['right cervical nerve', 'right cvn', 'cvn_r']),
    (['DMetaN(L)', 'DMetaN(R)'], ['dorsal mesothoracic nerve', 'dmetan']),
    ('DMetaN(L)', ['left dorsal mesothoracic nerve',  'left dmetan',  'dmetan_l']),
    ('DMetaN(R)', ['right dorsal mesothoracic nerve', 'right dmetan', 'dmetan_r']),
    (['DProN(L)', 'DProN(R)'], ['dorsal prothoracic nerve', 'dpron']),
    ('DProN(L)', ['left dorsal prothoracic nerve',  'left dpron',  'dpron_l']),
    ('DProN(R)', ['right dorsal prothoracic nerve', 'right dpron', 'dpron_r']),
    (['GF(L)', 'GF(R)'], ['giant fibers', 'gf']),
    ('GF(L)', ['left giant fibers',  'left gf',  'gf_l']),
    ('GF(R)', ['right giant fibers', 'right gf', 'gf_r']),
    (['HTct(UTct-T3)(L)', 'HTct(UTct-T3)(R)'], ['haltere tectulum', 'htct', 'utct-t3']),
    ('HTct(UTct-T3)(L)', ['left haltere tectulum',  'left htct',  'htct_l', 'left utct-t3',  'left utct_t3',  'utct-t3_l', 'utct_t3_l']),
    ('HTct(UTct-T3)(R)', ['right haltere tectulum', 'right htct', 'htct_r', 'right utct-t3', 'right utct_t3', 'utct-t3_r', 'utct_t3_r']),
    (['LegNP(T1)(L)', 'LegNP(T1)(R)', 'LegNP(T2)(L)', 'LegNP(T2)(R)', 'LegNP(T3)(L)', 'LegNP(T3)(R)'], ['leg neuropil', 'legnp']),
    (['LegNP(T1)(L)', 'LegNP(T1)(R)'], ['leg neuropil t1', 'legnp_t1', 'legnp t1']),
    ('LegNP(T1)(L)', ['left leg neuropil t1',  'left legnp_t1',  'left legnp t1',  'legnp_t1_l']),
    ('LegNP(T1)(R)', ['right leg neuropil t1', 'right legnp_t1', 'right legnp t1', 'legnp_t1_r']),
    (['LegNP(T2)(L)', 'LegNP(T2)(R)'], ['leg neuropil T2', 'legnp_T2', 'legnp t2']),
    ('LegNP(T2)(L)', ['left leg neuropil t2',  'left legnp_t2',  'left legnp t2',  'legnp_t2_l']),
    ('LegNP(T2)(R)', ['right leg neuropil t2', 'right legnp_t2', 'right legnp t2', 'legnp_t2_r']),
    (['LegNP(T3)(L)', 'LegNP(T3)(R)'], ['leg neuropil T3', 'legnp_T3', 'legnp t3']),
    ('LegNP(T3)(L)', ['left leg neuropil t3',  'left legnp_t3',  'left legnp t3',  'legnp_t3_l']),
    ('LegNP(T3)(R)', ['right leg neuropil t3', 'right legnp_t3', 'right legnp t3', 'legnp_t3_r']),
    ('IntTct', ['intermediate tectulum', 'inttct']),
    ('LTct', ['lower tectulum', 'ltct']),
    (['MesoAN(L)', 'MesoAN(R)'], ['mesothoracic accessory nerve', 'mesoan']),
    ('MesoAN(L)', ['left mesothoracic accessory nerve',  'left mesoan',  'mesoan_l']),
    ('MesoAN(R)', ['right mesothoracic accessory nerve', 'right mesoan', 'mesoan_r']),
    (['MesoLN(L)', 'MesoLN(R)'], ['mesothoracic leg nerve', 'mesoln']),
    ('MesoLN(L)', ['left mesothoracic leg nerve',  'left mesoln',  'mesoln_l']),
    ('MesoLN(R)', ['right mesothoracic leg nerve', 'right mesoln', 'mesoln_r']),
    (['MetaLN(L)', 'MetaLN(R)'], ['metathoracic leg nerve', 'metaln']),
    ('MetaLN(L)', ['left metathoracic leg nerve',  'left MetaLN',  'metaln_l']),
    ('MetaLN(R)', ['right metathoracic leg nerve', 'right metaln', 'metaln_r']),
    (['NTct(UTct-T1)(L)', 'NTct(UTct-T1)(R)'], ['neck tectulum', 'ntct', 'utct-t1']),
    ('NTct(UTct-T1)(L)', ['left neck tectulum',  'left ntct',  'left utct-t1',  'ntct_l', 'left utct_t1',  'utct-t1_l', 'utct_t1_l']),
    ('NTct(UTct-T1)(R)', ['right neck tectulum', 'right ntct', 'right utct-t1', 'ntct_r', 'right utct_t1', 'utct-t1_r', 'utct_t1_r']),
    (['PDMN(L)', 'PDMN(R)'], ['posterior dorsal mesothoracic nerve', 'pdmn']),
    ('PDMN(L)', ['left posterior dorsal mesothoracic nerve',  'left pdmn',  'pdmn_l']),
    ('PDMN(R)', ['right posterior dorsal mesothoracic nerve', 'right pdmn', 'pdmn_r']),
    (['PrN(L)', 'PrN(R)'], ['prosternal nerve', 'prn']),
    ('PrN(L)', ['left prosternal nerve',  'left prn',  'prn_l']),
    ('PrN(R)', ['right prosternal nerve', 'right prn', 'prn_r']),
    (['ProCN(L)', 'ProCN(R)'], ['prothoracic chordotonal nerve', 'procn']),
    ('ProCN(L)', ['left prothoracic chordotonal nerve',  'left procn',  'procn_l']),
    ('ProCN(R)', ['right prothoracic chordotonal nerve', 'right procn', 'procn_r']),
    (['ProAN(L)', 'ProAN(R)'], ['prothoracic accessory nerve', 'proan']),
    ('ProAN(L)', ['left prothoracic accessory nerve',  'left proan',  'proan_l']),
    ('ProAN(R)', ['right prothoracic accessory nerve', 'right proan', 'proan_r']),
    (['ProLN(L)', 'ProLN(R)'], ['prothoracic leg nerve', 'proln']),
    ('ProLN(L)', ['left prothoracic leg nerve',  'left proln',  'proln_l']),
    ('ProLN(R)', ['right prothoracic leg nerve', 'right proln', 'proln_r']),
    (['VProN(L)', 'VProN(R)'], ['ventral prothoracic nerve', 'vpron']),
    ('VProN(L)', ['left ventral prothoracic nerve',  'left vpron',  'vpron_l']),
    ('VProN(R)', ['right ventral prothoracic nerve', 'right vpron', 'vpron_r']),
    (['WTct(UTct-T2)(L)', 'WTct(UTct-T2)(R)'], ['wing tectulum', 'wtct', 'utct-t2']),
    ('WTct(UTct-T2)(L)', ['left wing tectulum',  'left wtct',  'left utct-t2',  'wtct_l', 'utct-t2_l', 'left utct_t2',  'utct_t2_l']),
    ('WTct(UTct-T2)(R)', ['right wing tectulum', 'right wtct', 'right utct-t2', 'wtct_r', 'utct-t2_r', 'right utct_t2', 'utct_t2_r']),
    (['mVAC(T1)(L)', 'mVAC(T1)(R)', 'mVAC(T2)(L)', 'mVAC(T2)(R)', 'mVAC(T3)(L)', 'mVAC(T3)(R)'], ['medial ventral association center', 'mvac']),
    (['mVAC(T1)(L)', 'mVAC(T1)(R)'], ['medial ventral association center t1', 'mvac_t1', 'mvac t1']),
    ('mVAC(T1)(L)', ['left medial ventral association center t1',  'left mvac_t1',  'left mvac t1',  'mvac_t1_l']),
    ('mVAC(T1)(R)', ['right medial ventral association center t1', 'right mvac_t1', 'right mvac t1', 'mvac_t1_r']),
    (['mVAC(T2)(L)', 'mVAC(T2)(R)'], ['medial ventral association center t2', 'mvac_t2', 'mvac t2']),
    ('mVAC(T2)(L)', ['left medial ventral association center t2',  'left mvac_t2',  'left mvac t2',  'mvac_t2_l']),
    ('mVAC(T2)(R)', ['right medial ventral association center t2', 'right mvac_t2', 'right mvac t2', 'mvac_t2_r']),
    (['mVAC(T3)(L)', 'mVAC(T3)(R)'], ['medial ventral association center t3', 'mvac_t3', 'mvac t3']),
    ('mVAC(T3)(L)', ['left medial ventral association center t3',  'left mvac_t3',  'left mvac t3',  'mvac_t3_l']),
    ('mVAC(T3)(R)', ['right medial ventral association center t3', 'right mvac_t3', 'right mvac t3', 'mvac_t3_r']),
]

arborization_regions = []

for a, b in arborization_regions:
    for i in range(len(b)):
        b[i] = b[i].lower()

# 'subregion query name': (Class, Instance, Name)
subregions = {}

subregions = {k.lower(): v for k, v in subregions.items()}

path = pathlib.Path(__file__).parent.resolve()
with open('{}/neuron_types.json'.format(path), 'r') as f:
    all_types = json.load(f)

neuron_types = {k.lower().replace('+', ''): "/r(?i){}[^0-9a-zA-Z](.*)".format(k.split('(')[0].replace('+', '\\\+')) for k in all_types}
subtypes = {}
for n in all_types:
    if len(n.split('_')) > 1:
        sub_names = n.split('_')
        if len(sub_names[-1]) == 1:
            name = '_'.join(sub_names[:-1])
            if name not in subtypes:
                subtypes[name] = []
            subtypes[name].append(sub_names[-1])
neuron_types.update({k.lower().replace('+', ''): "/r(?i){}_({})[^0-9a-zA-Z](.*)".format(k.replace('+', '\\\+'), '|'.join(v))  for k, v in subtypes.items()})

neuron_types['all'] = '/r(.*)'

neuron_types.update({'regex{}'.format(i): 'regex{}'.format(i) for i in range(100)})
