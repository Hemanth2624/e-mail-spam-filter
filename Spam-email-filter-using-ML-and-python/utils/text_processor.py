import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize NLTK resources
required_packages = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']

def download_nltk_data():
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}' if package == 'punkt' 
                          else f'corpora/{package}' if package in ['stopwords', 'wordnet']
                          else f'taggers/{package}')
        except LookupError:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)

# Download required NLTK data
download_nltk_data()

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()

        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        try:
            # Tokenization
            tokens = word_tokenize(text)

            # Remove stopwords and lemmatize
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                     if token not in self.stop_words]

            return ' '.join(tokens)
        except Exception as e:
            print(f"Error in text preprocessing: {str(e)}")
            return text  # Return original text if processing fails

    def extract_features(self, text):
        # Basic feature extraction
        features = {
            'has_urgent': 1 if any(word in text.lower() for word in ['urgent', 'immediate', 'important']) else 0,
            'has_money': 1 if any(word in text.lower() for word in ['money', 'cash', 'dollar', 'prize', 'bank', 'account']) else 0,
            'has_action_required': 1 if any(word in text.lower() for word in ['click', 'sign', 'verify', 'confirm', 'validate']) else 0,
            'has_sensitive': 1 if any(word in text.lower() for word in ['password', 'credit', 'ssn', 'account', 'security']) else 0,
            'length': len(text.split()),
            'caps_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }
        return features