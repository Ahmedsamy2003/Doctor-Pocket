# Doctor Pocket — Backend
 
The Doctor Pocket backend is a FastAPI-based REST API that connects the React frontend to the fine-tuned Doctor Pocket medical question-answering model.
 
The backend is responsible for:
 
- Loading the Qwen2.5-1.5B-Instruct base model.
- Loading the Doctor Pocket LoRA adapter.
- Running inference using 4-bit NF4 quantization.
- Processing medical questions.
- Generating educational medical-information responses.
- Providing API endpoints for health checks and text generation.
- Connecting the React frontend to the AI model.
- Loading the model once and reusing it for subsequent requests.
---
 
## 🧠 Backend Architecture
 
```text
                         Doctor Pocket
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             React Frontend        FastAPI Backend
             localhost:5173       localhost:8000
                    │                   │
                    │      HTTP         │
                    └────────►─────────┘
                                        │
                                        ▼
                              Doctor Pocket Model
                                        │
                              ┌─────────┴─────────┐
                              │                   │
                              ▼                   ▼
                    Qwen2.5-1.5B-Instruct   LoRA Adapter
                              │                   │
                              └─────────┬─────────┘
                                        │
                                        ▼
                                  AI Response
```
 
---
 
## 🤖 Language Model
 
The backend uses:
 
**Qwen/Qwen2.5-1.5B-Instruct**
 
as the base language model.
 
Doctor Pocket was fine-tuned using QLoRA, producing a LoRA adapter that is loaded on top of the original Qwen model.
 
The inference architecture is therefore:
 
```text
Qwen2.5-1.5B-Instruct
          +
Doctor Pocket LoRA Adapter
          ↓
   Doctor Pocket Model
          ↓
      AI Response
```
 
---
 
## ⚙️ Model Loading
 
The backend uses the following technologies for model loading and inference:
 
- PyTorch
- Hugging Face Transformers
- PEFT
- BitsAndBytes
The base model is loaded using:
 
- 4-bit quantization
- NF4 quantization
- Double quantization
- FP16 compute
This significantly reduces the memory required to run the model compared with loading the model entirely in higher precision.
 
The backend uses automatic device placement when CUDA is available.
 
---
 
## 🖥️ GPU Support
 
The backend automatically detects whether CUDA is available.
 
During development, Doctor Pocket was successfully tested using an NVIDIA GeForce RTX 4050 Laptop GPU.
 
Example startup output:
 
```text
CUDA available: True
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
```
 
When CUDA is available, the model uses the NVIDIA GPU for inference.
 
---
 
## 📁 Backend Structure
 
The backend is organized approximately as follows:
 
```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── ...
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── model_loader.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── ...
│   │
│   └── main.py
│
├── requirements.txt
├── .env
├── venv/
└── README.md
```
 
The following files/directories are intentionally excluded from GitHub:
 
```text
venv/
.env
__pycache__/
```
 
---
 
## 🚀 Running the Backend
 
### 1. Open the Project Directory
 
From PowerShell:
 
```powershell
cd "D:\AI\Doctor Pocket"
```
 
### 2. Activate the Backend Virtual Environment
 
Run:
 
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```
 
The terminal should then show:
 
```text
(venv)
```
 
### 3. Return to the Project Root
 
Run:
 
```powershell
cd ..
```
 
You should now be at:
 
```text
D:\AI\Doctor Pocket
```
 
### 4. Start the FastAPI Server
 
Run:
 
```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```
 
The backend should start at:
 
```text
http://127.0.0.1:8000
```
 
A successful startup will load the tokenizer, base model, and Doctor Pocket LoRA adapter.
 
Typical startup messages include:
 
```text
Starting Doctor Pocket API...
 
Loading Doctor Pocket model...
 
CUDA available: True
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
 
Loading tokenizer...
Tokenizer loaded.
 
Loading Qwen base model...
Base model loaded.
 
Loading Doctor Pocket LoRA adapter...
Doctor Pocket adapter loaded successfully!
 
