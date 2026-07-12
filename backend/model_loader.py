import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from config import BASE_MODEL, ADAPTER_MODEL

model = None
tokenizer = None


def load_model():
    global model, tokenizer

    if model is not None:
        return model, tokenizer

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading base model...")

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    print("Loading DPO adapter...")

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL,
    )

    model.eval()

    print("✅ Model loaded successfully!")

    return model, tokenizer