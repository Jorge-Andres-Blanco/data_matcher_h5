import h5py    # HDF5 support
import numpy as np


File1Dir='\\\\dfs\data\lmcat\inhouse\\20260309\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_2_160326\CV_test_Gr_2_160326_0001\\'
#File1Dir='/data/lmcat/inhouse/20260309/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_2_160326/CV_test_Gr_2_160326_0001/'

File1Name='CV_test_Gr_2_160326_0001.h5'
ScanN1='2'
FileN1=File1Dir+File1Name

# FileN2 has to be camera
File2Dir='\\\\dfs\data\lmcat\inhouse\\20260316\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_2_160326_camera\CV_test_Gr_2_160326_camera_0001\\'
#File2Dir='/data/lmcat/inhouse/20260316/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_2_160326_camera/CV_test_Gr_2_160326_camera_0001/'
File2Name='CV_test_Gr_2_160326_camera_0001.h5'
ScanN2='1'
FileN2=File2Dir+File2Name

name_x= 'epoch'


f1 = h5py.File(FileN1, "r")
dataX1 = f1.get(ScanN1+'.1'+'/measurement/'+name_x)
Epoch1 = np.asarray(dataX1)

f2 = h5py.File(FileN2, "r")
dataX2 = f2.get(ScanN2+'.1'+'/measurement/'+name_x)
Epoch2 = np.asarray(dataX2)

f1.close()
f2.close()

PosArray=[]
for i in range(len(Epoch2)):
	Tcurr=Epoch2[i]
	PosCurr=int(np.where(Tcurr <Epoch1)[0][0])
	PosArray.append(PosCurr)
	


inDataFile=File2Name.split('.h5')[0]
resultfilename='epoch_'+inDataFile +'_scan_'+ScanN2+'.dat'
fout = open(resultfilename, "w")
np.savetxt(fout, PosArray, fmt='%d')
fout.close()