Doctor Pocket model is ready.
Doctor Pocket API is ready!
```
 
---
 
## 📚 FastAPI Documentation
 
FastAPI automatically provides interactive API documentation.
 
Once the backend is running, open:
 
```text
http://127.0.0.1:8000/docs
```
 
This opens the Swagger UI.
 
Swagger allows the API endpoints to be tested directly from the browser without using the React frontend.
 
---
 
## ❤️ Health Check Endpoint
 
Doctor Pocket provides a health-check endpoint:
 
```http
GET /api/health
```
 
Open:
 
```text
http://127.0.0.1:8000/api/health
```
 
This endpoint is used to verify that the FastAPI backend is running correctly.
 
A successful response indicates that the backend is available.
 
---
 
## 🧬 Generate Endpoint
 
The backend provides a direct model-generation endpoint:
 
```http
POST /api/generate
```
 
The endpoint accepts a medical question.
 
**Request**
 
```json
{
  "question": "What are common symptoms of iron deficiency anemia?"
}
```
 
**Response**
 
```json
{
  "answer": "The most common symptom of iron deficiency anemia is fatigue..."
}
```
 
The exact generated answer may vary between requests because the model uses sampling during generation.
 
---
 
## 💬 Chat Endpoint
 
The React frontend communicates with the backend through:
 
```http
POST /api/chat
```
 
The frontend sends:
 
```json
{
  "question": "What are the symptoms of dehydration?"
}
```
 
The backend processes the question using the Doctor Pocket model and returns:
 
```json
{
  "answer": "..."
}
```
 
The React frontend then displays the answer inside the Doctor Pocket conversation interface.
 
---
 
## 🔄 Request Flow
 
A typical Doctor Pocket request follows this process:
 
```text
User enters a medical question
              │
              ▼
       React Frontend
              │
              │ POST /api/chat
              ▼
       FastAPI Backend
              │
              ▼
       Question Processing
              │
              ▼
      Doctor Pocket Model
              │
       ┌──────┴──────┐
       ▼             ▼
 Qwen Base       LoRA Adapter
       │             │
       └──────┬──────┘
              ▼
       Text Generation
              │
              ▼
        JSON Response
              │
              ▼
       React Frontend
              │
              ▼
        User sees answer
```
 
---
 
## 🧠 Model Loading Lifecycle
 
The model is loaded once when the FastAPI application starts.
 
The backend does not reload the model every time a user asks a question.
 
The loading process is:
 
```text
FastAPI starts
      │
      ▼
Load tokenizer
      │
      ▼
Load Qwen base model
      │
      ▼
Configure 4-bit NF4 quantization
      │
      ▼
Load Doctor Pocket LoRA adapter
      │
      ▼
Set model to evaluation mode
      │
      ▼
Cache model
      │
      ▼
API ready
```
 
This is important because loading a large language model for every request would cause significant latency.
 
---
 
## 🧩 LoRA Adapter
 
Doctor Pocket uses a LoRA adapter instead of storing a completely separate full fine-tuned model.
 
The adapter is stored locally at:
 
```text
model/doctor_pocket_qwen25_1_5b_lora/
```
 
The backend loads the adapter using PEFT:
 
```python
PeftModel.from_pretrained(...)
```
 
The adapter is applied on top of:
 
```text
Qwen/Qwen2.5-1.5B-Instruct
```
 
This allows the relatively small LoRA adapter to contain the task-specific fine-tuning while the original Qwen model remains the base model.
 
---
 
## 📦 Model Directory
 
The overall project contains:
 
```text
Doctor Pocket/
│
├── backend/
│
├── frontend/
│
├── model/
│   ├── README.md
│   └── doctor_pocket_qwen25_1_5b_lora/
│
└── notebooks/
```
 
The actual model weights are intentionally excluded from the GitHub repository because they are large.
 
The model documentation remains available through:
 
```text
model/README.md
```
 
---
 
## 🚫 Why the Model Weights Are Not on GitHub
 
The trained LoRA adapter contains large model files that are not appropriate for a normal source-code repository.
 
Therefore, the project's `.gitignore` excludes:
 
```text
model/doctor_pocket_qwen25_1_5b_lora/
```
 
The resulting structure is:
 
```text
model/
├── README.md
└── doctor_pocket_qwen25_1_5b_lora/
    └── [ignored model files]
