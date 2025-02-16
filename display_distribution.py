from custom_model import CustomLanguageModel
from constants import *
from primitives import *
import matplotlib.pyplot as plt

python_model = CustomLanguageModel.load_model(python_model_file) # CustomLanguageModel(processed_train_files[0])
cpp_model = CustomLanguageModel.load_model(cpp_model_file) # CustomLanguageModel(processed_train_files[1])

# ---------------------------
# 'def' in python

# Extract the trigrams and their probabilities
trigram_probabilities = python_model.distribution_map[Bigram("d", "e")].dist.items()

# Sort the trigrams by probability in descending order
sorted_trigrams = sorted(trigram_probabilities, key=lambda x: x[1], reverse=True)

# Separate the top 10 trigrams and the rest
top_10_trigrams = sorted_trigrams[:10]
other_trigrams = sorted_trigrams[10:]

# Prepare the data for plotting
x_values = [trigram.end for trigram, _ in top_10_trigrams] + ['Others']
y_values = [probability for _, probability in top_10_trigrams] + [sum(probability for _, probability in other_trigrams)]

# Plot the graph
plt.figure(figsize=(10, 5))
plt.bar(x_values, y_values, color='blue')
plt.xlabel('Trigram End')
plt.ylabel('Probability')
plt.title('Trigram Probabilities starting with "de"')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/def_python_dist.png')

# ---------------------------
# '#in' in c++

# Extract the trigrams and their probabilities
trigram_probabilities = cpp_model.distribution_map[Bigram("#", "i")].dist.items()

# Sort the trigrams by probability in descending order
sorted_trigrams = sorted(trigram_probabilities, key=lambda x: x[1], reverse=True)

# Separate the top 10 trigrams and the rest
top_10_trigrams = sorted_trigrams[:10]
other_trigrams = sorted_trigrams[10:]

# Prepare the data for plotting
x_values = [trigram.end for trigram, _ in top_10_trigrams] + ['Others']
y_values = [probability for _, probability in top_10_trigrams] + [sum(probability for _, probability in other_trigrams)]

# Plot the graph
plt.figure(figsize=(10, 5))
plt.bar(x_values, y_values, color='blue')
plt.xlabel('Trigram End')
plt.ylabel('Probability')
plt.title('Trigram Probabilities starting with "#i"')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/#in_cpp_dist.png')
