import math
from hyperopt import fmin, tpe, hp, space_eval
from hyperopt.mongoexp import MongoTrials

def objective(x):
    from rasa_nlu.training_data import load_data
    from rasa_nlu.config import RasaNLUModelConfig
    from rasa_nlu.utils import read_yaml
    from rasa_nlu.evaluate import run_evaluation
    from rasa_nlu.model import Trainer

    config_yml = """
language: en
pipeline:
- name: "intent_featurizer_count_vectors"
- name: "intent_classifier_tensorflow_embedding"
  "epochs": {}
""".format(x)
    config = read_yaml(config_yml)
    config = RasaNLUModelConfig(config)
    trainer = Trainer(config)
    training_data = load_data('/hyperopt/data/train.md')
    interpreter = trainer.train(training_data)
    evaluation = run_evaluation('/hyperopt/data/test.md', interpreter)
    intent_f1 = evaluation['intent_evaluation']['f1']
    return {'loss': 1-intent_f1, 'status': STATUS_OK }

print("starting process")
space = hp.qloguniform('epochs', 1, 200, 2)
trials = MongoTrials('mongo://mongodb:27017/foo_db/jobs', exp_key='exp3')
best = fmin(objective, space, trials=trials, algo=tpe.suggest, max_evals=100)

print(best)
print(space_eval(space, best))
