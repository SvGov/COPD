import os
import random


def delete_random_dicom(path, count_leave):
    files = os.listdir(path)
    count_delete = len(files) - count_leave
    for i in range(count_delete):
        dicom = random.choice(files)
        dicom_path = os.path.join(path, dicom)
        os.remove(dicom_path)
        files.remove(dicom)


if __name__ == "__main__":
    path = r"C:\Users\Sveta\COPD\data\lungCancer_CT\Negative"
    count_leave = 1000
    delete_random_dicom(path, count_leave)
