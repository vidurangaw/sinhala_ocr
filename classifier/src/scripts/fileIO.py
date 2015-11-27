__author__ = 'Naleen'

import pickle
import os

package_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def write_tl_file(dataArray, dataString, fileName):
    file_ = os.path.join(package_directory, fileName)

    print file_
    file = open(file_, "w")
    classAttributes="val\t"
    dataAttributes=""
    for k in range (0, len(dataArray)):
        dataAttributes=dataAttributes+"data"+str(k)+"\t"

    classType="d\t"
    dataType=""
    for k in range (0, len(dataArray)):
        dataType=dataType+"c"+"\t"

    file.write(classAttributes+dataAttributes+"\n"+classType+dataType+"\nclass\n")
    file.write(dataString.encode("UTF-8"))
    file.close()


def write_label_file(LabelList, fileName):
    file_ = os.path.join(package_directory, fileName)
    with open(file_, 'wb') as f:
        pickle.dump(LabelList, f)


def read_label_file(file):
    file_ = os.path.join(package_directory, file)
    with open(file_, 'rb') as f:
        list = pickle.load(f)
        return list
