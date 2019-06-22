import os
from Board import Board
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)


def get_examples(color_, moves):
    features_ = []
    labels_ = []
    for i, unformatted_move in enumerate(moves):
        move = []
        for j in range(0, len(unformatted_move)):
            move.append(float(unformatted_move[j]))
        if color_ == 0:
            if i % 2 == 0:
                features_.append(np.array(move))
            else:
                labels_.append(np.array(move))
        else:
            if i % 2 == 1:
                features_.append(np.array(move))
            else:
                labels_.append(np.array(move))

    if len(features_) > len(labels_):
        features_.pop()


    return np.array(features_), np.array(labels_)


if __name__ == '__main__':
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    color = int(input('Enter 0 to use White and 1 to use Black\n'))
    if color == 0:
        features_file = parent + '/../Parser/vectorized_games/white_games_won/white_games_won.txt'
    else:
        features_file = parent + '/../Parser/vectorized_games/black_games_won/black_games_won.txt'

    NN_model = Sequential()

    # The Input Layer :
    NN_model.add(Dense(256, kernel_initializer='normal', input_dim=256, activation='linear'))

    # The Hidden Layers :
    NN_model.add(Dense(256, kernel_initializer='normal', activation='sigmoid'))
    NN_model.add(Dense(256, kernel_initializer='normal', activation='sigmoid'))
    NN_model.add(Dense(256, kernel_initializer='normal', activation='sigmoid'))

    # The Output Layer :
    NN_model.add(Dense(256, kernel_initializer='normal', activation='hard_sigmoid'))

    # Compile the network :
    NN_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    NN_model.summary()
    checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
    checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
    callbacks_list = [checkpoint]

    with open(features_file, 'r') as f:
        game = f.readline()
        while game:
            squished_moves = game.split(',')
            moves = []
            for squished_move in squished_moves:
                moves.append(Board.convert_compact_string_to_normal(squished_move))

            training_features, training_labels = get_examples(color, moves)
            # Train the network
            NN_model.fit(training_features, training_labels, epochs=50, batch_size=32, validation_split=0.2,
                         callbacks=callbacks_list)
            game = f.readline()

    # serialize model to JSON
    model_json = NN_model.to_json()
    if color == 0:
        with open(parent + "/nn_data/white/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        NN_model.save_weights(parent + "/nn_data/white/model.h5")
    else:
        with open(parent + "/nn_data/black/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        NN_model.save_weights(parent + "/nn_data/black/model.h5")
    print("Saved model to disk")

else:
    exit(-1)
