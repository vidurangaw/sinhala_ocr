
from __future__ import division
__author__ = 'Naleen'





import pickle

import Orange
import src.scripts.fileIO as fileIO
import src.feature_extractor as feature_extractor
import src.scripts.neuralnet as NN
import src.scripts.testing as tst
import matplotlib.pyplot as plt


def tune(zone, start, end, n_mid, reg_fact, max_iter):
    #1-35////////35-41

    data_training= feature_extractor.extractor(zone, 1,30, phase='train')
    data_testing=feature_extractor.extractor(zone, 30,41, phase='train')


    CAarr=[]

    n_mid=20
    max_iter=80
    # reg_fact=30


    # for max_iter in range(1, 200):
    # for n_mid in range(1,100):
    for reg_fact in range(0,500):
        reg_fact=reg_fact/100
        learner=[NN.NeuralNetworkLearner(n_mid=n_mid, reg_fact=reg_fact, max_iter=max_iter, normalize=True, rand=None)]
        cross_val = Orange.evaluation.testing.learn_and_test_on_test_data(learner, data_training,data_testing, preprocessors=(), callback=None, store_classifiers=1, store_examples=False)
        cross_val_data = Orange.evaluation.testing.ExperimentResults(
                    [cross_val.classifier_names[0]], cross_val.class_values,
                    )

        # print cross_val_data
        CAs = Orange.evaluation.scoring.CA(cross_val)
        AUCs = Orange.evaluation.scoring.confusion_matrices(cross_val)

        CAarr.append(CAs[0])
        print "Classification Accuracy: %5.3f" % CAs[0] +"  :  "+str(reg_fact)



    #Cost graph
    plt.title("RegFact - Cost")
    plt.savefig('test/RegFact - Cost.png')
    plt.close()

    #Classification Accuracy Graph
    fig_CA=plt.figure()
    fig_CA.suptitle("RegFact - Classification Accuracy")

    ax2=fig_CA.add_subplot(111)
    ax2.plot(CAarr)
    print CAarr
    fig_CA.savefig('test/RegFact - Classification Accuracy.png')



#iterations vs cost/CA
#reg_fac vs cost/CA
#no of nurons vs cost/CA



tune(zone='upper', start=1, end=41, n_mid=100, reg_fact=1, max_iter=100)
