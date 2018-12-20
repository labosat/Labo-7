from setup import setup1, setup2, experiment_setup
from classes import smu2612b, smu2400, Experiment

address1 = 26
address2 = 24

instrument_setup = [setup1(), setup2()]
experiment_setup = experiment_setup()

instruments = [smu2612b(address1), smu2400(address2)]
experiment = Experiment(instruments, instrument_setup, experiment_setup)

experiment.iv_a()