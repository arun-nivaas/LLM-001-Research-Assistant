from fastapi import APIRouter, HTTPException
from evaluators.evaluator_retreiver import RetrieverEvaluator
from services.rag_pipeline import PDFQA
from typing import Any, Dict, cast, List
import numpy as np

router = APIRouter(tags=["Evaluation"])

@router.post("/")
async def evaluate_rag(k: int = 12, threshold: float = 0.7) -> Dict[str, Any]:
    """
    Endpoint to evaluate the retriever performance using benchmark queries.
    """

    try:
        # Load sample evaluation text
        with open("evaluation_text.txt", "r", encoding="utf-8") as f:
            pdf_text = f.read()

        # Initialize PDFQA pipeline and evaluator
        pdfqa = PDFQA(pdf_text)
        evaluator = RetrieverEvaluator(pdfqa.retriever)

        # Define a benchmark (you can later move this to a JSON input)
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
        results = evaluator.evaluate(benchmark, k=k, similarity_threshold=threshold)

        # ✅ Convert all numpy data types to native Python (float/int)
        def convert_numpy(obj: Any) -> Any:
            # np.generic covers numpy scalar types like np.float32, np.int64, etc.
            if isinstance(obj, (np.generic,)):
                return obj.item()
            elif isinstance(obj, dict):
                # help static type checkers by casting to a known mapping type
                return {k: convert_numpy(v) for k, v in cast(Dict[Any, Any], obj).items()}
            elif isinstance(obj, list):
                # cast the list to List[Any] so the comprehension variable has a known type
                return [convert_numpy(v) for v in cast(List[Any], obj)]
            return obj

        clean_results = convert_numpy(results)

        return {"status": "success", "metrics": clean_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
