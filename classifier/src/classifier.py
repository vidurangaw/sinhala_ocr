from __future__ import division

__author__ = 'Naleen'


import pickle
import Orange
import scripts.fileIO as fileIO
import feature_extractor
import scripts.neuralnet as NN
import os

package_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def train(zone, start, end, phase, learner, n_mid, reg_fact, max_iter, normalize,rand ):
    #1-35////////35-41

    data_training= feature_extractor.extractor(zone, start,end, phase)

    if learner == True:

        # learner = Orange.classification.neural.NeuralNetworkLearner(data_training,n_mid=n_mid, reg_fact=reg_fact, max_iter=max_iter, normalize=normalize, rand=rand)
        learner = NN.NeuralNetworkLearner(data_training,n_mid=n_mid, reg_fact=reg_fact, max_iter=max_iter, normalize=normalize, rand=rand)

        fname = os.path.join(package_directory,'learner/ANN_'+zone)
        # with open(fname, 'rb') as file_:
        #     pickle.dump(learner, open(file_)
        with open(fname, 'w') as f:
            pickle.dump(learner, f)  
        # print os.path.realpath(os.path.dirname(__file__))
        # print os.path.abspath(__file__)
        # pickle.dump(learner, open(package_directory+'/learner/ANN_'+zone, 'w'))
#open(os.path.join(package_directory,'learner/ANN_lower'))
    # get the classifier names for later
    cross_val = Orange.evaluation.testing.cross_validation([Orange.classification.neural.NeuralNetworkLearner(n_mid=1, reg_fact=1, max_iter=1, normalize=True, rand=None)], data_training,5)
    cross_val_data = Orange.evaluation.testing.ExperimentResults(
                    [cross_val.classifier_names[0]], cross_val.class_values,
                    )
    # print cross_val_data.classifier_names
    fileIO.write_label_file(cross_val_data.classifier_names, 'learner/'+zone+'ZoneLabels')


    # print "Classification Accuracy: %5.3f" % CAs[0]
    # char= char_map()

    # classifier = pickle.load(open('learner/ANN_'+zone))
    # data_validation = Orange.data.Table('learner/data_'+zone+'.tab')
    # # print data_validation
    # i=1
    # j=1
    # for e in data_validation:
    #      i=i+1
         # print classifier(e, Orange.classification.Classifier.GetBoth)


         # if classifier(e, Orange.classification.Classifier.GetValue)==e.get_class():
         #     j=j+1
             # print e.get_class()



def validate(zone, start, end, phase):
    #1-35////////35-41

    data_validation= feature_extractor.extractor(zone, start,end, phase)
    validation_data = Orange.data.Table(os.path.join(package_directory,'learner/data_'+zone+'.tab'))

    classifier = pickle.load(open(os.path.join(package_directory,'learner/ANN_'+zone)))



    # data_validation = Orange.data.Table('data_'+zone+'_validate.tab')
    i=1
    j=1
    for e in data_validation:
         i=i+1
         # print e
         # print e.get_class()
         # print classifier(e, Orange.classification.Classifier.GetBoth)
         # print classifier(e, Orange.classification.Classifier.GetValue)

         if classifier(e, Orange.classification.Classifier.GetValue)==e.get_class():
             j=j+1
             # print e.get_class()

    print "############"+zone+"############"
    print "Classification Accuracy ("+zone+"):"+str(float(j/i))
    print "i  "+str(i)
    print "j  "+str(j)
    print "################################"

         # return classifier(e, Orange.classification.Classifier.GetValue)

    #

