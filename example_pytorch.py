import torch
from torch.autograd import Variable
import torch.nn as nn

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
    dropout = 0.4

@ex.automain
def dnn_main(input_dim, output_dim, neurons, dropout, _run):  # Include _run in input for tracking metrics
    # Dummy data
    x_train = torch.randn(1000, input_dim)
    y_train = torch.randn(1000, output_dim)
    x_train, y_train = Variable(x_train), Variable(y_train, requires_grad=False)

    # Initialize model
    net = nn.Sequential(
        nn.Linear(input_dim, neurons),
        nn.BatchNorm1d(neurons),
        nn.ReLU(),
        nn.Dropout(dropout),
        nn.Linear(neurons, output_dim),
    )
    optimizer = torch.optim.Adam(params=net.parameters())
    loss_function = nn.MSELoss(size_average=False)

    # Training
    for epoch in range(100):
        out = net(x_train)
        loss = loss_function(out, y_train)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(epoch, loss.data[0])
        # Monitor training loss
        _run.log_scalar("training.loss", loss.data[0], epoch)
