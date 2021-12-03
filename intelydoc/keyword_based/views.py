#for views
import builtins
from django.shortcuts import render, HttpResponse,redirect

#for upload
import os,shutil
from .upload import upload_files

#for classifier
from .keyword_extraction import extract_keywords
#from django.template import loader
from django.template.response import TemplateResponse

#for download
from .view_docs import show_files

#for create_zip
from .create_zip import create_zipfile 
from django.http.response import FileResponse

# for duplicates
from filecmp import cmp

#login
from django.contrib.auth.models import User,auth

#for reports
from .reports import  get_category_names, get_report_full, get_report_cl, get_report_un, get_category_names,get_report_category
from django.contrib.auth.models import User

# Create your views here.
def upload(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else: 
        usernames=[]
        emails=[]
        users = User.objects.all()
        count=0
        for record in users.iterator():
            usernames.append(record.username)
            emails.append(record.email)
            count = count + 1       
        return render(request, 'login.html',{'login':False, 'usernames':usernames, 'emails':emails, 'count':count})

    path='uploads/'+username+'/uploaded'

    if os.path.exists(path):
        folder_exists=True
    else:
        folder_exists=False

    if request.method == 'GET':
        clf_type=request.GET['clf_type']

        #check for classifier_name variable is set
        try:
            request.GET['classifier_name']
        except:
            classifier_name=None
        else:
            classifier_name=request.GET['classifier_name']

        #check for built_in variable is set
        try:
            request.GET['built_in']
        except:
            built_in=None
        else:
            built_in=request.GET['built_in']


        try:
            request.GET['prev']
        except:
            return render(request, 'upload.html',{'folder_exists':folder_exists, 'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in})
        else:            
            return render(request, 'upload.html',{'folder_exists':folder_exists, 'clf_type':clf_type, 'prev':'True', 'classifier_name':classifier_name, 'built_in':built_in})
        

    elif request.method == 'POST':
        upload_type=request.POST['upload']
        clf_type=request.POST['clf_type']
        classifier_name=request.POST['classifier_name']
        built_in=request.POST['built_in']
        upload_path = 'uploads/' + username + '/uploaded/'  
        path= 'uploads/' + username + '/uploaded/'

        # The file object to take name attribute value input box
        file_folder = request.FILES.getlist('folder')
        multiple_files = request.FILES.getlist('files')
        files = file_folder + multiple_files

        # uploading files and getting file count
        uploaded_count=upload_files(path,upload_path,upload_type, files)
        folder_exists = True
        
        return render(request, 'upload.html',{'folder_exists':folder_exists, 'uploaded_count':uploaded_count, 'clf_type':clf_type, 'uploaded':'True', 'classifier_name':classifier_name, 'built_in':built_in})
    else:
        return redirect('upload') 

def keyword_based(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'POST':

        #Remove classified and not classifed directories if exist
        classified_path='uploads/'+username+'/classified/'
        if os.path.exists(classified_path):                    
            shutil.rmtree(classified_path)
        not_classified_path='uploads/'+username+'/not_classified/'
        if os.path.exists(not_classified_path):                    
            shutil.rmtree(not_classified_path)

        #create a dict for categories and relevant keywords
        category_list={}
        input_count = int(request.POST['input_count'] )
        for i in range(input_count):
            category = request.POST['category'+str(i)]
            defined_keywords= request.POST['defined_keywords'+str(i)]
            category_list[category]= defined_keywords.split(',')
        
        path='uploads/'+username+'/uploaded/'
        after_classification_path = 'uploads/'+username+'/'
        
        for filename in os.listdir(path):
            name=os.path.join(path,filename)
            extracted_keywords=extract_keywords(name)
            #list for matching count of all categories
            all_matching_percentages = {}
            if extracted_keywords != [''] or extracted_keywords is not None:
                #check if extracted keywords are matching with given keywords 
                matched = False          
                for category_name in category_list:
                    matching_keyword_count=0
                    #for extracted_keyword in extracted_keywords:
                    for given_keyword in category_list[category_name]:
                            given_keyword = given_keyword.lower()
                            if given_keyword in extracted_keywords:
                                matching_count = extracted_keywords.count(given_keyword)
                                matching_keyword_count += matching_count
                    matching_percentage = (matching_keyword_count/len(category_list[category_name]))
                    all_matching_percentages[category_name] = matching_percentage
                if all_matching_percentages != []:
                    matching_category = max(all_matching_percentages, key=all_matching_percentages.get)

                    if all_matching_percentages[matching_category] > 0:
                        # new path to upload classified files
                        classify_path=after_classification_path +'classified/'+ matching_category + '/'
                        if not os.path.exists(classify_path):
                            os.makedirs(classify_path)
                        #copy file to new path
                        shutil.copy(name, classify_path)
                        matched = True

                if matched is False:
                    not_classified_path = after_classification_path +'not_classified/'
                    if not os.path.exists(not_classified_path):
                        os.makedirs(not_classified_path)
                    shutil.copy(name, not_classified_path) 
                      
            else:
                not_classified_path = after_classification_path +'not_classified/'
                if not os.path.exists(not_classified_path):
                    os.makedirs(not_classified_path)
                shutil.copy(name, not_classified_path)

            
        return redirect('/keyword_based/download')
    else:
        return render(request, 'keyword_based.html')

def download(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:
        usernames=[]
        emails=[]
        users = User.objects.all()
        count=0
        for record in users.iterator():
            usernames.append(record.username)
            emails.append(record.email)
            count = count + 1       
        return render(request, 'login.html',{'login':False, 'usernames':usernames, 'emails':emails, 'count':count})

    
    folder_path='uploads/'+username+'/'

    #traverse through directories and build a dict
    transfer_files, classified, classified_category_count =show_files(folder_path)
    view_file_path='/uploads/'+username+'/'
    return render(request, 'download.html', {'transfer':transfer_files,'classified_category_count':classified_category_count, 'classified':classified, 'path':view_file_path})


def create_zip(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'GET':
        subdir_name=request.GET['folder_name']

        path='uploads/'+username+'/'+subdir_name+'/'
        destination_path='uploads/'+username+'/'+subdir_name+'/'

        #Create zipfile
        response=create_zipfile(destination_path, path, username, subdir_name)
        return response

def duplicate(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'GET':
        clf_type=request.GET['clf_type']
        classifier_name=request.GET['classifier_name']
        built_in=request.GET['built_in']

        return render(request, 'duplicate.html',{'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in})

    if request.method == 'POST':
        
        clf_type=request.POST['clf_type']
        classifier_name=request.POST['classifier_name']
        built_in=request.POST['built_in']

        
        file_dir = 'uploads/'+username+'/uploaded/'

        try:
            request.POST['search']
        except:
            try:
                request.POST['remove']
            except:
                print('done')
                selected_files=request.POST.getlist('selected_files')
                for file_name in selected_files:
                    file_path = file_dir + file_name
                    os.remove(file_path) 
                return render(request, 'duplicate.html', {'removed':True, 'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in})
            else:
                true_duplicates = request.POST['true_duplicates']

                #Converting query string to a list
                true_duplicates = true_duplicates.replace("[", "")
                true_duplicates = true_duplicates.replace("'", "")
                true_duplicates = true_duplicates.replace("]", "")
                true_duplicates = true_duplicates.split(', ')

                for file_name in true_duplicates:
                    file_path = file_dir + file_name
                    os.remove(file_path)    
                return render(request, 'duplicate.html', {'removed':True, 'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in})

        else:
            files = sorted(os.listdir(file_dir))

            # list containing the classes of documents with the same content
            duplicates = []
            all_files = []
            true_duplicates = []

            count=0
            # comparison of the documents
            for file in files:
                
                is_duplicate = False
                
                check=file_dir + file
                

                for class_ in all_files:
                    check_with = file_dir + class_[0]

                    is_duplicate = cmp(
                        check,
                        check_with,
                        shallow = False
                    )
                    if is_duplicate:
                        count += 1
                        class_.append(file)
                        true_duplicates.append(file)
                        break
                
                if not is_duplicate:
                    all_files.append([file]) 
            for item in all_files:
                if len(item)>1:
                    duplicates.append(item)
            path= '/uploads/'+username+'/uploaded/'
            return render(request, 'duplicate.html',{'duplicates': duplicates, 'true_duplicates':true_duplicates, 'count':count, 'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in, 'path':path})

def reports(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})
    return render(request, 'reports.html')   

def view_reports(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'POST':
        category_name = request.POST['category_name']
        folder_path='uploads/'+username+'/'
        categories = get_category_names(folder_path)
        documents = get_report_category(folder_path,category_name)
        return render(request, 'show_category_report.html',{'categories':categories,'documents':documents})
    else:
        user_details = User.objects.get(username=username)

        report_type = request.GET['report']
        folder_path='uploads/'+username+'/'
        if report_type == 'full':
            documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classified= get_report_full(folder_path, report_type)
        elif report_type == 'cl':
            documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classified= get_report_cl(folder_path, report_type)
        elif report_type == 'un':
            documents,classified_file_count,un_classified_file_count, uploaded_file_count,total_classified= get_report_un(folder_path, report_type)
        elif report_type == 'category':
            categories = get_category_names(folder_path)
            return render(request, 'show_category_report.html',{'categories':categories})

        
        return render(request, 'show_reports.html',{'documents':documents, 'user_details':user_details,
        'classified_file_count':classified_file_count,'un_classified_file_count':un_classified_file_count,
        'uploaded_file_count':uploaded_file_count, 'total_classified':total_classified}) 

            