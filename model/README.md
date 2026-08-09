# Doctor Pocket - Qwen2.5-1.5B-Instruct LoRA Adapter

## Overview
Doctor Pocket is a **research / educational prototype** medical question-answering assistant.
It is a QLoRA fine-tune of `Qwen/Qwen2.5-1.5B-Instruct` and is **not** a substitute for professional medical advice.

## Base model
- `Qwen/Qwen2.5-1.5B-Instruct`

## Fine-tuning method
- QLoRA: base model loaded in 4-bit NF4 (double quantization), LoRA adapters trained in fp16.
- LoRA rank: 16, alpha: 32, dropout: 0.05
- Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj

## Dataset
- Source: `MedicalQuestionAnswering.csv` (16,358 examples after cleaning)
- Split: 13,086 train / 1,636 validation / 1,636 test (80/10/10, stratified by topic, seed=42)

## Training
- Epochs: 1
- Effective batch size: 16 (per-device 2 x 8 accumulation)
- Learning rate: 0.0002
- Sequence length: 1024
- Final training loss: 0.8481
- Training time: 192.9 minutes
- Training date: 2026-08-08T14:01:16.785524 UTC

## Inference instructions
Load the base model in 4-bit (or fp16) and apply this adapter with PEFT:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("/content/doctor_pocket_qwen25_1_5b_lora")
model = PeftModel.from_pretrained(base_model, "/content/doctor_pocket_qwen25_1_5b_lora")

messages = [
    {"role": "system", "content": "You are Doctor Pocket, an AI medical information assistant. Provide clear, cautious, educational medical information. Do not claim to replace a doctor. For emergencies or serious symptoms, advise the user to seek professional medical care. Do not invent medical facts."},
    {"role": "user", "content": "What are common symptoms of iron deficiency anemia?"},
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(output[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True))
```

See `backend/` (Section 23 of the training notebook) for a ready-to-run FastAPI server built on top
of this exact adapter.

## ⚠️ Medical safety warning
This is a research/educational medical assistant. It has **not** been clinically validated.
Do not use it for real diagnosis, treatment decisions, or in place of professional medical care.
For emergencies, contact real emergency services.
