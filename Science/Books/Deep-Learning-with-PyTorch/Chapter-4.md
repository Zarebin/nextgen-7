# 4.1: working with images
- Representing images with a 2D tensor for grayscale pictures (1 channel) and a 3D tensor for RGB pictures (3 channels).
 - Normalizing data will help model training. it can be done by subtracting the mean and dividing to std.
# 4.2: 3D images
- An extra dimension for depth.

# 4.3: Representing tabular data
- Use a tensor for loading tabular files like CSV.
- Continuous, ordinal, and categorical values.
- One hot encoding for categorical numbers.

# 4.4: Working with time series
- Use a tensor with a sorted axis by time.

# 4.5: Representing text
- Natural language processing (NLP): 1- RNN 2-Transformer
how to convert texts to numbers? 
-  One-hot-encoding characters: Can not understand semantics.
- One-hot encoding whole words: Long and sparse vectors, can't add new tokens.
- Text embeddings: Understand semantics and represent each token with a vector with a bound size. Words with similar meanings have similar embeddings and their vectors are close together in vector space. BERT and GPT can be used for finding embeddings. These models understand words' meanings in their nearby words and can detect more relation between words. 
