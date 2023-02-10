import sys
sys.path.append('./code/')
import cal_CloudRadKernel as CRK
import compute_ECS as CE
import organize_jsons as OJ
import cld_fbks_ecs_assessment_v3 as dataviz
import os,stat,glob
import cases_lookup as CL
import pickle
import json

# No need to modify if diagnosing E3SM results
#================================================================================================
model = 'E3SM'       
institution = 'LLNL'
variant = 'r1i1p1f1' ### not necessary to be changed generally. 
grid_label = 'gr1'   ### not necessary to be changed generally. 

# User Input:
#================================================================================================
machine = 'compy'

# where you save your regridded output from diag_feedback_E3SM package. The same as the run_dir
# in main-test.py of diag_feedback_E3SM package
run_dir = '/compyfs/qiny108/colla/'

if machine == 'compy':
    webdir = '/compyfs/www/qiny108/colla/assessed-cloud-fbks/'

# shortname of sensitivity experiments 
versions = [
'v2test', 
]

# set simulation length: (start, end)
tslice = ("0002-01-01", "0003-12-31")

#================================================================================================
# Please don't modify anything below...

newmodels = []
for iversion,version in enumerate(versions):

    newmodels.append(model+'_'+version)

    # directionary of your input model data 
    # [you need to run main.py in diag_feedback_e3sm package first with PreProces = True to get all needed data here.]
    if machine == 'LC':
        path = '/p/lustre2/qin4/diag_feedback_E3SM_postdata/'
    elif machine == 'compy':
        path = run_dir+'diag_feedback_E3SM_postdata/'
    
    fields = ['tas','rsdscs','rsuscs','OMEGA','FISCCP1_COSP'] # don't change this. 
    
    # generate xmls pointing to the cmorized netcdf files 
    os.system('mkdir xmls/')
    
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
    
            searchstring = path+'/'+casename+'/'+field+'_*????01-????12.nc'
            xmlname = 'xmls/'+exp+'.'+model+'.'+field+'.'+version+'.xml'
    
            if os.path.isfile(xmlname):
                print('========= ',xmlname,' is available now =======================')
            else:
                os.system('cdscan -x '+xmlname+' '+searchstring)
    
            filenames[exp][field] = xmlname


    # calculate all feedback components and Klein et al (2013) error metrics:
    fname = 'data/backup_dict_'+version+'.pickle'
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

    fin = open('data/backup_dict_'+version+'.pickle','rb')
    fbk_dict,obsc_fbk_dict,err_dict = pickle.load(fin)
    fin.close()

    # add this model to the pre-existing json file containing other model results: 
    updated_fbk_dict,updated_obsc_fbk_dict = OJ.organize_fbk_jsons(fbk_dict,obsc_fbk_dict,model+'_'+version,variant,flag=iversion)
    updated_err_dict = OJ.organize_err_jsons(err_dict,model+'_'+version,variant,flag=iversion)


# plot this model alongside other models and expert assessment:
if not os.path.isdir('figures/'+versions[-1]+'/'):
    os.system('mkdir figures/'+versions[-1]+'/')
figdir = 'figures/'+versions[-1]+'/'
result = dataviz.make_all_figs(updated_fbk_dict,updated_obsc_fbk_dict,updated_err_dict,newmodels,figdir,onlytest=False)

if not os.path.isdir('data'+versions[-1]):
    os.rename("data", "data"+versions[-1])
    os.system('cp -rp data_bak data')

# copy to webdir
if machine == 'compy':
    try:
        os.makedirs(webdir)
    except:
        print(webdir+' already exists.')

    os.system('cp -rp '+figdir+' '+webdir)

    for name in glob.glob(webdir+versions[-1]+'/*'):
        st = os.stat(name)
        os.chmod(name, st.st_mode | stat.S_IROTH)

print('Done!')
