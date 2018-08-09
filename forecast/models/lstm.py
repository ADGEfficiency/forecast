""" an LSTM built in keras """

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam


class ManyOneLSTM(object):
    """
    A many to one LSTM

    i.e. a sequence -> single output

    Note that the output is not a single node - 1D (i.e. shape=(16, ))
    """

    def __init__(
            self,
            input_length,
            layers,
            output_nodes,
            lr=0.001,
            loss='mae',
            batch_size=64
    ):
        #  network structure
        self.input_length = input_length
        self.layers = layers
        self.output_nodes = output_nodes

        #  training
        self.lr = lr
        self.loss = loss
        self.batch_size = batch_size

        self.model = self.build_graph()

    def build_graph(self):
        model = Sequential()

        model.add(LSTM(
            self.layers[0],
            return_sequences=True,
            input_shape=(self.input_length, 1)
        ))

        for layer in self.layers[1:]:
            model.add(LSTM(20))

        model.add(Dense(self.output_nodes))

        opt = Adam(lr=self.lr)
        model.compile(loss='mae', optimizer=opt)
        print(model.summary())

        return model

    def fit(self, x, y, epochs=1):
        return self.model.fit(
            x, y, batch_size=self.batch_size, epochs=epochs)

    def predict(self, x):
        return self.model.predict(x)
