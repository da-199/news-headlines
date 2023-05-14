import json
import pandas as pd
import re

def test_word(event, context):
    
    df = pd.DataFrame(event)
    df_word = pd.DataFrame()

    exclude = ['a', 'an', 'and', 'the', 'on', 'he','him',
    'she','her','they','who','what','where','when','of',
    'for','with','next','by','to','it','are','about',
    'them', 'his','hers','at','after','in','i','now',
    'how','my','is','says','up','all','that','got',
    'will','new','one','some','would','off','as','from',
    'was','say','but','can','not','this', 'has','have',
    'we','be','into','get','give','actually','every',
    'more','why','could','well','make','best','according',
    'or','your', 'through','over','its', 'here', 'our',
    'coming','do','wants','want','were','just',
    'keep','keeps','out','top','drop','their','there',
    'need','needs','even','ask','way','ways','saw','seen',
    'these','own','very','see','go','try','tried','use','starting',
    'start','if','yet','they’re','often','few','only','you','no']
    
    lst = []
    
    df_word['Word'] = df['Title'].apply(lambda x: x.split(' '))
    df_word = df_word.explode('Word').reset_index(drop=True)
    flat = df_word['Word'].tolist()
    flat = [item for item in flat if pd.notnull(item)]
    
    final = []
    
    for i in range(len(flat)):
            
        flat[i] = re.sub("’s$",'',flat[i]) 
        flat[i] = re.sub("'s$",'',flat[i]) 
        flat[i] = re.sub('[-‘’—()+;&!$?:,.]', '', flat[i])
        flat[i] =  flat[i].replace("'", '')
        flat[i] = re.sub('\d','', flat[i])
    
        for y in exclude:
            if y == flat[i].lower():
                flat[i] = flat[i].lower().replace(y, '') 
    
    word_list = [item for item in flat if item]
    
    word_counts = {}
    for word in word_list: 
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    df_final = pd.DataFrame(list(word_counts.items()), columns=['word', 'count'])
    
    return {'staging_word_count': df_final.to_dict('list'), 'v2_headline': df.to_dict('list')}
