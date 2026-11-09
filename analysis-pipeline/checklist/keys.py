import uuid

META_SK = "META"

def new_id() -> str:
    return uuid.uuid4().hex[:8]

def question_sk(qid: str) -> str:
    return f"Q#{qid}"