```
 
This keeps the GitHub repository lightweight while still documenting the model.
 
---
 
## 🔐 Environment Variables
 
Local environment configuration is stored in:
 
```text
backend/.env
```
 
The `.env` file is intentionally excluded from GitHub.
 
Sensitive information should never be hard-coded into the source code.
 
Never commit:
 
- API keys
- Authentication tokens
- Hugging Face tokens
- Passwords
- Private credentials
---
 
## 🩺 Doctor Pocket System Prompt
 
The backend uses a system prompt to guide the model toward cautious and educational responses.
 
The system prompt is:
 
```text
You are Doctor Pocket, an AI medical information assistant.
Provide clear, cautious, educational medical information.
Do not claim to replace a doctor.
For emergencies or serious symptoms, advise the user to seek professional medical care.
Do not invent medical facts.
```
 
The system prompt is included together with the user's question before generation.
 
---
 
## 💬 Chat Formatting
 
Doctor Pocket uses the official Qwen tokenizer chat template instead of manually creating an incompatible prompt format.
 
The conversation is structured conceptually as:
 
```text
System:
You are Doctor Pocket, an AI medical information assistant.
 
User:
What are the symptoms of dehydration?
 
Assistant:
[Generated response]
```
 
The tokenizer's official chat template converts this conversation into the format expected by the Qwen instruction model.
 
---
 
## ⚙️ Text Generation
 
The backend uses configurable generation parameters including:
 
- `max_new_tokens`
- `temperature`
- `top_p`
- `repetition_penalty`
These parameters control the length, randomness, and repetition behavior of generated answers.
 
The current inference configuration uses sampling to produce natural responses while attempting to reduce repetitive generation.
 
---
 
## 🧪 Model Testing
 
Doctor Pocket was manually evaluated using ten medical questions covering several different topics.
 
| # | Question Topic | Result |
|---|-----------------|--------|
| 1 | Dehydration | Good |
| 2 | High blood pressure | Good |
| 3 | Type 2 diabetes | Good |
| 4 | Cold vs. flu | Good |
| 5 | Vitamin D deficiency | Good |
| 6 | Headaches | Good |
| 7 | Pneumonia | Good |
| 8 | Minor burn | Bad — repeated the same information multiple times |
| 9 | Asthma | Good |
| 10 | Emergency chest pain | Good — acceptable, but not optimal |
 
The evaluation showed that Doctor Pocket can produce useful responses for a variety of general medical-information questions.
 
The minor-burn example demonstrated a weakness in repetitive generation.
 
The emergency chest-pain response was considered acceptable, although there is room for improvement in emergency-response behavior.
 
This was a qualitative manual evaluation and should not be considered clinical validation.
 
---
 
## ⚠️ Medical Safety Disclaimer
 
Doctor Pocket is an:
 
**Educational / Research Prototype**
 
It is not a replacement for a qualified physician or other healthcare professional.
 
The model should not be used for:
 
- Medical diagnosis
- Emergency decision-making
- Individualized treatment decisions
- Prescription decisions
- Clinical decision-making
AI-generated information may contain:
 
- Incorrect information
- Missing information
- Repetition
- Outdated information
- Inappropriate recommendations
For serious or emergency symptoms, users should seek professional medical care.
 
---
 
## 🧪 Testing the API Without the Frontend
 
The backend can be tested directly through Swagger.
 
Start the server:
 
```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```
 
Then open:
 
```text
http://127.0.0.1:8000/docs
```
 
Find:
 
```http
POST /api/generate
```
 
Select **Try it out**.
 
Enter:
 
```json
{
  "question": "What are common symptoms of iron deficiency anemia?"
}
```
 
Then select **Execute**.
 
The API should return the generated Doctor Pocket answer.
 
---
 
## 🌐 Frontend Integration
 
The React frontend runs separately from the FastAPI backend.
 
The local development architecture is:
 
```text
React + Vite
localhost:5173
        │
        │ HTTP
        ▼
FastAPI
localhost:8000
        │
        ▼
