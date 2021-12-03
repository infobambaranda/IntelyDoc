import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import keyword_based.text_extraction as tx
from .preprocessing import text_preprocessing


def extract_keywords(name):


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
        text = ['']

    #text = text_preprocessing(text)
    text = text.lower()
    return text
    '''dataset=[text]
    if dataset == ['']:
        return dataset
    else:
        tfIdfVectorizer=TfidfVectorizer(use_idf=True)
        tfIdf = tfIdfVectorizer.fit_transform(dataset)
        df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        df=df.head(5)
        values=df.index.tolist()
        print(df)
        return values'''
        

