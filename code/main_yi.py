import cal_CloudRadKernel as CRK
import organize_jsons as OJ
import cld_fbks_ecs_assessment_v3 as dataviz
import os
import cases_lookup_yi as CL
import pickle
import json

# User Input:
#================================================================================================
model = 'E3SM'       
institution = 'LLNL'
variant = 'r1i1p1f1' ### not necessary to be changed generally. 
grid_label = 'gr1'   ### not necessary to be changed generally. 

# you can set version as a tag for different sensitivity experiments. The following casename for 
# control and warming will correspond to your version name. @@@@@ change here..
versions = [
#'v1',
#'v2',
#'v2.bk.clubb',
#'v2.bk.clubb.MG',
#'v2.bk.clubb.MG.ZM',
#'v2.bk.clubb.MG.ZM.gust',
#'v2.bk.clubb.MG.ZM.gust.trig',
#'v2.bk.clubb.MG.ZM.gust.trig.gw',
#'F2010-p4Ka.v2.Allv1nml.ipdf.gwenergy',
#'v2.bk.clubb.trig',
#'v1.SSTv1',
#'v2.SSTv2',
'v2ppe.FR',
'v2ppe.NDG',
]

newmodels = []
for iversion,version in enumerate(versions):

    newmodels.append(model+'_'+version)

    #continue

    # directionary of your input model data 
    # [you need to run main.py in diag_feedback_e3sm package first with PreProces = True to get all needed data here.]
    #path = '/p/lustre2/qin4/diag_feedback_E3SM_postdata'
    path = '/compyfs/qiny108/diag_feedback_E3SM_postdata/'
    
    # set simulation length: (start, end)
    #tslice = ("0002-01-01", "0006-12-31")
    if 'NDG' in version:
        tslice = ("2010-01-01", "2011-01-01")
    else:
        tslice = ("2010-01-01", "2018-12-31")
    
    fields = ['tas','rsdscs','rsuscs','OMEGA','FISCCP1_COSP'] # don't change this. 
    
    
    # generate xmls pointing to the cmorized netcdf files 
    os.system('mkdir ../xmls/')
    
    filenames={}
    for exp in ['amip','amip-p4K']:
        filenames[exp]={}
        if exp=='amip':
            activity = 'CMIP'
            #######  set the control case name @@@@@ change here..
            casename,_,_ = CL.get_lutable(version,exp)
        else:
            activity = 'CFMIP'
            #######  set the warming case name @@@@@ change here..
            casename,_,_ = CL.get_lutable(version,exp)
    
        print('casename=',casename)
    
    #================================================================================================
        for field in fields:
            #if field=='clisccp':
            if field=='FISCCP1_COSP':
                table='CFmon'
            else:
                table='Amon'
    
            searchstring = path+'/'+casename+'/'+field+'_*.nc'
            #searchstring = path+'/'+casename+'/'+field+'_*000612.nc' #avoid scanning other NC files not ending with 000612

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


# plot this model alongside other models and expert assessment:
os.system('mkdir ../figures/'+versions[-1]+'/')
figdir = '../figures/'+version+'/'
result = dataviz.make_all_figs(updated_fbk_dict,updated_obsc_fbk_dict,updated_err_dict,newmodels,figdir,onlytest=True)

os.system('mv ../data ../data'+versions[-1])
os.system('cp -rp ../data_bak ../data')


print('Done!')
