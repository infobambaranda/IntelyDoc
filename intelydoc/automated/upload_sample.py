#for upload
import os, shutil

def upload(username,request,classifier_name,classifier_description):
    path = 'uploads/'+username+'/sample/'

    if os.path.exists(path):  
        shutil.rmtree(path)            
    os.makedirs(path)

    categories = []
    input_count = int(request.POST['input_count'] )
    print(input_count)
    for i in range(input_count):
        category_name=request.POST['category'+str(i)]
        categories.append(category_name)
        upload_path= path + category_name + '/'
        os.makedirs(upload_path)
        files = request.FILES.getlist('files'+str(i))
        for file in files:
            file_name = str(file)
            with open(os.path.join(upload_path, file_name), 'wb') as f:
                # Block writing large files to prevent stuck
                for chunk in file.chunks(chunk_size=2014):
                    f.write(chunk)
    categories.sort()

    path = 'uploads/'+username+'/classifiers/'
    if not os.path.exists(path): 
        os.makedirs(path)
    
    classifier_categogories_file_path = 'uploads/' + username + '/classifiers/' + classifier_name + '.txt'
    for index,category in enumerate(categories):
        if index == 0:
            with open(classifier_categogories_file_path, 'w') as f:
                f.write(category)
        else:
            with open(classifier_categogories_file_path, 'a') as f:
                f.write('/')
                f.write(category)
    with open(classifier_categogories_file_path, 'a') as f:
        f.write('/')
        f.write(classifier_description)