import os, os.path as op
import sys
from time import time
from ...logme import *
    
def log_system_setup():
    
    uname_cmd = 'uname -a'
    runCmd( uname_cmd, log )
    
    # freesurfer version
    rec_cmd = 'recon-all --version'
    runCmd( rec_cmd, log )
    
    # fsl version
    fsl_cmd = 'flirt -version'
    runCmd( fsl_cmd, log )
    
    # dtk version
    odf_cmd = 'odf_recon -h'
#    runCmd( odf_cmd, log )
    
def create_folders():
    
    paths = [
        gconf.get_nifti(),
        gconf.get_fs(),
        gconf.get_cmp_tracto_mask(),
        gconf.get_cmp_tracto_mask_tob0(),
        gconf.get_cmp_fibers(),  
        gconf.get_log(),
        gconf.get_stats(),
        gconf.get_rawt1(),
        gconf.get_raw_diffusion(),
        gconf.get_cmp_scalars(),
        gconf.get_cmp_matrices(),
        gconf.get_nifti_trafo(),
        gconf.get_diffusion_metadata(),
        gconf.get_nifti_wm_correction(),
        gconf.get_cmp_rawdiff_resampled(),
        gconf.get_cmp_rawdiff_reconout(),
        gconf.get_cffdir(),
        op.join(gconf.get_fs(), 'mri', 'orig')
        ]

    if gconf.registration_mode == 'Nonlinear':
        paths.append(gconf.get_rawt2())

    for p in gconf.parcellation.keys():
        paths.append(op.join(gconf.get_cmp_tracto_mask(), p))
        
    for p in gconf.parcellation.keys():
        paths.append(op.join(gconf.get_cmp_tracto_mask_tob0(), p))

    for p in paths:
        if not op.exists(p):
            try:
                os.makedirs(p)
            except os.error:
                log.info("%s was already existing" % p)
            finally:
                log.info("Created directory %s" % p)
     
def set_env_vars():
    
    os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'
    os.environ['FSF_OUTPUT_FORMAT'] = 'nii.gz'
    
def log_paths():
    
    log.info("CMP path configuration:")

    log.info(gconf.freesurfer_home)
    log.info(gconf.fsl_home)
    log.info(gconf.dtk_home)
    log.info(gconf.dtk_matrices)


def run(conf):
    """ Run the first preprocessing step
    
    Parameters
    ----------
    conf : PipelineConfiguration object
        
    """
    # setting the global configuration variable
    globals()['gconf'] = conf
    globals()['log'] = gconf.get_logger() 
    start = time()
    
    log.info("Preprocessing")
    log.info("=============")

    log_system_setup()
    create_folders()
    set_env_vars()
    log_paths()
    
    log.info("Module took %s seconds to process." % (time()-start))
    
    
