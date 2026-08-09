# Doctor Pocket — Model
 
This directory contains the documentation and local deployment information for the trained Doctor Pocket language model.
 
Doctor Pocket is a medical question-answering AI assistant based on:
 
```text
Qwen/Qwen2.5-1.5B-Instruct
```
 
The base model was fine-tuned using QLoRA with a 4-bit NF4 quantized model and a PEFT LoRA adapter.
 
The resulting adapter is used by the FastAPI backend to generate medical-information responses.
 
---
 
## 🧠 Model Overview
 
Doctor Pocket uses the following architecture:
 
```text
Qwen/Qwen2.5-1.5B-Instruct
              │
              ▼
       4-bit NF4 Loading
              │
              ▼
          QLoRA
              │
              ▼
      Doctor Pocket LoRA
          Adapter
              │
              ▼
      FastAPI Inference
              │
              ▼
       Doctor Pocket
          Response
```
 
The project does not create a completely independent full-sized model.
 
Instead, the fine-tuning process produces a relatively small LoRA adapter containing the learned task-specific changes.
 
---
 
## 🤖 Base Model
 
The base language model is:
 
**Qwen/Qwen2.5-1.5B-Instruct**
 
The model is an instruction-following language model designed for conversational and instruction-based tasks.
 
Doctor Pocket uses the instruction-following capabilities of Qwen as the foundation for medical question answering.
 
---
 
## 🔬 Fine-Tuning Method
 
Doctor Pocket was fine-tuned using:
 
**QLoRA**
 
QLoRA combines:
 
- Low-Rank Adaptation (LoRA)
- 4-bit quantization
- Parameter-efficient fine-tuning
Instead of updating all parameters of the language model, LoRA introduces trainable low-rank matrices into selected layers.
 
This significantly reduces the number of trainable parameters and makes fine-tuning possible on limited GPU hardware.
 
---
 
## 📦 Quantization
 
The base model is loaded using:
 
**4-bit quantization**
 
with:
 
- Quantization type: NF4
- Double quantization: Enabled
- Compute dtype: FP16
The configuration uses:
 
```python
BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)
```
 
This configuration was selected specifically to make QLoRA training and inference practical on consumer GPUs and Google Colab T4 GPUs.
 
---
 
## 🧩 LoRA Configuration
 
The Doctor Pocket adapter was configured using PEFT LoRA.
 
The main LoRA configuration includes:
 
- LoRA rank (r): 16
- LoRA alpha: 32
- LoRA dropout: 0.05
The LoRA adapter targets the appropriate attention/projection layers of the Qwen2.5 architecture.
 
The purpose of these trainable modules is to allow the model to adapt to the medical question-answering task without updating the entire base model.
 
---
 
## 🎯 Why LoRA?
 
Full fine-tuning would require updating all parameters of the base model.
 
This would require significantly more:
 
- GPU memory
- Training time
- Storage
- Computational resources
LoRA instead trains a small number of additional parameters.
 
Conceptually:
 
```text
Original Model
      │
      ├── Frozen Base Parameters
      │
      └── Trainable LoRA Parameters
                    │
                    ▼
             Fine-Tuned Model
```
 
The original Qwen model remains frozen while the LoRA adapter learns the task-specific behavior.
 
---
 
## 🖥️ Training Hardware
 
The training configuration was designed for a free Google Colab environment using an NVIDIA T4 GPU.
 
Target hardware:
 
- GPU: NVIDIA Tesla T4
- VRAM: approximately 16 GB
- Precision: FP16
- Quantization: 4-bit NF4
The project was designed to minimize GPU memory usage while maintaining practical training performance.
 
---
 
## 📊 Training Configuration
 
The main training configuration was:
 
| Parameter | Value |
|-----------|-------|
| Base model | Qwen/Qwen2.5-1.5B-Instruct |
| Fine-tuning method | QLoRA |
| Quantization | 4-bit NF4 |
| Double quantization | Enabled |
| Compute dtype | FP16 |
| Epochs | 1 |
| Maximum sequence length | 1024 |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Learning rate | Approximately 2e-4 |
| Warmup ratio | Approximately 0.03 |
| Weight decay | 0.01 |
| Train batch size | 2 |
| Gradient accumulation | 8 |
| Effective batch size | 16 |
 
The exact training configuration is also stored with the training artifacts when available.
 
---
 
## 📚 Dataset
 
Doctor Pocket was trained on a medical question-answering dataset.
 
The original dataset contained approximately:
 
- 13,096 training examples
- 1,637 validation examples
The final training workflow uses a random:
 
- 80% Train
- 10% Validation
- 10% Test
split using:
 
