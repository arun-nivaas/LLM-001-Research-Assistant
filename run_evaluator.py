from evaluator_retreiver import RetrieverEvaluator
from rag_pipeline import PDFQA  

# Load PDF text
with open("evaluation_text.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

# Initialize your PDFQA pipeline
pdfqa = PDFQA(pdf_text)

# Initialize evaluator
evaluator = RetrieverEvaluator(pdfqa.retriever)

# Define benchmark queries
benchmark = [
    {
        "query": "What is positional encoding?",
        "answer": (
            "Positional Encoding is a d_model-dimensional vector that is added element-wise "
            "to each token embedding at the input of the encoder and decoder (E_token + PE_pos). "
            "Because the self-attention mechanism itself is order-agnostic, positional encodings "
            "provide the model with information about the position of each token in the sequence. "
            "The encoding is defined using fixed sine and cosine functions of varying frequencies: "
            "PE(pos,2i) = sin(pos / 10000^(2i/d_model)), PE(pos,2i+1) = cos(pos / 10000^(2i/d_model)), "
            "where pos is the token position and i is the dimension index. "
            "This sinusoidal design allows relative positions to be expressed as linear combinations "
            "of encodings and enables the model to generalize to sequence lengths longer than those "
            "seen during training, because the function is fixed and not learned."
        )
    }
]

# Run evaluation

results = evaluator.evaluate(benchmark, k=5)
print("Evaluation Results:", results)
