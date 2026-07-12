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

    # Create chat prompt
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    # Move tensors to model device
    inputs = {
        k: v.to(model.device)
        for k, v in inputs.items()
    }

    # Generate response
    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode ONLY the newly generated tokens
    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()

    # Remove any remaining assistant tag
    if answer.lower().startswith("assistant"):
        answer = answer[len("assistant"):].strip()

    if answer.startswith(":"):
        answer = answer[1:].strip()

    return answer