```text
seed = 42
```
 
The test set is kept separate from the training process and is only used for final evaluation.
 
---
 
## 🔀 Dataset Split
 
The intended data pipeline is:
 
```text
Medical Q&A Dataset
        │
        ▼
   Random Split
        │
   ┌────┼────┐
   ▼    ▼    ▼
  80%  10%  10%
 Train Val  Test
   │    │    │
   │    │    │
   ▼    ▼    ▼
Training Evaluation
          Test
```
 
The test set is not used for gradient updates during fine-tuning.
 
---
 
## 💬 Training Prompt Format
 
Doctor Pocket uses the official Qwen chat-template format.
 
A training example is conceptually structured as:
 
```text
System:
[Doctor Pocket system instructions]
 
User:
[Medical question]
 
Assistant:
[Medical answer]
```
 
The tokenizer's official chat template is used rather than manually constructing an incompatible prompt format.
 
This allows the fine-tuned model to preserve the conversational behavior expected from the Qwen instruction model.
 
---
 
## 🩺 Doctor Pocket System Prompt
 
The model is guided by the following system prompt during inference:
 
```text
You are Doctor Pocket, an AI medical information assistant.
Provide clear, cautious, educational medical information.
Do not claim to replace a doctor.
For emergencies or serious symptoms, advise the user to seek professional medical care.
Do not invent medical facts.
```
 
The purpose of this prompt is to encourage:
 
- Educational responses.
- Cautious language.
- Appropriate medical disclaimers.
- Emergency-care recommendations when appropriate.
- Avoidance of unsupported medical claims.
---
 
## 📏 Sequence Length
 
The maximum sequence length used for training is:
 
**1024 tokens**
 
This was selected as a practical compromise between:
 
- Context size
- GPU memory usage
- Training speed
- Information retention
Longer sequences increase memory requirements and can significantly slow training on a free T4 GPU.
 
---
 
## 🏋️ Training
 
The model was fine-tuned for:
 
**1 epoch**
 
The training process uses gradient accumulation to achieve a larger effective batch size while keeping the per-device batch size small enough for the available GPU memory.
 
The intended configuration is approximately:
 
- Per-device batch size: 2
- Gradient accumulation: 8
Effective batch size:
 
```text
2 × 8 = 16
```
 
---
 
## 📈 Evaluation
 
The model was evaluated using previously unseen medical questions.
 
The evaluation included ten manually selected questions covering multiple medical topics:
 
| # | Topic | Result |
|---|-------|--------|
| 1 | Dehydration | Good |
| 2 | High blood pressure | Good |
| 3 | Type 2 diabetes | Good |
| 4 | Cold vs. flu | Good |
| 5 | Vitamin D deficiency | Good |
| 6 | Headaches | Good |
| 7 | Pneumonia | Good |
| 8 | Minor burn | Bad — repeated information |
| 9 | Asthma | Good |
| 10 | Emergency chest pain | Good — acceptable but not optimal |
 
The results indicate that the model can provide useful general medical information across several topics.
 
However, the minor-burn example demonstrated repetitive-generation behavior, and the emergency chest-pain response still has room for improvement.
 
---
 
## ⚠️ Evaluation Limitations
 
The evaluation above is a qualitative project-level evaluation.
 
It is not clinical validation.
 
Medical AI systems require significantly more extensive testing before they can be considered appropriate for real-world clinical use.
 
Text-generation metrics such as:
 
- BLEU
- ROUGE
cannot by themselves determine whether a medical answer is clinically correct or safe.
 
A future version should include evaluation by qualified medical professionals and dedicated medical safety benchmarks.
 
---
 
## 💾 Model Files
 
The trained LoRA adapter is stored locally in:
 
```text
doctor_pocket_qwen25_1_5b_lora/
```
 
The directory may contain files such as:
 
```text
doctor_pocket_qwen25_1_5b_lora/
│
├── adapter_config.json
├── adapter_model.safetensors
├── tokenizer_config.json
├── tokenizer.json
├── special_tokens_map.json
└── ...
```
 
The exact files depend on the versions of Transformers and PEFT used during training.
 
---
 
## 🚫 Why the Model Weights Are Not Included on GitHub
 
The actual model weights are intentionally excluded from the GitHub repository.
 
The `.gitignore` contains:
 
```text
model/doctor_pocket_qwen25_1_5b_lora/
```
 
This prevents large model-weight files from being accidentally committed to GitHub.
 
The model directory therefore remains available locally while the repository contains the documentation required to understand the model.
 
The structure is:
 
```text
model/
│
├── README.md
│
└── doctor_pocket_qwen25_1_5b_lora/
    ├── adapter_config.json
    ├── adapter_model.safetensors
    └── ...
```
 
