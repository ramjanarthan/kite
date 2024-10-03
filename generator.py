import random

def sample(dist):
    """Given a map of {key: probability} representing a distribution, return a random key based on that distribution"""
    # step 1: generate a random number from 0 - 1
    # step 2: find out which probabiity range it lies in
    # step 3: return that key

    y = random.random()
    max = 0

    for (key, value) in sorted(dist.items()):
        max += value
        if y <= max:
            return key
    
    return dist.keys()[-1]

test_dist = {
    "a": 0.4,
    "b": 0.2,
    "c": 0.2,
    "d": 0.1,
    "e": 0.1,
}

counts = {
    "a": 0,
    "b": 0,
    "c": 0,
    "d": 0,
    "e": 0
}

# for _ in range(1, 20):
#     output = sample(test_dist)
#     counts[output] += 1
#     print(output)

# print(counts)