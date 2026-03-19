import h5py
import numpy as np
import matplotlib.pyplot as plt
from build_hdf5_files import print_structure

file = '\\\\dfs\data\lmcat\inhouse\\20260312\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_1_120326_camera\CV_test_Gr_1_120326_camera_0001\CV_test_Gr_1_120326_camera_0001_with_experimental_data.h5'

#/data/lmcat/inhouse/20260312/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_1_120326_camera/CV_test_Gr_1_120326_camera_0001/CV_test_Gr_1_120326_camera_0001.h5

with h5py.File(file, 'r') as f:
    data = f.get('1.1/instrument/CH4/signal')
    if data is None:
        raise ValueError("Objective error: Dataset '1.1/instrument/CH4/signal' does not exist in the HDF5 file.")
    x = np.asarray(data)

    img = f.get('1.1/measurement/basler')
    print(img.shape)

plt.plot(x)
plt.xlabel('Index')
plt.ylabel('CH4')
plt.show()


#