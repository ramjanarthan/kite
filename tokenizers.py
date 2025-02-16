from primitives import Bigram, Trigram

class BigramTokenizer:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.file_descriptor = open(filename, 'r')
        self.prev_bigram = None

    def next(self):
        curr_char = self.file_descriptor.read(1)

        if not curr_char:
            return None
        elif not self.prev_bigram:
            # We are the start of the file, and minimally can expect one more character to follow
            next = self.file_descriptor.read(1)

            if not next:
                raise Exception("Expected to have atleast one characters after a new line")
            
            bigram = Bigram(start=curr_char, end=next)
            self.prev_bigram = bigram
            return bigram
        else:
            # We are not at the start of line, so we expect prev_bigram to be a non null object
            if not self.prev_bigram:
                raise Exception("Expected a prev_bigram but found null")
            
            bigram = Bigram(start=self.prev_bigram.end, end=curr_char)
            self.prev_bigram = bigram
            return bigram

class TrigramTokenizer:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.file_descriptor = open(filename, 'r')
        self.prev_trigram = None

    def next(self):
        curr_char = self.file_descriptor.read(1)

        if not curr_char:
            return None
        elif not self.prev_trigram:
            # We are the start of the line, and minimally can expect one character and the end_of_line to follow
            next = self.file_descriptor.read(1)
            last = self.file_descriptor.read(1)

            if not next or not last:
                raise Exception("Expected to have atleast two characters after a new line")
            
            trigram = Trigram(start=curr_char, middle=next, end=last)
            self.prev_trigram = trigram
            return trigram
        else:
            # We are not at the start of line, so we expect prev_trigram to be a non null object
            if not self.prev_trigram:
                raise Exception("Expected a prev_trigram but found null")
            
            trigram = Trigram(start=self.prev_trigram.middle, middle=self.prev_trigram.end, end=curr_char)
            self.prev_trigram = trigram
            return trigram
