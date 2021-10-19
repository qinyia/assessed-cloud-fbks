import cal_CloudRadKernel as CRK
import organize_jsons as OJ
import cld_fbks_ecs_assessment_v3 as dataviz
import os

# User Input:
#================================================================================================
model = 'E3SM'	
institution = 'LLNL'
variant = 'r1i1p1f1'
grid_label = 'gr1'
#version = 'F2010v2rc1c'
version = 'F2010v1'

path = '/p/lustre2/qin4/diag_feedback_E3SM_postdata'
#================================================================================================

fields = ['tas','rsdscs','rsuscs','OMEGA','clisccp']

# generate xmls pointing to the cmorized netcdf files 
os.system('mkdir ../xmls/')

filenames={}
for exp in ['amip','amip-p4K']:
    filenames[exp]={}
    if exp=='amip':
        activity = 'CMIP'
        if version == 'F2010v2rc1c':
            casename = '20210423.v2rc1c.F2010.ne30pg2_oECv3.chrysalis'
        elif version == 'F2010v1':
            casename = '20210101.F2010C5-CMIP6-LR.ne30_oECv3.syrah.1024'
    else:
        activity = 'CFMIP'
        if version == 'F2010v2rc1c':
            casename = '20210423.v2rc1c.F2010plus4K.ne30pg2_oECv3.chrysalis'
        elif version == 'F2010v1':
            casename = '20210101.F2010C5-CMIP6-LR-p4K.ne30_oECv3.syrah.1024'

#    for field in ['tas','rsdscs','rsuscs','wap','clisccp']:
#    for field in ['tas','rsdscs','rsuscs','OMEGA','FISCCP1_COSP']:
    for field in fields:

        #if field=='clisccp':
        if field=='FISCCP1_COSP':
            table='CFmon'
        else:
            table='Amon'

        searchstring = path+'/'+casename+'/'+field+'_*.nc'
        xmlname = '../xmls/'+exp+'.'+model+'.'+field+'.'+version+'.xml'

        if os.path.isfile(xmlname):
            print('========= ',xmlname,' is available now =======================')
        else:
            os.system('cdscan -x '+xmlname+' '+searchstring)

        filenames[exp][field] = xmlname


tslice = ("0001-01-01", "0005-12-31")

# calculate all feedback components and Klein et al (2013) error metrics:
fbk_dict,obsc_fbk_dict,err_dict = CRK.CloudRadKernel(filenames,fields,tslice) 

# add this model to the pre-existing json file containing other model results: 
updated_fbk_dict,updated_obsc_fbk_dict = OJ.organize_fbk_jsons(fbk_dict,obsc_fbk_dict,model+'_'+version,variant)
updated_err_dict = OJ.organize_err_jsons(err_dict,model+'_'+version,variant)

# plot this model alongside other models and expert assessment:
os.system('mkdir ../figures/'+version+'/')
figdir = '../figures/'+version+'/'
result = dataviz.make_all_figs(updated_fbk_dict,updated_obsc_fbk_dict,updated_err_dict,model+'_'+version,figdir)

print('Done!')
