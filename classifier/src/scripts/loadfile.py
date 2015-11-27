__author__ = 'Naleen'
import pickle

def loadfile():

    lowerZoneLabels = fileIO.read_label_file('learner/lowerZoneLabels')
    middleZoneLabels = fileIO.read_label_file('learner/middleZoneLabels')
    upperZoneLabels = fileIO.read_label_file('learner/upperZoneLabels')
    classifier_middle = pickle.load(open('learner/ANN_middle'))
    classifier_lower = pickle.load(open('learner/ANN_lower'))
    classifier_upper = pickle.load(open('learner/ANN_upper'))

    return  lowerZoneLabels,middleZoneLabels,upperZoneLabels,classifier_middle,classifier_lower,classifier_upper
