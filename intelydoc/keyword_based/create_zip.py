import shutil
from django.shortcuts import HttpResponse

def create_zipfile(destination_path, path, username, subdir_name):
    #making zip file
    shutil.make_archive(destination_path, 'zip', path)

    #download zip file
    zip_file_path= 'uploads/'+username+'/' + subdir_name +'.zip'
    zip_file = open(zip_file_path, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="'+subdir_name+'.zip'
    return response