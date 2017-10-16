from sacred import Experiment
from sacred.observers import MongoObserver

ex = Experiment('My_Experiment')
my_url = 127.0.0.1:27017  # Or <server-static-ip>:<port> if running on server
ex.observers.append(MongoObserver.create(url=my_url,
                                         db_name='my_database'))


@ex.config
def dnn_config():
    input_dim = 100
    output_dim = 20
    neurons = 300
    dropout = 0.4

@ex.automain
def dnn_main(input_dim, output_dim, neurons, dropout, _run):  # Include _run in input for tracking metrics
    x_train, y_train, x_valid, y_valid = load_data()  # Custom function in some other place
    model = dnn_load_model(input_dim, output_dim, neurons, dropout)  # Custom function in some other place
    history = model.fit(x=x_train, y=y_train,
                        verbose=2,
                        validation_data=(x_valid, y_valid))

    # Save validation loss or other metric in sacred
    for idx, loss in enumerate(history.history['val_loss']):
        _run.log_scalar("validation.loss", loss, idx)
