
#for views
from django.shortcuts import render,redirect
from django.http import HttpResponse

#for upload
from .upload_sample import upload

#for classification
import automated.train_classifier as train
import os,shutil,pickle
import keyword_based.text_extraction as tx

#login
from django.contrib.auth.models import User,auth

def automated(request):
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

    if request.method == 'GET':
        return render(request, 'automated.html')

def custom(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})
    
    if request.method == 'GET':
        return render(request, 'custom.html')

    if request.method == 'POST':
        classifier_name = request.POST['classifier_name']
        classifier_description = request.POST['classifier_description']
        upload(username,request,classifier_name,classifier_description)
        
        training_doc_path='uploads/'+username+'/sample/'
        categories = os.listdir(training_doc_path)

        # Train Document Classfier
        train.svm(training_doc_path,categories,classifier_name,username)
        #train.decision_tree(path,categories)

        return render(request, 'custom.html', {'train':'done', 'classifier_name':classifier_name})

def pre_trained(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'GET':

        #list of built in classifiers
        built_in_path='uploads/classifiers/'
        file_list = os.listdir(built_in_path)
        built_in_classifiers = {}
        #remove .sav from name
        for index, classifier_name in enumerate(file_list):
            if classifier_name.endswith('.sav'):
                new_name = classifier_name.replace('.sav', '')
                #built_in_classifiers[index] = new_name
            else:
                #built_in_classifiers.pop(index)
                txt_file_path='uploads/classifiers/' + classifier_name
                with open(txt_file_path) as f:
                    text = f.read()
                description = text.split("/")
                description = description[-1]
            if index % 2 == 1:
                built_in_classifiers[new_name] = description
                

        #list of custom classifiers
        custom_path='uploads/'+username+'/classifiers/'
        if os.path.exists(custom_path): 
            custom_classifier_file_list= os.listdir(custom_path) 
            custom_classifiers ={}

            index=len(custom_classifier_file_list) - 1
            #remove .sav from name
            for index, classifier_name in enumerate(custom_classifier_file_list):
                if custom_classifier_file_list[index].endswith('.sav'):
                    new_name = custom_classifier_file_list[index].replace('.sav', '')
                    #custom_classifiers[index] = new_name
                else:
                    #custom_classifiers.pop(index)
                    txt_file_path='uploads/'+username+'/classifiers/' + classifier_name
                    with open(txt_file_path) as f:
                        text = f.read()
                    description = text.split("/")
                    description = description[-1]
                if index % 2 == 1:
                    custom_classifiers[new_name] = description
                    index = index - 1
        else:
            custom_classifiers = None

        return render(request, 'pre_trained.html',{'built_in_classifiers':built_in_classifiers, 'custom_classifiers':custom_classifiers})

def classify(request):
    if request.session.has_key("name"):
        username=request.session['name']
    else:        
        return render(request, 'login.html',{'login':False})

    if request.method == 'GET':  
        classifier_name=request.GET['classifier_name']
        built_in=request.GET['built_in']
         
        if built_in == 'True':
            #list of categories
            categories_path='uploads/classifiers/' + classifier_name + '.txt'
            with open(categories_path) as f:
                text = f.read()
            categories = text.split("/")
            del categories[-1]
            filename = 'uploads/classifiers/' + classifier_name + '.sav'            
        else:
            #list of categories
            categories_path='uploads/'+username+'/classifiers/' + classifier_name + '.txt'
            with open(categories_path) as f:
                text = f.read()
            categories = text.split("/")
            del categories[-1]
            filename = 'uploads/' + username + '/classifiers/' + classifier_name + '.sav'
        
        #Remove classified and not classifed directories if exist
        classified_path='uploads/'+username+'/classified/'
        if os.path.exists(classified_path):                    
            shutil.rmtree(classified_path)
        not_classified_path='uploads/'+username+'/not_classified/'
        if os.path.exists(not_classified_path):                    
            shutil.rmtree(not_classified_path)

        for category_name in categories:
            after_classification_path=classified_path + category_name + '/'
            os.makedirs(after_classification_path)
        
        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))

        #perform Classifcation
        from_path='uploads/'+username+'/uploaded/'
        for filename in os.listdir(from_path):
            name=os.path.join(from_path,filename)
            if name.endswith(".pdf"):
                text = tx.read_pdf(name)
            elif name.endswith(".docx"):
                text = tx.read_docx(name)
            #elif name.endswith(".doc"):
                #text = read_doc(name)
            elif name.endswith(".xlsx") or name.endswith(".xls"):
                text = tx.read_xlsx(name)
            elif name.endswith(".pptx"):
                text = tx.read_pptx(name)
            elif name.endswith(".csv"):
                text = tx.read_csv(name)
            elif name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png") or name.endswith(".tiff") or name.endswith(".gif"):
                text = tx.read_image(name)
            elif name.endswith(".txt"):
                text = tx.read_txt(name)
            else:
                text=''

            text=[text]
            if text != ['']:
                predict=loaded_model.predict(text)
                predict=int(predict)
                category_name=categories[predict]

                after_classification_path=classified_path + category_name + '/'
                #copy file to new path
                shutil.copy(name, after_classification_path)
            else:
                #Copy files to not classified
                if not os.path.exists(not_classified_path):
                    os.makedirs(not_classified_path)
                shutil.copy(name, not_classified_path)        

        return redirect('download')

def automated_classify(request):
    if request.method == 'GET': 
        clf_type=request.GET['clf_type']
        classifier_name=request.GET['classifier_name']
        built_in=request.GET['built_in']
        return render(request, 'automated_classify.html',{'clf_type':clf_type, 'classifier_name':classifier_name, 'built_in':built_in})