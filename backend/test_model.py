import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = "model/doctor_pocket_qwen25_1_5b_lora"
print("=" * 60)
print("DOCTOR POCKET — MODEL TEST")
print("=" * 60)

print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)

print("Tokenizer loaded.")

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

print("\nLoading Doctor Pocket LoRA adapter...")

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
)

model.eval()

print("Doctor Pocket adapter loaded successfully!")

question = "What are common symptoms of iron deficiency anemia?"

messages = [
    {
        "role": "system",
        "content": (
            "You are Doctor Pocket, an AI medical information assistant. "
            "Provide clear, cautious, educational medical information. "
            "Do not claim to replace a doctor. "
            "For emergencies or serious symptoms, advise the user to seek "
            "professional medical care. Do not invent medical facts."
        ),
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
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.pad_token_id,
    )

answer = tokenizer.decode(
    output_ids[0][inputs["input_ids"].shape[1]:],
    skip_special_tokens=True,
).strip()

print("\n" + "=" * 60)
print("USER:")
print(question)
print("\nDOCTOR POCKET:")
print(answer)
print("=" * 60)

print("\nGPU MEMORY:")
print(
    f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB allocated"
)