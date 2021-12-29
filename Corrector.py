import re
from collections import Counter
import pickle


class Corrector:

    def __words__(self, text):
        return re.findall(r'\w+', text.lower())

    def __init__(self):
        f = open("not_unique_final_cleaned_vocab.pkl", 'rb')
        dicti = pickle.load(f)
        f.close()
        self.dicti = list(filter(None, dicti))
        self.WORDS = Counter(self.__words__(open('big.txt', 'r', encoding='utf-8').read()))

    def correction(self, word, context):
        "Most probable spelling correction for word."
        spell_context = Counter(self.__candidates__(word, context))
        real_candidates = spell_context.most_common()
        #     N=sum(spell_context.values())
        #     for i in range(0,len(spell_context)):
        #         spell_context[word] = spell_context[word] / N
        #     print(spell_context)
        return real_candidates[0]

    def corrector(self, word):
        def candidates():
            "Generate possible spelling corrections for word."
            return self.__known__([word]) or self.__known__(self.__edits1__(word)) or self.__known__(
                self.__edits2__(word)) or [word]

        def P(cw, N=sum(self.WORDS.values())):
            "Probability of `word`."
            return self.WORDS[cw] / N

        return max(candidates(), key=P)

    def __candidates__(self, word, context):
        "Generate possible spelling corrections for word."
        norvig_candidates = (
                self.__known__([word]) | self.__known__(self.__edits1__(word)) | self.__known__(
            self.__edits2__(word)) | {word})
        context_candidates = self.__context_sensitive_candidates__(context)
        current_context = Counter([w for w in context_candidates if w in norvig_candidates])
        return [w for w in context_candidates if w in norvig_candidates]

    def __known__(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)

    def __edits1__(self, word):
        "All edits that are one edit away from `word`."
        letters = 'آابپتثجچحخدذرزژسشضطظعغفقکگلمنوهی'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [R + L[1:] for R, L in splits if L]
        transposes = [R + L[1] + L[0] + L[2:] for R, L in splits if len(L) > 1]
        replaces = [R + c + L[1:] for R, L in splits if L for c in letters]
        inserts = [R + c + L for R, L in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def __edits2__(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.__edits1__(word) for e2 in self.__edits1__(e1))

    def sen_corrector(self, query):
        words = query.split()
        for i in range(0, len(words)):
            #         words[i] = correction(words[i],' '.join(words[:i] + words[i+1:]))
            words[i] = self.correction(words[i], query)
        return words

    def __context_sensitive_candidates__(self, words):
        possibles = []
        for w in words.split():
            indices = [i for i, x in enumerate(self.dicti) if x == w]
            for i in indices:
                possibles.extend(self.dicti[i:i + 2] + self.dicti[i - 1:i])
        return possibles


Cor = Corrector()
print(Cor.sen_corrector('خیابان اپام'))
print(Cor.sen_corrector('کاهن مبعد'))

print(Cor.corrector('انلقاب'))
