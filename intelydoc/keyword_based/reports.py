import os

def classified_file(folder_path):
    total_files = 0  # total files
    classified_file_count = {}
    for dirpath, sub_dirnames, filenames in os.walk(folder_path+'classified'):
        for sub_directory in sub_dirnames:
            for dirpath, sub_dirnames, filenames in os.walk(folder_path+'classified/'+sub_directory):
                file_count_sub= len(filenames)
                classified_file_count[sub_directory]=file_count_sub
                total_files += file_count_sub
    return classified_file_count,total_files
def un_classified_file(folder_path):
    for dirpath, sub_dirnames, filenames in os.walk(folder_path+'not_classified'):
        un_classified_file_count= len(filenames)
        return un_classified_file_count

def uploaded_file(folder_path):
    for dirpath, sub_dirnames, filenames in os.walk(folder_path+'uploaded'):
        uploaded_file_count= len(filenames)
        return uploaded_file_count

def get_report_full(folder_path, report_type):
    documents={}
    
    for file_path,directory, files in os.walk(folder_path):
        sub_dir_name = os.path.basename(file_path)
        for file in files:
            sub_dir_name = os.path.basename(file_path)
            sub_dir_files=[]
            if '/sample' not in file_path and '/uploaded' not in file_path:
                if '/classifiers' not in file_path:
                    if not file.endswith('.zip'):
                        sub_dir_files.append(sub_dir_name)
                        file_size = str(round((os.path.getsize(file_path+'/'+file))/1000))+' KB'
                        sub_dir_files.append(file_size)
                        documents[file]=sub_dir_files
    
    classified_file_count,total_classsified = classified_file(folder_path)
    un_classified_file_count = un_classified_file(folder_path)
    uploaded_file_count = uploaded_file(folder_path)

    return documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classsified

def get_report_cl(folder_path, report_type):
    documents={}
    
    for file_path,directory, files in os.walk(folder_path+'classified'):
        sub_dir_name = os.path.basename(file_path)
        for file in files:
            sub_dir_name = os.path.basename(file_path)
            sub_dir_files=[]
            if '/sample' not in file_path and '/uploaded' not in file_path:
                if '/classifiers' not in file_path and '/not_classified' not in file_path:
                    if not file.endswith('.zip'):
                        sub_dir_files.append(sub_dir_name)
                        file_size = str(round((os.path.getsize(file_path+'/'+file))/1000))+' KB'
                        sub_dir_files.append(file_size)
                        documents[file]=sub_dir_files

    classified_file_count,total_classsified = classified_file(folder_path)
    un_classified_file_count = un_classified_file(folder_path)
    uploaded_file_count = uploaded_file(folder_path)
    return documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classsified

def get_report_un(folder_path, report_type):
    documents={}
    
    for file_path,directory, files in os.walk(folder_path+'not_classified'):
        for file in files:
            sub_dir_files=[]
            if '/sample' not in file_path and '/uploaded' not in file_path:
                if '/classifiers' not in file_path and '/classified' not in file_path:
                    if not file.endswith('.zip'):
                        sub_dir_files.append('not_classified')
                        file_size = str(round((os.path.getsize(file_path+'/'+file))/1000))+' KB'
                        sub_dir_files.append(file_size)
                        documents[file]=sub_dir_files
                        
    classified_file_count,total_classsified = classified_file(folder_path)
    un_classified_file_count = un_classified_file(folder_path)
    uploaded_file_count = uploaded_file(folder_path)
    return documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classsified

def get_report_category(folder_path,category_name):
    documents={}
    print(category_name)
    for file_path,directory, files in os.walk(folder_path+'classified'):
        for file in files:
            sub_dir_name = os.path.basename(file_path)
            sub_dir_files=[]
            if category_name in file_path:
                if not file.endswith('.zip'):
                    sub_dir_files.append(sub_dir_name)
                    file_size = str(round((os.path.getsize(file_path+'/'+file))/1000))+' KB'
                    sub_dir_files.append(file_size)
                    documents[file]=sub_dir_files
    print(documents)
    return documents

def get_category_names(folder_path):
    categories=[]
    for file_path,directory, files in os.walk(folder_path+'classified'):
        for file in files:
            if '/sample' not in file_path and '/uploaded' not in file_path:
                if '/classifiers' not in file_path and '/not_classified' not in file_path:
                    if not file.endswith('.zip'):
                        sub_dir_name = os.path.basename(file_path)
                        if sub_dir_name not in categories:
                            categories.append(sub_dir_name)
    return categories
    print(categories)