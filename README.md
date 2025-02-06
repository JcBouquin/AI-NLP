# AI-NLP

Natural Language Processing (NLP) project incorporating various components for text processing, language understanding, and conversational AI.

## Project Structure

### Agents
Conversational agents and dialogue systems implementation:
- Task-oriented dialogue systems
- Open-domain chatbots
- Custom agent frameworks

### Langchain
Integration with LangChain framework for building NLP applications:
- Document processing
- Prompt engineering
- Chain management
- Vector stores integration

### Transformers
Implementation and fine-tuning of Transformer models:
- BERT implementations
- Custom model training
- Task-specific adaptations
- 
### Coursera-NLP-specialisation
Implementation of NLP techniques and exercises from Coursera specialization:
- Text classification
- Named Entity Recognition (NER)
- Machine translation
- Sentiment analysis
- Musique generation
  

## Prerequisites

### Python Environment
- Python 3.8+
- virtualenv or conda

### Core Dependencies
```txt
torch>=2.0.0
transformers>=4.30.0
langchain>=0.0.300
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.2.0
spacy>=3.5.0
```

### Optional Dependencies
```txt
pytorch-lightning>=2.0.0
wandb>=0.15.0
ray>=2.5.0
fastapi>=0.100.0
```

### GPU Support (Recommended)
- CUDA 11.7+
- cuDNN 8.5+
- GPU with minimum 8GB VRAM

## Installation

```bash
git clone https://github.com/JcBouquin/AI-NLP.git
cd AI-NLP
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

 
