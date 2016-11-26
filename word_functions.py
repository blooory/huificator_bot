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
    # I did it in we_find_latin_letters function
    #text = leave_only_russian_letters(text)
    text = [x for x in (set(text.split(' ')) - {''}) if n_slogov(x)>=2]
    return text
    
def find_verbs(words, parser):
    verbs = []
    COUNT = 'sing'
    GENDER = 'femn'
    PERSON = '3per'
    for word in words:
        res = parser.parse(word)[0]
        if (res.tag.POS == 'VERB') | (res.tag.POS == 'INFN'):
            if res.tag.gender is None:
                res = res.inflect({COUNT,PERSON})
            else:
                res = res.inflect({COUNT,PERSON,GENDER})
            try:
                verbs.append(res.word)
            except:
                pass
    return verbs

latin_to_russian = {u'e':u'е',u'y':u'у',u'o':u'о',u'p':u'р',u'a':u'а',u'k':u'к',u'x':u'х',u'c':u'с',u'b':u'ь',\
                    u'm':u'т',u'n':u'п',u'3':u'з',u'0':u'о'}
latin_to_russian_keys = list(latin_to_russian.keys())
russian_letters = u'й ц у к е н г ш щ з х ъ ф ы в а п р о л д ж э ё я ч с м и т ь б ю'.split()

def replace_fake_letter(three_letters):
    if  three_letters[0] in russian_letters and three_letters[1] in latin_to_russian_keys and\
    three_letters[0] in russian_letters:
        three_letters = three_letters[0] + latin_to_russian[three_letters[1]] + three_letters[2]
    elif three_letters[0] in russian_letters and three_letters[1] in latin_to_russian_keys and\
    three_letters[2] in latin_to_russian_keys :
        three_letters = three_letters[0] + latin_to_russian[three_letters[1]] + latin_to_russian[three_letters[2]] 
    elif three_letters[2] in russian_letters and three_letters[1] in latin_to_russian_keys and\
    three_letters[0] in latin_to_russian_keys :
        three_letters = latin_to_russian[three_letters[0]] + latin_to_russian[three_letters[1]]+three_letters[2] 
    return three_letters

def find_fake_letters(word):
    old_word = word
    for i in range(len(word)-3):
        word = word[:i] + replace_fake_letter(word[i:i+3]) + word[i+3:]
    flag_fake = (old_word != word)
    return word,flag_fake
    
def we_find_latin_letters(words):
    new_words = []
    fake_flag = False
    for word in words:
        if len(leave_only_russian_letters(word)) >2:
            new_word,flag_word = find_fake_letters(word)
            new_words.append(new_word)
            if flag_word:
                fake_flag = True
    return new_words, fake_flag