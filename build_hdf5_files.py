import h5py
from get_data import get_mask_from_indices, get_total_length
import numpy as np


def create_hybrid_skeleton(template_path, dest_path, source_data_file, scan_number, mask):
    
    # Open all three files at once. Avoid opening/closing files inside loops.
    with h5py.File(template_path, 'r') as template_f, \
         h5py.File(dest_path, 'w') as dest_f, \
         h5py.File(source_data_file, 'r') as source_f:
         
        # 1. Copy root attributes
        for key, val in template_f.attrs.items():
            dest_f.attrs[key] = val

        def copy_item(name, obj):
            
            if isinstance(obj, h5py.Group) and name != '1.1/measurement':  # Skip copying the measurement group as a group
                dst_group = dest_f.require_group(name)
                for key, val in obj.attrs.items():
                    dst_group.attrs[key] = val
                    
            elif isinstance(obj, h5py.Dataset):
               
                rel_path = name[4:]  # Remove the scan prefix (e.g., '2.1/') assuming it's always 4 characters (less than 10 scans)
                
                measurement_path_source = f"{scan_number}.1/{rel_path}"
                raw_data = source_f.get(measurement_path_source)
                
                if  (raw_data is not None) and (raw_data.shape) and ('basler' not in name):
                    
                    masked_data = raw_data[mask] 
                    
                    # Create the dataset WITH the masked data. 
                    dst_dataset = dest_f.create_dataset(
                        name, 
                        data=masked_data,
                        compression=obj.compression
                    )

                    var_name = name.split('/')[-2]

                    dest_f[f'1.1/measurement/{var_name}'] = h5py.SoftLink(f'/{name}')  # Link to measurement group
                    print(f'1.1/measurement/{var_name} linked to {name}')

                else:

                    # It's not in source file, or not a measurement. Create the empty template.
                    dst_dataset = dest_f.create_dataset(
                        name,
                        shape=obj.shape,
                        dtype=obj.dtype,
                        chunks=obj.chunks,
                        compression=obj.compression
                    )
                    
                # Copy attributes for both cases
                for key, val in obj.attrs.items():
                    dst_dataset.attrs[key] = val


        dest_f.require_group('1.1/measurement')
        # 2. Execute the traversal
        template_f.visititems(copy_item)
        
    print(f"Hybrid structure created in {dest_path}")


def print_structure(name, obj):
    print(f"{name} - {type(obj).__name__}")



def link_external_data(master_file_path, link_mapping):
    """
    Populates an HDF5 file with external links to other files.
    
    Parameters:
    master_file_path (str): The file where the links will be created.
    link_mapping (dict): A dictionary where:
        - Key: The internal path in the master file (e.g., 'group1/my_data')
        - Value: A tuple of (source_file_path, source_internal_path)
    """
    with h5py.File(master_file_path, 'a') as master:
        for master_path, (src_file, src_path) in link_mapping.items():
            
            # Objectively necessary: You cannot overwrite an existing dataset with a link.
            # It must be deleted first if it exists.
            if master_path in master:
                del master[master_path]
            
            # Create the external link
            master[master_path] = h5py.ExternalLink(src_file, src_path)

        master['1.1/measurement/basler'] = h5py.SoftLink('/1.1/instrument/basler/image')
            
    print("External links successfully established.")


def main():

    template_file = '\\\\dfs\data\lmcat\inhouse\\20260316\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_3_170326_camera\CV_test_Gr_3_170326_camera_0001\CV_test_Gr_3_170326_camera_0001.h5'
    #/data/lmcat/inhouse/20260316/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_3_170326_camera/CV_test_Gr_3_170326_camera_0001/CV_test_Gr_3_170326_camera_0001.h5

    source_exp_data_file='\\\\dfs\data\lmcat\inhouse\\20260309\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_2_160326\CV_test_Gr_2_160326_0001\CV_test_Gr_2_160326_0001.h5'
    source_scan_number='2'

    #FileDir='/data/lmcat/inhouse/20260309/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_1_120326/CV_test_Gr_1_120326_0002/' #This is for Friday
    #FileDir='/data/lmcat/inhouse/20260309/ihma818/id10-surf/20260301/RAW_DATA/CV_test_Gr_2_160326/CV_test_Gr_2_160326_0001/' #This is for Monday
    # 'CV_test_Gr_1_120326_0002.h5' for Friday, 'CV_test_Gr_2_160326_0001.h5' for Monday
    # Scan '5' for Friday, '2' for Monday

    source_camera_data_file='\\\\dfs\data\lmcat\inhouse\\20260316\ihma818\id10-surf\\20260301\RAW_DATA\CV_test_Gr_2_160326_camera\CV_test_Gr_2_160326_camera_0001\CV_test_Gr_2_160326_camera_0001.h5'
    source_camera_scan_number='1'



    indices_file='epoch_CV_test_Gr_2_160326_camera_0001_scan_1.dat' # 'epoch_CV_test_Gr_1_120326_camera_0001_scan_8.dat' for Friday, 'epoch_CV_test_Gr_2_160326_camera_0001_scan_1.dat' for Monday

    mask = get_mask_from_indices(indices_file, get_total_length(source_exp_data_file, source_scan_number))

    dest_file = source_camera_data_file.replace('.h5', '_with_experimental_data.h5')

    create_hybrid_skeleton(template_file, dest_file, source_exp_data_file, source_scan_number, mask)

    link_mapping = {
        '1.1/instrument/basler': (source_camera_data_file, f'{source_camera_scan_number}.1/instrument/basler')
    }

    link_external_data(dest_file, link_mapping)


if __name__ == "__main__":
    main()