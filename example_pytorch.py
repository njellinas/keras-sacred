from sacred import Experiment
from sacred.observers import MongoObserver

ex = Experiment('My_Experiment')
my_url = '127.0.0.1:27017'  # Or <server-static-ip>:<port> if running on server
ex.observers.append(MongoObserver.create(url=my_url,
                                         db_name='my_database'))


@ex.config
def dnn_config():
    input_dim = 100
    output_dim = 20
    neurons = 300
    activation = 'relu'
    dropout = 0.4

@ex.automain
def dnn_main(input_dim, output_dim, neurons, activation, dropout, _run):  # Include _run in input for tracking metrics
    print(input_dim)
