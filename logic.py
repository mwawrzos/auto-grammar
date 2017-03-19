from sentenceParser import lexer


class Token:
    def __init__(self, name):
        self.name = name
        self.meta = []
        self.predecessors = dict()
        self.successors = dict()

    def inc_pre(self, predecessor):
        self.predecessors[predecessor] = self.predecessors.get(predecessor, 0) + 1

    def inc_suc(self, successor):
        self.successors[successor] = self.successors.get(successor, 0) + 1

    def get_name(self):
        return self.name


class StartToken(Token):
    def __init__(self):
        Token.__init__(self, '<start>')


class EndToken(Token):
    def __init__(self):
        Token.__init__(self, '<end>')


def add_meta(meta, with_id):
    return meta + [with_id.attrib['id']]


class TokenAnalyzer:
    def __init__(self, previous, tokens, meta):
        self.meta = meta
        self.tokens = tokens
        self.previous = previous

    def next(self, token):
        if token not in self.tokens:
            self.tokens[token] = Token(token)
        self.tokens[token].meta.append(self.meta)

        self.previous.inc_suc(token)
        self.tokens[token].inc_pre(self.previous.get_name())
        self.previous = self.tokens[token]

    def fin(self):
        return self.previous


class Stats:
    def __init__(self):
        self.tokens = dict()

    def analyse_book(self, book):
        for chapter in book:
            self.analyse_chapter(chapter, add_meta([], book))

    def analyse_chapter(self, chapter, meta):
        previous = StartToken()
        for verse in chapter:
            previous = self.analyse_verse(previous, verse, add_meta(meta, chapter))
        previous.inc_suc(EndToken)

    def analyse_verse(self, previous, verse, meta):
        analyser = TokenAnalyzer(previous, self.tokens, add_meta(meta, verse))
        lexer.input(verse.text)
        for token in lexer:
            analyser.next(token.value)
        return analyser.fin()
