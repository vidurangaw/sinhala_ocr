
from __future__ import division
__author__ = 'Naleen'





import pickle

import Orange
import src.scripts.fileIO as fileIO
import src.feature_extractor as feature_extractor
import src.scripts.neuralnet as NN
import src.scripts.testing as tst
import matplotlib.pyplot as plt


def tune(zone, start, end, phase, learner, n_mid, reg_fact, max_iter, normalize,rand ):
    #1-35////////35-41

    data_training= feature_extractor.extractor(zone, 1,30, phase)
    data_testing=feature_extractor.extractor(zone, 30,41, phase)
    # learner=[NN.NeuralNetworkLearner(n_mid=100, reg_fact=1, max_iter=100, normalize=True, rand=None)]
    # learner=[Orange.classification.neural.NeuralNetworkLearner(n_mid=200, reg_fact=1, max_iter=250, normalize=True, rand=None)]
    # get the classifier names for later

    # cross_val = Orange.evaluation.testing.learn_and_test_on_test_data(learner, data_training,data_testing, preprocessors=(), callback=None, store_classifiers=1, store_examples=False)
    # # cross_val = tst.learn_and_test_on_test_data(learner, data_training,data_testing, preprocessors=(), callback=None, store_classifiers=True, store_examples=False)
    # cross_val_data = Orange.evaluation.testing.ExperimentResults(
    #                 [cross_val.classifier_names[0]], cross_val.class_values,
    #                 )

    # pickle.dump(learner[0], open('learnertest/ANN_'+zone, 'w'))
    # print cross_val_data.classifier_names

    CAarr=[]
    for n_mid in range(0,10):
        # Orange.tuning.ThresholdLearner(learner=learner, n_mid=n_mid)
        learner=[NN.NeuralNetworkLearner(n_mid=n_mid, reg_fact=1, max_iter=100, normalize=True, rand=None)]
        cross_val = Orange.evaluation.testing.learn_and_test_on_test_data(learner, data_training,data_testing, preprocessors=(), callback=None, store_classifiers=1, store_examples=False)
        cross_val_data = Orange.evaluation.testing.ExperimentResults(
                    [cross_val.classifier_names[0]], cross_val.class_values,
                    )

        # print cross_val_data
        CAs = Orange.evaluation.scoring.CA(cross_val)
        AUCs = Orange.evaluation.scoring.confusion_matrices(cross_val)
        # print  AUCs
        CAarr.append(CAs[0])
        print "Classification Accuracy: %5.3f" % CAs[0] +"  :  "+str(n_mid)



    plt.plot(CAarr)
    print CAarr
    plt.ylabel('some numbers')
    plt.show()
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





tune(zone='lower', start=1, end=41, phase='train', learner=True, n_mid=100, reg_fact=1, max_iter=100, normalize=True, rand=None)