The adapter directory is ignored by Git, while this README remains tracked.
 
---
 
## 🔗 Loading the Model
 
The FastAPI backend loads the model using:
 
- `AutoTokenizer`
- `AutoModelForCausalLM`
- `PeftModel`
The loading process is:
 
```text
Load tokenizer
      │
      ▼
Load Qwen base model
      │
      ▼
Apply 4-bit NF4 quantization
      │
      ▼
Load Doctor Pocket LoRA adapter
      │
      ▼
Set model to evaluation mode
      │
      ▼
Generate responses
```
 
---
 
## 🧠 Model Loading Example
 
The basic architecture used by the backend is:
 
```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
 
from peft import PeftModel
```
 
The base model is:
 
```python
BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
```
 
The LoRA adapter is loaded on top of the base model:
 
```python
model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
)
```
 
---
 
## ⚡ Inference
 
During inference, the backend:
 
1. Receives a medical question.
2. Adds the Doctor Pocket system prompt.
3. Applies the Qwen chat template.
4. Tokenizes the prompt.
5. Runs the model on the available device.
6. Generates the response.
7. Decodes the generated tokens.
8. Returns the answer to the frontend.
The inference pipeline is:
 
```text
User Question
      │
      ▼
System Prompt
      │
      ▼
Qwen Chat Template
      │
      ▼
Tokenizer
      │
      ▼
Doctor Pocket Model
      │
      ▼
Generated Tokens
      │
      ▼
Decoded Answer
      │
      ▼
FastAPI
      │
      ▼
React Frontend
```
 
---
 
## ⚙️ Generation Parameters
 
The current backend uses generation settings similar to:
 
```text
max_new_tokens: 256
temperature: 0.7
top_p: 0.9
repetition_penalty: 1.1
```
 
These parameters control the behavior of the generated response.
 
In particular, the repetition penalty is used to reduce repetitive outputs.
 
Further tuning may improve problematic cases such as the minor-burn evaluation example.
 
---
 
## 🔄 Adapter vs. Full Model
 
Doctor Pocket uses a LoRA adapter rather than storing a completely independent full model.
 
### LoRA Adapter
 
Contains:
 
- Task-specific learned parameters
Advantages:
 
- Smaller storage requirement.
- Faster to save.
- Easier to distribute.
- Can be loaded on top of the original base model.
- Keeps the original model separate.
### Merged Model
 
A merged model combines:
 
```text
Base Model + LoRA Adapter
```
 
into a single model.
 
Advantages:
 
- Simpler deployment in some environments.
- No separate adapter loading step.
Disadvantages:
 
- Larger storage requirement.
- Requires additional memory during merging.
- Less flexible than keeping the adapter separate.
For Doctor Pocket, the LoRA adapter is the primary deployment artifact.
 
---
 
## 🚀 Backend Integration
 
The model is designed to be loaded by the Doctor Pocket FastAPI backend.
 
The backend is located at:
 
```text
../backend/
```
 
The general architecture is:
 
```text
React Frontend
      │
      │ POST /api/chat
      ▼
FastAPI Backend
      │
      ▼
Qwen Base Model
      +
Doctor Pocket LoRA
      │
      ▼
Generated Medical Information
      │
      ▼
React Frontend
```
 
See:
 
```text
../backend/README.md
```
 
for complete backend documentation.
 
---
 
## 🧪 Example Inference
 
Example question:
 
```text
What are common symptoms of iron deficiency anemia?
```
 
The model generates an educational response describing common symptoms such as fatigue and other possible signs.
 
The exact response may vary because generation uses sampling.
 
The model should not be interpreted as providing a medical diagnosis.
 
---
 
## 🧰 Training Technologies
 
The Doctor Pocket training pipeline uses:
 
| Technology | Purpose |
|------------|---------|
| PyTorch | Deep learning framework |
| Transformers | Model and tokenizer |
| Datasets | Dataset processing |
| PEFT | LoRA implementation |
| TRL | Supervised fine-tuning |
| Accelerate | Training/device management |
| BitsAndBytes | 4-bit quantization |
| Hugging Face Hub | Model/tokenizer access |
| Matplotlib | Training visualization |
| scikit-learn | Supporting evaluation/data utilities |
 
---
 
## 📓 Training Notebook
 
The training workflow was developed as a Google Colab notebook designed for an NVIDIA T4 GPU.
 
The notebook covers:
 
