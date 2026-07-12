import torch

from config import (
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
)

from model_loader import load_model


def generate_answer(question: str):

    model, tokenizer = load_model()

    messages = [
        {
            "role": "user",
            "content": question,
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    if answer.startswith(prompt):
        answer = answer[len(prompt):].strip()

    return answer