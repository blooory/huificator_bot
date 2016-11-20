import string

def n_slogov(s):
    return len(list(filter(lambda x: x in 'уеыаоэяиюё', list(s))))

def vowel_pos(s, num_vowel):
    cnt = 0
    vowel_cnt = 0
    for i in s:
        if (i in 'уеыаоэяиюё'):
            vowel_cnt += 1
            if vowel_cnt == num_vowel:
                return cnt
        cnt += 1

def replace_string(s, d):
    for key in d:
        s = s.replace(key, d[key])
    return s

def leave_only_russian_letters(s):
    s_upd = ''
    for letter in s:
        s_upd += letter*(letter in 'ёйцукенгшщзхъфывапролджэячсмитьбю ')
    return s_upd

def huificate_word(hui_word):
    prefix = 'ху'
    print(hui_word)
    if n_slogov(hui_word) <= 2:
        vowel = hui_word[vowel_pos(hui_word, 1)]
        postfix = hui_word[(vowel_pos(hui_word, 1)+1):]
        vowel = replace_string(vowel, {'а':'я', 'у':'ю', 'о':'ё','э':'е'})
    else:
        vowel = hui_word[vowel_pos(hui_word, 2)]
        postfix = hui_word[(vowel_pos(hui_word, 2)+1):]
        vowel = replace_string(vowel, {'а':'я', 'у':'ю', 'о':'ё','э':'е'})
    return prefix + vowel + postfix

def preprocess_text(text):
    exclude = set(string.punctuation)
    text = (''.join(ch for ch in text if ch not in exclude)).lower()
    text = leave_only_russian_letters(text)
    text = [x for x in (set(text.split(' ')) - {''}) if n_slogov(x)>=2]
    return text
    
def find_verbs(words, parser):
    verbs = []
    COUNT = 'sing'
    GENDER = 'femn'
    PERSON = '3per'
    for word in words:
        res = parser.parse(word)[0]
        print(res.tag.POS)
        if (res.tag.POS == 'VERB') | (res.tag.POS == 'INFN'):
            if res.tag.gender is None:
                res = res.inflect({COUNT,PERSON})
            else:
                res = res.inflect({COUNT,PERSON,GENDER})
            verbs.append(res.word)
    return verbs
    
