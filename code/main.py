import cal_CloudRadKernel as CRK
import compute_ECS as CE
import organize_jsons as OJ
import cld_fbks_ecs_assessment_v3 as dataviz
import os
import cases_lookup as CL
import pickle
import json

# User Input:
#================================================================================================
model = 'E3SM'       
institution = 'LLNL'
variant = 'r1i1p1f1' ### not necessary to be changed generally. 
grid_label = 'gr1'   ### not necessary to be changed generally. 

# Flag to compute ECS
# True: compute ECS using abrupt-4xCO2 run
# False: do not compute, instead rely on ECS value present in the json file (if it exists)
get_ecs = True
#================================================================================================

if get_ecs:
    exps = ['amip','amip-p4K','piControl','abrupt-4xCO2']
else:
    exps = ['amip','amip-p4K']

# generate xmls pointing to the cmorized netcdf files 
os.system('mkdir ../xmls/')
filenames={}
for exp in exps:
    filenames[exp]={}
    if exp=='amip-p4K':
        activity = 'CFMIP'
    else:
        activity = 'CMIP'
    if 'amip' in exp:
        fields = ['tas','rsdscs','rsuscs','wap','clisccp'] # necessary for cloud feedback calcs
    else:
        fields = ['tas', 'rlut', 'rsut', 'rsdt'] # needed for ECS calc
    for field in fields:
        if field=='clisccp':
            table='CFmon'


# you can set version as a tag for different sensitivity experiments. The following casename for 
# control and warming will correspond to your version name. @@@@@ change here..
versions = ['F2010v2rc1c']

newmodels = []
for iversion,version in enumerate(versions):

    newmodels.append(model+'_'+version)

    #continue

    # directionary of your input model data 
    # [you need to run main.py in diag_feedback_e3sm package first with PreProces = True to get all needed data here.]
    path = '/p/lustre2/qin4/diag_feedback_E3SM_postdata'
    
    # set simulation length: (start, end)
    tslice = ("0001-01-01", "0005-12-31")
    
    fields = ['tas','rsdscs','rsuscs','OMEGA','FISCCP1_COSP'] # don't change this. 
    
    
    # generate xmls pointing to the cmorized netcdf files 
    os.system('mkdir ../xmls/')
    
    filenames={}
    for exp in ['amip','amip-p4K']:
        filenames[exp]={}
        if exp=='amip':
            activity = 'CMIP'
            #######  set the control case name @@@@@ change here..
            casename = CL.get_lutable(version,exp)


        else:
            activity = 'CFMIP'
            #######  set the warming case name @@@@@ change here..
            casename = CL.get_lutable(version,exp)
   
        print('casename=',casename)
    
    #================================================================================================
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


    # calculate all feedback components and Klein et al (2013) error metrics:
    fname = '../data/backup_dict_'+version+'.pickle'
    if not os.path.isfile(fname):
        fbk_dict,obsc_fbk_dict,err_dict = CRK.CloudRadKernel(filenames,fields,tslice) 

        # save dict into pickle as a backup
        fout = open(fname,'wb')
        pickle.dump([fbk_dict,obsc_fbk_dict,err_dict],fout)
        fout.close()

    else:
        print('Data is ready for',version)
    

# organize all data into json file for further making figures
for iversion,version in enumerate(versions):

    fin = open('../data/backup_dict_'+version+'.pickle','rb')
    fbk_dict,obsc_fbk_dict,err_dict = pickle.load(fin)
    fin.close()

    # add this model to the pre-existing json file containing other model results: 
    updated_fbk_dict,updated_obsc_fbk_dict = OJ.organize_fbk_jsons(fbk_dict,obsc_fbk_dict,model+'_'+version,variant,flag=iversion)
    updated_err_dict = OJ.organize_err_jsons(err_dict,model+'_'+version,variant,flag=iversion)

    ecs = None
    if get_ecs:
        # calculate ECS and add it to the pre-existing json file containing other models' results:
        ecs = CE.compute_ECS(filenames) 
    updated_ecs_dict = OJ.organize_ecs_jsons(ecs,model,variant)

# plot this model alongside other models and expert assessment:
os.system('mkdir ../figures/'+version+'/')
figdir = '../figures/'+version+'/'
result = dataviz.make_all_figs(updated_fbk_dict,updated_obsc_fbk_dict,updated_err_dict,updated_ecs_dict,newmodels,figdir,onlytest=True)

print('Done!')
