import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import *
from scipy.signal import convolve2d
from sklearn.model_selection import train_test_split
import pdb

sub_list = ['subj1', 'subj2', 'subj3', 'subj4', 'subj5', 'subj6', 'subj7', 'subj8', 'subj9']
Y_dat = np.array([0, 1, 0, 1, 0, 1, 0, 1, 1])
X_dat = np.full((9, 1, 32492, 7), np.nan)

for ind_sub, sub in enumerate(sub_list):
    print(f'load {sub}')
    fname_surf = f'/vols/Data/daa/databases/HCP_Q2_FourtyUnrelatedSubjects/{sub}/MNINonLinear/fsaverage_LR32k/{sub}.L.inflated.32k_fs_LR.surf.gii'
    my_surface = nib.load(fname_surf)
    fname_feature = f'/vols/Data/daa/databases/HCP_Q2_FourtyUnrelatedSubjects/{sub}/MNINonLinear/fsaverage_LR32k/{sub}.L.curvature.32k_fs_LR.shape.gii'
    my_feature = nib.load(fname_feature)
    # array of points with x,y,z coordinates
    ps = my_surface.darrays[0].data
    # array of faces with coordinates of vertices that it connects
    ts = my_surface.darrays[1].data
    for ind in np.arange(0, my_surface.darrays[0].data.shape[0]):
        my_dat = np.full(7, np.nan)
        n_ind = np.unique(np.append(np.append(ts[np.where(ts[:, 0] == ind)], ts[np.where(ts[:, 1] == ind)]), ts[np.where(ts[:, 2] == ind)]))
        # featureness
        dat = my_feature.darrays[0].data[n_ind]
        my_dat[0:len(dat)] = dat
        X_dat[ind_sub, 0, ind, :] = my_dat


# chop into train and test
X_train, X_test, y_train, y_test = train_test_split(X_dat, Y_dat, test_size=0.33)
y_train = keras.utils.to_categorical(y_train, 2)
y_test = keras.utils.to_categorical(y_test, 2)

# Neural network
print('build cnn')
model = keras.models.Sequential()
model.add(Conv2D(8, (1, 7), strides=(1, 7), input_shape=(1, 32492, 7), padding='same', data_format='channels_first'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
