from rouge_score import rouge_scorer
from bert_score import score



def compute_rouge_scores(reference_answers, generated_answers):

    scorer = rouge_scorer.RougeScorer(['rouge1','rouge2','rougeL'], use_stemmer=True)
    scores = scorer.score(reference_answers, generated_answers)

    # Extract precision, recall, f1 for each ROUGE type
    rouge1_f1 = scores["rouge1"].fmeasure
    rouge2_f1 = scores["rouge2"].fmeasure
    rougel_f1 = scores["rougeL"].fmeasure

    # Return a clean summary instead of spamming prints
    return {
        "ROUGE-1": round(float(rouge1_f1), 4),
        "ROUGE-2": round(float(rouge2_f1), 4),
        "ROUGE-L": round(float(rougel_f1), 4),
    }

def bert_score(reference_answers, generated_answers):
    
    P, R, F1 = score([generated_answers], [reference_answers], lang='en', verbose=True)
    return {
        "BERTScore_Precision": round(float(P.mean()), 4),
        "BERTScore_Recall": round(float(R.mean()), 4),
        "BERTScore_F1": round(float(F1.mean()), 4),
    }
    