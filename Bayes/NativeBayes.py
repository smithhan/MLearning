import csv

def list_words(text):
    words = []
    words_tmp = text.lower().split()
    for w in words_tmp:
        if w not in words and len(w) > 3:
            words.append(w)
    return words


def training(texts):
    words=[]
    c_word = {}
    c_categories = {}
    c_texts = 0
    c_total_words = 0
    for t in texts:
        c_texts = c_texts + 1
        if t[1] not in c_categories:
            c_categories[t[1]] = 1
        else:
            c_categories[t[1]] = c_categories[t[1]] + 1
    for t in texts:
        words = list_words(t[0])
    for p in words:
        if p not in c_word:
          c_total_words = c_total_words + 1
          c_word[p] = {}
          for c in c_categories:
            c_word[p][c] = 0
        c_word[p][t[1]] = c_word[p][t[1]] + 1
    return (c_word, c_categories, c_texts, c_total_words)


def classifier(subject_line, c_words, c_categories, c_texts, c_tot_words):
    category = ""
    category_prob = 0
    for c in c_categories:
        prob_c = float(c_categories[c]) / float(c_texts)
        words = list_words(subject_line)
        pro_total_c = prob_c
        for p in words:
            if p in c_words:
                prob_p = float(c_words[p][c]) / float(c_tot_words)
                # probabilty p(category|word)
                prob_cond = prob_p / prob_c
                # probablity p(word|category)
                prob = (prob_p * prob_cond) / prob_c
                pro_total_c = pro_total_c * prob

            if category_prob < pro_total_c:
                category = c
                category_prob = pro_total_c

    return (category, category_prob)

if __name__ == "__main__":

    with open('/Users/hanzhao/PycharmProjects/MLstudy/file/training.csv') as f:
        subjects = dict(csv.reader(f, delimiter=','))
        p,c,t,tp = training(subjects.items())

        #First Test
        clase = classifier("FREE Cell Phone + $50 Cash Back",p,c,t,tp)
        print("Result: {0} ".format(clase))


    #Second Test
    with open("/Users/hanzhao/PycharmProjects/MLstudy/file/test.csv") as f:
        correct = 0
        tests = csv.reader(f)
        for subject in tests:
            clase = classifier(subject[0],p,c,t,tp)
            if clase[0] == subject[1]:
                correct += 1
        print("Efficiency {0} of 10".format(correct))