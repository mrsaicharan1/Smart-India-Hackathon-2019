import re
import nltk
import bs4 as bs   

from extract_ppt import ppt_to_text
import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
# article_text = ppt_to_text()
articles = ['https://www.everydayhealth.com/drugs/acetylcysteine',
            'https://www.empr.com/drug/acetylcysteine-solution-for-inhalation/',
            'https://en.wikipedia.org/wiki/Acetylcysteine',
            'https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5558a5f5-e821-473b-7d8a-5d33d09f0586&type=display',
            'https://www.empr.com/drug/acetylcysteine-solution-for-inhalation/',
            'https://www.webmd.com/lung/breathing-problems-causes-tests-treatments#1'
            'https://www.healthline.com/health/home-treatments-for-shortness-of-breath', 'https://prowersmedical.com/solutions-for-lung-disease-and-breathing-problems/',
            'https://www.practo.com/medicine-info/ambroxol-530-api', 'https://en.wikipedia.org/wiki/Ambroxol', 'https://clinicaltrials.gov/ct2/show/NCT03415269',
            'https://en.wikipedia.org/wiki/Cetirizine', 'https://www.who.int/csr/disease/coronavirus_infections/faq/en/','https://www.cdc.gov/healthcommunication/toolstemplates/entertainmented/tips/ChronicRespiratoryDisease.html',
            'https://www.webmd.com/lung/copd/10-faqs-about-living-with-copd#1']


for article in articles:
    try:
        scraped_data = opener.open(article)
        article_text = scraped_data.read()
    except Exception as e:
        continue
    parsed_article = bs.BeautifulSoup(article_text,'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""

    for p in paragraphs:  
        article_text += p.text

    raw_data = article_text
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)  

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    import heapq  
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)  

    # Removing Square Brackets and Extra Spaces
    summary = re.sub(r'\[[0-9]*\]', ' ', summary)  
    summary = re.sub(r'\s+', ' ', summary)

    # Removing special characters and digits
    summary = re.sub('[^a-zA-Z]', ' ', summary)  
    summary = re.sub(r'\s+', ' ', summary)

    print(summary)
    print("----------------------------------------")
    print("----------------------------------------")
    print("----------------------------------------")
    print("----------------------------------------")

    from rake_nltk import Rake
    r = Rake()
    r.extract_keywords_from_text(raw_data)
    keywords_yay = r.get_ranked_phrases()
    print(keywords_yay)

    print("----------------------------------------")