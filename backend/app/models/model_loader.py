import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

# backend/app/models/model_loader.py
# Project root is three levels above this file:
# models -> app -> backend -> Doctor Pocket
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

ADAPTER_PATH = PROJECT_ROOT / "model" / "doctor_pocket_qwen25_1_5b_lora"


DOCTOR_POCKET_SYSTEM_PROMPT = (
    "You are Doctor Pocket, an AI medical information assistant. "
    "Provide accurate, concise, cautious, and educational medical information. "
    "Answer only what the user asks and avoid adding unrelated symptoms or conditions. "
    "Do not invent medical facts, diagnoses, medications, treatments, or test results. "
    "When discussing symptoms, distinguish common symptoms from less common or severe symptoms. "
    "Do not claim to diagnose the user or replace a qualified healthcare professional. "
    "If symptoms could indicate an emergency or serious condition, clearly advise "
    "the user to seek appropriate professional medical care. "
    "If you are uncertain about a medical fact, say that you are uncertain rather "
    "than guessing."
)


_model = None
_tokenizer = None


def get_model_and_tokenizer():
    """
    Load the Doctor Pocket model once and reuse it.

    The model consists of:
    - Qwen2.5-1.5B-Instruct base model
    - Doctor Pocket LoRA adapter
    """

    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    print("=" * 60)
    print("Loading Doctor Pocket model...")
    print("=" * 60)

    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # ---------------------------------------------------------
    # Tokenizer
    # ---------------------------------------------------------

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)

    print("Tokenizer loaded.")

    # ---------------------------------------------------------
    # Qwen base model
    # ---------------------------------------------------------

    print("\nLoading Qwen base model...")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )

    print("Base model loaded.")

    # ---------------------------------------------------------
    # Doctor Pocket LoRA adapter
    # ---------------------------------------------------------

    print("\nLoading Doctor Pocket LoRA adapter...")

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_PATH,
    )

    model.eval()

    print("Doctor Pocket adapter loaded successfully!")

    # Cache the loaded model
    _model = model
    _tokenizer = tokenizer

    print("\nDoctor Pocket model is ready.")

    return _model, _tokenizer


def generate_answer(
    question: str,
    max_new_tokens: int = 256,
) -> str:

    model, tokenizer = get_model_and_tokenizer()

    messages = [
        {
            "role": "system",
            "content": DOCTOR_POCKET_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(model.device)

    print("\nGenerating answer...")

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.pad_token_id,
        )

    generated = output_ids[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated,
        skip_special_tokens=True,
    ).strip()

    return answer