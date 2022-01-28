
def get_lutable(version,exp):
    lu_table = {
    'F2010-p4Ka.v1':[
    '20211208.F2010C5-CMIP6-LR.IC.ne30_oECv3.compy.1080',
    '20211210.F2010C5-CMIP6-LR.IC.p4Ka.ne30_oECv3.compy.1080',
    ],
    'F2010-p4Ka.v2':[
    '20211208.v2.F2010-CICE.IC.ne30pg2_EC.compy',
    '20211210.v2.F2010-CICE.IC.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb':[
    '20220110.v2.F2010-CICE.IC.back.clubb.ne30pg2_EC.compy',
    '20220110.v2.F2010-CICE.IC.back.clubb.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb.MG':[
    '20220110.v2.F2010-CICE.IC.back.clubb.MG.ne30pg2_EC.compy',
    '20220110.v2.F2010-CICE.IC.back.clubb.MG.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb.MG.ZM':[
    '20220119.v2.F2010-CICE.IC.back.clubb.MG.ZM.ne30pg2_EC.compy',
    '20220119.v2.F2010-CICE.IC.back.clubb.MG.ZM.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb.MG.ZM.gust':[
    '20220119.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.ne30pg2_EC.compy',
    '20220119.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb.MG.ZM.gust.trig':[
    '20220120.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.trig.ne30pg2_EC.compy',
    '20220120.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.trig.p4Ka.ne30pg2_EC.compy',
    ],
    'v2.bk.clubb.MG.ZM.gust.trig.gw':[
    '20220120.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.trig.gw.ne30pg2_EC.compy',
    '20220120.v2.F2010-CICE.IC.back.clubb.MG.ZM.gust.trig.gw.p4Ka.ne30pg2_EC.compy',
    ],
    'F2010-p4Ka.v2.Allv1nml.ipdf.gwenergy':[
    '20211228.v2.F2010-CICE.IC.Allv1nml.ipdf.gwenergy.ne30pg2_EC.compy',
    '20211228.v2.F2010-CICE.IC.Allv1nml.ipdf.gwenergy.p4Ka.ne30pg2_EC.compy',
    ]
    }

    if exp == 'amip':
        return lu_table[version][0]
    else:
        return lu_table[version][1]