```text
Environment setup
        ↓
Dependency installation
        ↓
GPU verification
        ↓
Dataset loading
        ↓
Dataset inspection
        ↓
Dataset preprocessing
        ↓
80/10/10 split
        ↓
Tokenizer
        ↓
Qwen model loading
        ↓
QLoRA configuration
        ↓
Training
        ↓
Evaluation
        ↓
Model saving
        ↓
Inference testing
        ↓
FastAPI preparation
```
 
The notebook is stored in:
 
```text
../notebooks/
```
 
---
 
## 📁 Model Directory Structure
 
The expected local structure is:
 
```text
model/
│
├── README.md
│
└── doctor_pocket_qwen25_1_5b_lora/
    │
    ├── adapter_config.json
    ├── adapter_model.safetensors
    ├── tokenizer_config.json
    ├── tokenizer.json
    ├── special_tokens_map.json
    └── ...
```
 
The adapter directory is excluded from GitHub using `.gitignore`.
 
---
 
## 🔐 Model Security
 
The model directory should never contain:
 
- Hugging Face access tokens.
- API keys.
- Passwords.
- Private credentials.
- `.env` files.
Authentication credentials should be stored separately and never committed to source control.
 
---
 
## 📦 Deployment
 
The recommended deployment architecture is:
 
```text
                   Production System
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       React Frontend        FastAPI Backend
                                    │
                                    ▼
                          Doctor Pocket Model
                                    │
                           ┌────────┴────────┐
                           │                 │
                           ▼                 ▼
                     Qwen Base        LoRA Adapter
```
 
The FastAPI backend loads the model once when the server starts.
 
It does not reload the model for every request.
 
---
 
## 🔮 Future Model Improvements
 
Potential improvements include:
 
### Training
 
- Larger and higher-quality medical datasets.
- Better dataset filtering.
- Removal of duplicated examples.
- More epochs if justified by validation performance.
- Hyperparameter optimization.
- Improved instruction formatting.
- Better handling of long answers.
### Generation
 
- Improved repetition control.
- Better emergency-response behavior.
- More deterministic generation for safety-sensitive questions.
- Response length control.
- Streaming generation.
### Medical Safety
 
- Medical safety classifiers.
- Retrieval-Augmented Generation.
- Verified medical knowledge sources.
- Human medical review.
- Medical benchmark evaluation.
- Emergency-intent detection.
---
 
## ⚠️ Medical Safety
 
Doctor Pocket is an educational and research prototype.
 
It is not intended to:
 
- Diagnose medical conditions.
- Replace physicians.
- Prescribe medication.
- Recommend individualized treatment.
- Make emergency medical decisions.
- Replace professional medical care.
The model can generate incorrect, incomplete, outdated, or misleading information.
 
For serious or emergency symptoms, users should seek professional medical care.
 
---
 
## 📌 Model Summary
 
| Property | Value |
|----------|-------|
| Model | Qwen/Qwen2.5-1.5B-Instruct |
| Fine-Tuning | QLoRA |
| Quantization | 4-bit NF4 |
| Double Quantization | Enabled |
| Compute Precision | FP16 |
| LoRA Rank | 16 |
| LoRA Alpha | 32 |
| LoRA Dropout | 0.05 |
| Training Epochs | 1 |
| Maximum Sequence Length | 1024 |
| Dataset Split | 80% Train / 10% Validation / 10% Test |
| Random Seed | 42 |
| Primary Deployment | FastAPI + React |
 
---
 
## 🔗 Related Documentation
 
Complete project documentation:
 
```text
../README.md
```
 
Backend documentation:
 
```text
../backend/README.md
```
 
Frontend documentation:
 
```text
../frontend/README.md
```
 
Training notebook:
 
```text
../notebooks/
```
 
---
 
## 👨‍💻 Doctor Pocket
 
**Doctor Pocket — Medical AI Assistant**
 
Doctor Pocket demonstrates an end-to-end AI application pipeline:
 
```text
Medical Dataset
      ↓
Data Preprocessing
      ↓
Instruction Formatting
      ↓
Qwen2.5-1.5B-Instruct
      ↓
QLoRA Fine-Tuning
      ↓
LoRA Adapter
      ↓
4-bit Inference
      ↓
FastAPI
      ↓
React
      ↓
Medical Q&A Application
```
 
The project demonstrates how a relatively small instruction-following language model can be adapted for a specialized medical question-answering application using parameter-efficient fine-tuning.
 
---
 
## ⚠️ Final Disclaimer
 
Doctor Pocket is an educational and research project.
 
The model is not a medical professional and does not provide professional medical advice, diagnosis, or treatment.
 
AI-generated medical information should always be verified with a qualified healthcare professional.
 
In emergencies or situations involving serious symptoms, seek professional medical care immediately.