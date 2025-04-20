import config as config

import pygad
import os

if (os.path.exists(config.GA_MODEL_FILE+".pkl") and os.path.isfile(config.GA_MODEL_FILE+".pkl")):
    ga_instance: pygad.GA = pygad.load(config.GA_MODEL_FILE)
    best_solution = ga_instance.last_generation_elitism
    assert best_solution is not None
    print(best_solution)