Doctor Pocket Model
```
 
Start the frontend from another terminal:
 
```powershell
cd frontend
npm.cmd run dev
```
 
Vite will normally provide:
 
```text
http://localhost:5173/
```
 
For the complete application to work locally, both the frontend and backend servers must be running.
 
---
 
## 🛠️ Main Backend Technologies
 
| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| PyTorch | Deep learning framework |
| Transformers | Language model loading and inference |
| PEFT | LoRA adapter loading |
| BitsAndBytes | 4-bit quantization |
| Qwen2.5-1.5B-Instruct | Base language model |
 
---
 
## 📂 Backend Responsibilities
 
The backend connects the trained language model to the web application.
 
Its main responsibilities are:
 
```text
1. Start the API server
        ↓
2. Detect available hardware
        ↓
3. Load tokenizer
        ↓
4. Load quantized Qwen model
        ↓
5. Load Doctor Pocket LoRA adapter
        ↓
6. Receive medical questions
        ↓
7. Apply Doctor Pocket system prompt
        ↓
8. Apply Qwen chat template
        ↓
9. Generate response
        ↓
10. Return JSON response
```
 
---
 
## 🔗 Complete Doctor Pocket Architecture
 
The complete Doctor Pocket project consists of three major layers:
 
```text
                 DOCTOR POCKET
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
   Frontend        Backend         Model
       │              │              │
     React          FastAPI      Qwen2.5-1.5B
       │              │              │
       │              │         LoRA Adapter
       │              │              │
       └──── HTTP ────┴──────────────┘
                      │
                      ▼
                AI Response
```
 
---
 
## 🚧 Current Development Status
 
The Doctor Pocket backend is currently functional as a local development API.
 
Implemented components include:
 
- FastAPI backend.
- Qwen2.5-1.5B-Instruct integration.
- Doctor Pocket LoRA adapter integration.
- 4-bit NF4 inference.
- CUDA GPU support.
- Model caching.
- Health-check endpoint.
- Text-generation endpoint.
- Chat endpoint.
- JSON request/response handling.
- Swagger API documentation.
- React frontend integration.
---
 
## 🔮 Future Improvements
 
Potential future improvements include:
 
- Streaming responses.
- Conversation history.
- User authentication.
- Database integration.
- Request rate limiting.
- Better error handling.
- Medical safety filtering.
- Retrieval-Augmented Generation (RAG).
- Medical knowledge grounding.
- Response caching.
- Automated model evaluation.
- Production deployment.
- HTTPS.
- Monitoring and logging.
- More advanced emergency-response safeguards.
---
 
## 📌 Project Pipeline
 
The complete Doctor Pocket pipeline is:
 
```text
Medical Q&A Dataset
        ↓
Data Preprocessing
        ↓
80/10/10 Data Split
        ↓
Qwen2.5-1.5B-Instruct
        ↓
QLoRA Fine-Tuning
        ↓
Doctor Pocket LoRA Adapter
        ↓
4-bit Quantized Inference
        ↓
FastAPI Backend
        ↓
React Frontend
        ↓
Medical Q&A Application
```
 
The backend is the bridge between the fine-tuned language model and the user-facing React application.
 
---
 
## 🔗 Related Documentation
 
For the complete project documentation:
 
```text
../README.md
```
 
For model and training information:
 
```text
../model/README.md
```
 
For the React frontend:
 
```text
../frontend/README.md
```
 
For the training notebook:
 
```text
../notebooks/
```
 
---
 
## 👨‍💻 Doctor Pocket
 
**Doctor Pocket — Medical AI Assistant**
 
An educational/research project demonstrating the integration of:
 
- Large Language Models
- QLoRA Fine-Tuning
- PEFT / LoRA
- 4-bit Quantization
- PyTorch
- FastAPI
- React
The project demonstrates the complete process of taking a fine-tuned language model and integrating it into a functional AI-powered web application.
 
---
 
## ⚠️ Disclaimer
 
Doctor Pocket is an educational and research project.
 
It does not provide professional medical advice, diagnosis, or treatment.
 
Always consult a qualified healthcare professional for medical concerns, and seek emergency medical care when necessary.