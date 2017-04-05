import os

from _utils import get_list_scans, bruker_read_files
from scan_converter import convert_a_scan


def show_study_structure(pfo_study):
    """
    Print to console the structure of the study.
    :param pfo_study: path to folder study.
    :return: [None] only print to console information.
    """

    if not os.path.isdir(pfo_study):
        raise IOError('Input folder does not exists.')

    print('Study folder structure: ')
    scans_list = list_files(pfo_study)
    print('\n')
    print('List of scans: {}'.format(scans_list))
    pfi_first_scan = os.path.join(pfo_study, scans_list[0])
    acqp = bruker_read_files('acqp', pfi_first_scan)
    print('Version: {}'.format(acqp['ACQ_sw_version'][0]))


def get_info_sj(pfo_study):
    """
    :param pfo_study: path to study folder.
    :return: get the information of the subject as a dictionary.
    """

    if not os.path.isdir(pfo_study):
        raise IOError('Input folder does not exists.')

    return bruker_read_files('subject', pfo_study)


def get_subject_name(pfo_study):
    """
    :param pfo_study: path to study folder.
    :return: name of the subject in the study. See get_subject_id.
    """
    info_sj = get_info_sj(pfo_study)
    return info_sj['SUBJECT_name']


def get_subject_id(pfo_study):
    """
    :param pfo_study: path to study folder.
    :return: id of the subject. See get_subject_name
    """
    info_sj = get_info_sj(pfo_study)
    return info_sj['SUBJECT_id'][0]


def convert_a_study(pfo_study_brukert_input,
                    pfo_study_nifti_output,
                    study_name=None,
                    scans_list=None,
                    list_new_name_each_scan=None,
                    nifti_version=1,
                    qform=2,
                    sform=1,
                    axis_direction=(-1, -1, 1),
                    save_human_readable=True,
                    normalise_b_vectors_if_dwi=True,
                    correct_slope=False,
                    verbose=1
                    ):
    """
    Core method of the module from a study Bruker folder structure to the homologous folder structure containing
     all the scans in nifti format and the additional information as python dictionaries and readable and ordered .txt
     files.
    :param pfo_study_brukert_input: path to folder Bruker study.
    :param pfo_study_nifti_output: path to folder where the converted study will be stored.
    :param study_name: [None] study name, that will be the name of the main output folder with the new structure.
    :param scans_list: [None] scans of the study that will be converted.
        E.g. scans_list=('3', '4')
    If default None, all the study will be converted
    :param list_new_name_each_scan:
    :param list_new_name_each_scan: [None] dictionary of the filename of the nifti images output corresponding to the scan list
        E.g, dict_fin_output={'3':'Patient supine', '4':'Patient prone'}
    :param nifti_version: see convert_a_scan.__doc__
    :param qform:
    :param sform:
    :param axis_direction:
    :param save_human_readable:
    :param normalise_b_vectors_if_dwi:
    :param correct_slope:
    :param verbose: 0 no, 1 yes, 2 yes for debug
    :return: [None]
    """
    if not os.path.isdir(pfo_study_brukert_input):
        raise IOError('Input folder does not exists.')
    if not os.path.isdir(pfo_study_nifti_output):
        raise IOError('Output folder does not exists.')

    if scans_list is None:
        scans_list = get_list_scans(pfo_study_brukert_input)

    if study_name is None:
        study_name = get_subject_name(pfo_study_brukert_input)
    if list_new_name_each_scan is None:
        list_new_name_each_scan = scans_list
    else:
        if not len(scans_list) == len(list_new_name_each_scan):
            msg = 'list_name_each_scan {0} does not have the same amount of scans in the ' \
                  'study: {1}'.format(list_new_name_each_scan, scans_list)
            raise IOError(msg)

    pfo_nifti_study = os.path.join(pfo_study_nifti_output, study_name)
    os.system('mkdir -p {0}'.format(pfo_nifti_study))

    for brukert_scan_name, nifti_scan_name in zip(scans_list, list_new_name_each_scan):

        pfo_scan_bruker = os.path.join(pfo_study_brukert_input, brukert_scan_name)
        pfo_scan_nifti = os.path.join(pfo_nifti_study, nifti_scan_name)

        convert_a_scan(pfo_scan_bruker,
                       pfo_scan_nifti,
                       create_output_folder_if_not_esists=True,
                       fin_output=list_new_name_each_scan,
                       nifti_version=nifti_version,
                       qform=qform,
                       sform=sform,
                       axis_direction=axis_direction,
                       save_human_readable=save_human_readable,
                       normalise_b_vectors_if_dwi=normalise_b_vectors_if_dwi,
                       correct_slope=correct_slope,
                       verbose=verbose
                       )
