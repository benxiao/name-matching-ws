from keras.models import Sequential
from keras.layers import Dense, Dropout, ZeroPadding1D, LSTM
import numpy as np

def preproc(data):
    result = []
    for name in data:
        row = []
        for c in name.lower():
            entry = [0] * 26
            entry[ord(c) - 97] = 1
            row.append(entry)
        while len(row) < 15:
            entry = [0] * 26
            row.append(entry)
        result.append(row)
    return np.array(result)


class LSTMModel:
    def __init__(self):
        self.model = Sequential()
        self.model.add(ZeroPadding1D(padding=2, input_shape=(15, 26)))
        self.model.add(LSTM(64, return_sequences=False, activation='relu'))
        self.model.add(Dropout(0.4))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(2, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
        self.model.load_weights('lstm_name2sex.h5')

    def predict(self, name):
        x = preproc([name])
        y = self.model.predict(x, batch_size=1)
        return y[0].argmax(), y[0]

    def summary(self):
        return self.model.summary()


if __name__ == '__main__':
    lstm = LSTMModel()
    name = " "
    while name:
        name = input("name: ")
        print(lstm.predict(name))
