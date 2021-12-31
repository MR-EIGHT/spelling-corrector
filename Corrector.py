import random
import time
from collections import Counter
import pickle


class Corrector:
    """
    This class is used to correct queries by using Peter Norvig's implementation of edit-distance algorithm in its core.
    """

    def __init__(self):
        """
              initializes the class.
              loads the data.
              counts the frequencies of the words.
        """
        f = open("data+.pkl", 'rb')
        self.dicti = pickle.load(f)
        f.close()
        self.WORDS = Counter(self.dicti)

    def correction(self, word, context):
        """Most probable spelling correction for word by considering the context."""
        spell_context = Counter(self.__candidates__(word, context))
        real_candidates = spell_context.most_common(5)

        return real_candidates[0][0]

    def corrector(self, word):
        """
        Isolated correction function.
        """

        def candidates():
            """Generate possible spelling corrections for word."""
            return self.__known__([word]) or self.__known__(self.__edits1__(word)) or self.__known__(
                self.__edits2__(word)) or [word]

        def p(cw, N=sum(self.WORDS.values())):
            """Probability of `word`."""
            return self.WORDS[cw] / N

        return max(candidates(), key=p)

    def __candidates__(self, word, context):
        """Generate possible spelling corrections for word."""
        norvig_candidates = (
                self.__known__([word]) | self.__known__(self.__edits1__(word)) | self.__known__(
            self.__edits2__(word)) | {word})
        context_candidates = self.__context_sensitive_candidates__(context)
        return [w for w in context_candidates if w in norvig_candidates]

    def __known__(self, words):
        """The subset of `words` that appear in the dictionary of WORDS."""
        return set(w for w in words if w in self.WORDS)

    def __edits1__(self, word):
        """All edits that are one edit away from `word`."""
        letters = 'آابپتثجچحخدذرزژسشضطظعغفقکگلمنوهی'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [R + L[1:] for R, L in splits if L]
        transposes = [R + L[1] + L[0] + L[2:] for R, L in splits if len(L) > 1]
        replaces = [R + c + L[1:] for R, L in splits if L for c in letters]
        inserts = [R + c + L for R, L in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def __edits2__(self, word):
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.__edits1__(word) for e2 in self.__edits1__(e1))

    def sensitive_corrector(self, query):
        """
              main function that iterates over the query words and corrects them.
        """
        words = query.split()
        rate = 0
        # checks the frequency of the whole phrase in case all the entered words are wrong...
        # in that case the program corrects one word randomly and isolated.
        # then tries to generate the context and edit by using the context.
        for i in range(0, len(words)):
            rate += self.WORDS[words[i]]
        if rate < 100:
            index = random.randint(0, len(words) - 1)
            words[index] = self.corrector(words[index])
            query = ' '.join(words)

        for i in range(0, len(words)):
            words[i] = self.correction(words[i], query)
            query = ' '.join(words)
        return words

    def __context_sensitive_candidates__(self, words):
        """
        gets the words as query and generates a context by the local words of the words.
        """
        possibles = []
        for w in words.split():
            indices = [i for i, x in enumerate(self.dicti) if x == w]
            for i in indices:
                possibles.extend(self.dicti[i - 2:i + 3])
        return possibles

    def wspace_correction(self, query):
        """
        corrects whitespaces if the frequency of the joined words is more than the multiplication of the current word
        by 3.
        """
        words = query.split()
        i = 0
        while i < len(words) - 1:
            if self.WORDS[words[i] + words[i + 1]] > self.WORDS[words[i]] * 3:
                words[i] = words[i] + words[i + 1]
                del words[i + 1]
            else:
                i += 2
                continue
            i += 1
        return ' '.join(words)


if __name__ == '__main__':
    """
    tests written to test the corrector's performance and the time it takes to operate.
    """
    start = time.perf_counter()
    Cor = Corrector()

    print(Cor.wspace_correction('خمی نی اما م خو    بی'))
    print(Cor.wspace_correction('رن گین کما ن'))

    print(Cor.sensitive_corrector('خیابان اپام'))
    print(Cor.sensitive_corrector('کاهن مبعد'))
    print(Cor.sensitive_corrector(' السامی انلقاب'))
    print(Cor.sensitive_corrector('دوزت رشد'))
    print(Cor.sensitive_corrector('نزریه نسبیت'))
    print(Cor.sensitive_corrector(' السامی انلقاب'))
    print(Cor.sensitive_corrector('پدر عجب شیمی'))
    print(Cor.sensitive_corrector('انقلاب اسمالی ایراد'))
    print(Cor.sensitive_corrector('دین مسیهیت'))

    print(Cor.corrector('دوزت'))
    print(Cor.corrector('انلقاب'))
    print(Cor.corrector('فصادها'))
    print(Cor.corrector('انبسات'))
    print(Cor.corrector('انلغاد'))
    print(Cor.corrector('اسمالی'))
    print(Cor.corrector('انلقاب'))
    print(Cor.corrector('ایراد'))
    print(Cor.corrector('اگتشاف'))

    end = time.perf_counter()

    print(f'Elapsed time whole process: {end - start}')
