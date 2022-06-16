def get_lutable(version,exp):
    lu_table = {
    'F2010v2rc1c':[
    '20211208.F2010C5-CMIP6-LR.IC.ne30_oECv3.compy.1080',
    '20211210.F2010C5-CMIP6-LR.IC.p4Ka.ne30_oECv3.compy.1080',
    ],
    }

    if exp == 'amip':
        return lu_table[version][0]
    else:
        return lu_table[version][1]
