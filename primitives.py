import numpy as np

class Unigram:
    """Class to represent a Unigram in one part: start"""
    __slots__ = ('start',)

    def __init__(self, start) -> None:
        self.start = start

    def __eq__(self, other) -> bool:
        return isinstance(other, Unigram) and self.start == other.start
    
    def __lt__(self, other) -> bool:
        return self.start < other.start
       
    def __hash__(self) -> int:
        return hash((self.start))
    
    def __str__(self) -> str:
        return f"Unigram Main: {self.start}"

class Bigram:
    """Class to represent a bigram in two parts: start and end"""
    __slots__ = ('start', 'end')

    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def __eq__(self, other) -> bool:
        return isinstance(other, Bigram) and self.start == other.start and self.end == other.end
    
    def __lt__(self, other) -> bool:
        if self.start != other.start:
            return self.start < other.start
        else:
            return self.end < other.end
        
    def __hash__(self) -> int:
        return hash((self.start, self.end))
    
    def __str__(self) -> str:
        return f"Bigram {self.start}{self.end}"
    
    def history(self) -> Unigram:
        return Unigram(start=self.start)


class Trigram:
    """Class to represent a trigram in three parts: start, middle and end"""
    __slots__ = ('start', 'middle', 'end')

    def __init__(self, start, middle, end) -> None:
        self.start = start
        self.middle = middle
        self.end = end

    def __eq__(self, other) -> bool:
        return isinstance(other, Trigram) and self.start == other.start and self.middle == other.middle and self.end == other.end
    
    def __lt__(self, other) -> bool:
        if self.start != other.start:
            return self.start < other.start
        elif self.middle != other.middle:
            return self.middle < other.middle
        else:
            return self.end < other.end
        
    def __hash__(self) -> int:
        return hash((self.start, self.middle, self.end))
    
    def __str__(self) -> str:
        return f"Trigram {self.start}{self.middle}{self.end}"
    
    def history(self) -> Bigram:
        return Bigram(start=self.start, end=self.middle)
    
class BigramDistribution:
    """For a given bigram, this class contains the distribution over all possible trigrams that it prefixes.
    For example, for the bigram "in", the distribution would contain the probabilities for all possible trigrams
    beginning with it like "ina", "inb", "inc" etc."""
    __slots__ = ('bigram', 'dist')

    def __init__(self, bigram, dist=None) -> None:
        self.bigram = bigram
        self.dist = dist if dist is not None else {}

    def __str__(self) -> str:
        return f"BigramDistribution for {self.bigram} with {len(self.dist)} trigrams"