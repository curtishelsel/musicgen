from keras import utils, models, layers 
import numpy as np

b = [423, 774, 781, 781, 1069, 664, 32, 689, 692, 116, 108
 ,1160, 797, 149, 564, 510, 90, 564, 751, 90, 564, 90]

b = b[::-1]

k = len(set(b))
p = sorted(set(item for item in b))
n = dict((note, number) for number, note in enumerate(p))

print(k)

data = []
label = []
for i in range(0, len(b) - 11, 1):
    s_in = b[i:i + 11]
    s_out = b[i + 11]
    data.append([n[note] for note in s_in])
    label.append(n[s_out])

print(label)

data = np.reshape(data, (len(data), 11, 1))
data = data / float(k)
print(data.shape)
label = utils.to_categorical(label)
model = models.Sequential()
    
model.add(layers.LSTM(32, input_shape=(data.shape[1],
                data.shape[2]), return_sequences=True))
model.add(layers.Dropout(0.3))
model.add(layers.LSTM(64, return_sequences=True))
model.add(layers.Dropout(0.3))
model.add(layers.LSTM(32))
model.add(layers.Dense(32))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(k))
model.add(layers.Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])
model.fit(data, label, epochs=50)

model.save("a.hd5")
