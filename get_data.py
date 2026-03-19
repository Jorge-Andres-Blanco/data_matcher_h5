import numpy as np
import h5py
import matplotlib.pyplot as plt



def get_total_length(file_name, scan_number):

    with h5py.File(file_name, "r") as f:
        dataX = f.get(scan_number+'.1'+'/measurement/epoch')
        total_length = len(np.asarray(dataX))

    return total_length



def get_mask_from_indices(indices_file, total_length):
    
    with open(indices_file, 'r') as f:
        indices = [int(line.strip()) for line in f]
    
    mask = np.zeros(total_length, dtype=bool)
    mask[indices] = True
    
    return mask



def get_data_from_mask(file_name, scan_number, variables, mask):
    
    data_list = []

    with h5py.File(file_name, "r") as f:
        for var in variables:
            
            dataX = f.get(scan_number+'.1'+'/measurement/'+ var)
            
            data_list.append(np.asarray(dataX))
    
    data_array = np.array(data_list)  # Append the data to the array
    
    masked_data = data_array[:, mask]
    
    return masked_data



def main():

    FileDir='\\\\dfs\data\lmcat\inhouse\\20260309\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_2_160326\CV_test_Gr_2_160326_0001\\' # This is for Windows and for Monday
    
    #FileDir='/data/lmcat/inhouse/20260309/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_1_120326/CV_test_Gr_1_120326_0002/' #This is for Friday
    #FileDir='/data/lmcat/inhouse/20260309/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_2_160326/CV_test_Gr_2_160326_0001/' #This is for Monday
    
    FileName='CV_test_Gr_2_160326_0001.h5' # 'CV_test_Gr_1_120326_0002.h5' for Friday, 'CV_test_Gr_2_160326_0001.h5' for Monday
    
    Scan='2' # '5' for Friday, '2' for Monday

    indices_file='epoch_CV_test_Gr_2_160326_camera_0001_scan_1.dat' # 'epoch_CV_test_Gr_1_120326_camera_0001_scan_8.dat' for Friday, 'epoch_CV_test_Gr_2_160326_camera_0001_scan_1.dat' for Monday

    File=FileDir+FileName

    name_X = ['CH4', 'Ar', 'H2', 'Pressure']

    
    total_length = get_total_length(File, Scan)
    mask = get_mask_from_indices(indices_file, total_length)
    masked_data = get_data_from_mask(File, Scan, name_X, mask)

    i = 0

    plt.plot(masked_data[i])
    plt.title('Masked Data Plot')
    plt.xlabel('Index')
    plt.ylabel(f'{name_X[i]}')
    plt.show()


if __name__ == "__main__":
    main()

