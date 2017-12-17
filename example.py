import numpy as np
from keras.models import Sequential
from keras.layers import InputLayer, Dense, BatchNormalization, Activation, Dropout

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
    neurons = 64
    activation = 'relu'
    dropout = 0.4

@ex.automain
def dnn_main(input_dim, output_dim, neurons, activation, dropout, _run):  # Include _run in input for tracking metrics
    # Dummy data
    x_train = np.random.randn(1000, 100)
    y_train = np.random.randn(1000, 20)
    x_valid = np.random.randn(1000, 100)
    y_valid = np.random.randn(1000, 20)

    # Model architecture
    # Input layer
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, input_dim), name='input'))
    # Hidden layer
    model.add(Dense(units=neurons, name='hidden'))
    model.add(BatchNormalization())
    model.add(Activation(activation=activation))
    model.add(Dropout(rate=dropout))
    # Output layer
    model.add(Dense(units=output_dim, name='output'))
    model.add(BatchNormalization())

    # Compile model
    model.compile(optimizer='Adam',
                  loss='mse')

    # Training and validation
    history = model.fit(x=x_train, y=y_train,
                        batch_size=64,
                        epochs=100,
                        verbose=2,
                        validation_data=(x_valid, y_valid))

    # Save validation loss or other metric in sacred
    for idx, loss in enumerate(history.history['val_loss']):
        _run.log_scalar("validation.loss", loss, idx)
