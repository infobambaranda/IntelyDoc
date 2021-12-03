import os

def show_files(folder_path):
    transfer_files={}
    classified_path=folder_path+'classified'
    not_classified_path=folder_path+'not_classified'
    if not os.path.exists(classified_path) and not os.path.exists(not_classified_path):
        classified = 'False'
    elif not os.path.exists(classified_path):
        classified='no files'
    else:
        classified = 'True'

    for file_path,directory, files in os.walk(folder_path):
        sub_dir_name = os.path.basename(file_path)
        #print(file_path)
        sub_dir_files=[]
        for file in files:
            if '/sample' not in file_path:
                if '/classifiers' not in file_path:
                    sub_dir_files.append(file)
        if '/sample' not in file_path:
            if '/classifiers' not in file_path:
                transfer_files[sub_dir_name]=sub_dir_files

    #remove 1st element of the dict which is empty
    transfer_files.pop('', None)
    #counting no of classified folders
    classified_category_count=0
    for key in transfer_files:
        if key!= 'uploaded' and key!='classified' and key!='not_classified':
            classified_category_count+= 1
    classified_category_count+= 1

    return transfer_files, classified, classified_category_count