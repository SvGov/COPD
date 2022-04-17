import os
import shutil
import pydicom
from pydicom import dcmread
import numpy as np


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


def is_int16(series_path):
    dicom_list = os.listdir(series_path)
    # (предполагаем, что в одной папке все изображения одинакового типа,
    # но некоторые файлы могут вызвать ошибку при переводе в массив)

    for dicom in dicom_list:
        dicom_path = os.path.join(series_path, dicom)
        try:
            img = dcmread(dicom_path)
            img_arr = img.pixel_array
            if img_arr.dtype == 'int16':
                return True
            else:
                return False
        except ValueError:
            continue
    return False


def copy_files(path_imgs, path_annot, path_to):
    patient_list = os.listdir(path_imgs)

    # patient - ../Lung_Dx-A0001
    for patient in patient_list:
        patient_num = patient[-5:]  # A0001
        patient_cat = patient_num[0]

        annotation_path = os.path.join(path_annot, patient_num)
        xml_list = os.listdir(annotation_path)

        patient_path = os.path.join(path_imgs, patient)
        date_list = os.listdir(patient_path)
        date_list.sort()

        # date - ../04-04-2007-NA-Chest-07990
        for date in date_list:
            date_path = os.path.join(patient_path, date)
            series_list = os.listdir(date_path)
            series_list.sort()

            # series - ../2.000000-5mm-40805
            for series in series_list:
                series_path = os.path.join(date_path, series)
                # мы пришли в папку с dcm файликами

                # не будем копировать изображения с типом пикселей отличающихся от int16
                if not is_int16(series_path):
                    continue

                dicom_list = os.listdir(series_path)
                dicom_list = list(filter(lambda dcm: dcm[0] == '1', dicom_list))
                dicom_list.sort()

                for dicom in dicom_list:
                    dicom_path = os.path.join(series_path, dicom)

                    # проверить читается ли файл
                    try:
                        img = dcmread(dicom_path)
                        img_arr = img.pixel_array
                    except ValueError:
                        continue

                    dicom_info_num = img.SOPInstanceUID
                    new_name = patient_num + '__' + date[0:10] + '__' + series[0] + '__' + dicom

                    # вычислить новую директорию для файла
                    # те что с аннотациями в Positive_X, те что без в Negative
                    if dicom_info_num + '.xml' in xml_list:
                        new_dir = path_to + '/Positive_' + patient_cat
                        # new_dir =  path_to + '/Positive'
                    else:
                        # в Negative скопируем только из одной папки
                        if date == date_list[0] and series == series_list[0]:
                            new_dir = path_to + '/Negative'
                        else:
                            continue

                    # копируем в новую директорию с новым именем
                    new_path = os.path.join(new_dir, new_name)
                    shutil.copyfile(dicom_path, new_path)


if __name__ == "__main__":
    path_imgs = r"C:\Users\Sveta\COPD\data\Lung-PET-CT-Dx_orig-mini"
    path_annot = r"C:\Users\Sveta\COPD\data\Annotation"
    path_to = "C:/Users/Sveta/COPD/data/lungCancer_CT_new"

    if not os.path.isdir(path_to):
        os.mkdir(path_to)
    os.chdir(path_to)
    os.mkdir("Positive_A")
    os.mkdir("Positive_B")
    os.mkdir("Positive_E")
    os.mkdir("Positive_G")
    os.mkdir("Negative")

    copy_files(path_imgs, path_annot, path_to)

