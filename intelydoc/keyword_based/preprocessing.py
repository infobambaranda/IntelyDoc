import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def text_preprocessing(text):
    text = text.replace('\n', ' ')    
    text=text.lower()  
    text=re.sub("(\\d|\\W)+"," ",text)# remove special characters and digits    
    text_tokens =text.split()#splitting text into words
        
    en_stops = set(stopwords.words('english')) 
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]#removing stop words and tokenizing
    
    ps = PorterStemmer()  
    stem_words=[word for word in tokens_without_sw if ps.stem(word) ]#stemming
    
    text = ' '.join(stem_words) # concatenating array elements to a string.

    return text