#from urllib import request
import os,shutil

def upload_files(path,upload_path,upload_type, files):
    if upload_type == 'upload':
            if os.path.exists(path):    
                shutil.rmtree(path)            
            os.makedirs(upload_path)

        

    uploaded_count=0
    for file in files:
        # Get the file name, __str__ property of the file object returned is the file name
        file_name = str(file)
        with open(os.path.join(upload_path, file_name), 'wb') as f:
            # Block writing large files to prevent stuck
            for chunk in file.chunks(chunk_size=2014):
                f.write(chunk)
        uploaded_count += 1
        f.close()
        
    return uploaded_count