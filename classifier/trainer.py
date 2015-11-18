__author__ = 'Naleen'

# from src import classifier
# from src.classifier import validate
from src import classifier

def train():
	classifier.train(zone='lower', start=1, end=30, phase='train', learner=True, n_mid=20, reg_fact=2.5, max_iter=60, normalize=True, rand=None)
	classifier.validate(zone='lower', start=30, end=41, phase='validate')

	classifier.train(zone='middle', start=1, end=30, phase='train', learner=True, n_mid=80, reg_fact=6.5, max_iter=40, normalize=True, rand=None)
	classifier.validate(zone='middle', start=30, end=41, phase='validate')

	classifier.train(zone='upper', start=1, end=30, phase='train', learner=True, n_mid=20, reg_fact=3.5, max_iter=80, normalize=True, rand=None)
	classifier.validate(zone='upper', start=30, end=41, phase='validate')
# n_mid=100, reg_fact=1, max_iter=1000, normalize=True, rand=None)
#
# train(zone='lower', start=1, end=30, phase='train', learner=False)
# validate(zone='lower', start=30, end=41, phase='validate')