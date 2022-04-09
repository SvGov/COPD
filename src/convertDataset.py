import os
import shutil
import pydicom


def load_file_information(filename):
    information = {}
    ds = pydicom.read_file(filename, force=True)
    information['dicom_num'] = ds.SOPInstanceUID
    # information['PatientID'] = ds.PatientID
    # information['PatientName'] = ds.PatientName
    # information['PatientBirthDate'] = ds.PatientBirthDate
    # information['PatientSex'] = ds.PatientSex
    # information['StudyID'] = ds.StudyID
    # information['StudyDate'] = ds.StudyDate
    # information['StudyTime'] = ds.StudyTime
    # information['InstitutionName'] = ds.InstitutionName
    # information['Manufacturer'] = ds.Manufacturer
    # information['NumberOfFrames'] = ds.NumberOfFrames
    return information


def copy_files(path_imgs, path_annot, path_to):
    patient_list = os.listdir(path_imgs)

    # patient - ../Lung_Dx-A0001
    for patient in patient_list:
        patient_num = patient[-5:]  # A0001
        patient_cat = patient_num[0]
        patient_path = os.path.join(path_imgs, patient)
        date_list = os.listdir(patient_path)
        date_list.sort()

        # date - ../04-04-2007-NA-Chest-07990
        date = date_list[0]
        date_path = os.path.join(patient_path, date)
        series_list = os.listdir(date_path)
        series_list.sort()

        # series - ../2.000000-5mm-40805
        series = series_list[0]
        series_path = os.path.join(date_path, series)

        # мы пришли в папку с dcm файликами
        # теперь их нужно скопировать с другим именем
        # те что с аннотациями в Positive_X, те что без в Negative
        dicom_list = os.listdir(series_path)
        dicom_list.sort()

        annotation_path = os.path.join(path_annot, patient_num)
        xml_list = os.listdir(annotation_path)

        for dicom in dicom_list:
            # для каждого файла, проверяем есть ли соответствующая ему аннотация
            dicom_path = os.path.join(series_path, dicom)
            dicom_info_num = load_file_information(dicom_path)['dicom_num']
            if dicom_info_num + '.xml' in xml_list:
                shutil.copyfile(dicom_path, path_to + '/Positive_' + patient_cat + '/' + patient_num + '_' + dicom)
            else:
                shutil.copyfile(dicom_path, path_to + '/Negative/' + patient_num + '_' + dicom)


if __name__ == "__main__":
    path_imgs = r"C:\Users\Sveta\COPD\data\manifest-1608669183333\Lung-PET-CT-Dx"
    path_annot = r"C:\Users\Sveta\COPD\data\Annotation"
    path_to = "C:/Users/Sveta/COPD/data/lungCancer_CT"

    if not os.path.isdir(path_to):
        os.mkdir(path_to)
    os.chdir(path_to)
    os.mkdir("Positive_A")
    os.mkdir("Positive_B")
    os.mkdir("Positive_E")
    os.mkdir("Positive_G")
    os.mkdir("Negative")

    copy_files(path_imgs, path_annot, path_to)

