# Doctor Pocket — Frontend
 
The Doctor Pocket frontend is a responsive React-based web interface for interacting with the Doctor Pocket medical question-answering AI assistant.
 
The frontend provides a clean conversational interface where users can:
 
- Ask medical-information questions.
- Select suggested questions.
- View AI-generated responses.
- Start a new consultation.
- Access the FastAPI backend through HTTP requests.
- Use the application on desktop and mobile devices.
- View loading states while the AI generates a response.
- Receive user-friendly error messages if the backend is unavailable.
---
 
## 🧠 Frontend Architecture
 
The Doctor Pocket frontend is built using React and communicates with the FastAPI backend through HTTP requests.
 
```text
                         Doctor Pocket
                              │
                              ▼
                      React Frontend
                      localhost:5173
                              │
                              │ HTTP POST
                              ▼
                       FastAPI Backend
                       localhost:8000
                              │
                              ▼
                    Doctor Pocket Model
                              │
                              ▼
                         AI Response
                              │
                              ▼
                      React Frontend
                              │
                              ▼
                         User Interface
```
 
---
 
## ⚛️ Frontend Technologies
 
The frontend uses:
 
| Technology | Purpose |
|------------|---------|
| React | User interface framework |
| Vite | Frontend development/build tool |
| JavaScript | Application logic |
| CSS | Interface styling and responsive design |
| Lucide React | UI icons |
| Fetch API | Communication with FastAPI |
 
---
 
## 📁 Frontend Structure
 
The frontend is organized approximately as follows:
 
```text
frontend/
│
├── public/
│
├── src/
│   ├── App.jsx
│   ├── App.css
│   └── ...
│
├── package.json
├── package-lock.json
├── vite.config.js
└── README.md
```
 
The following directories are intentionally excluded from GitHub:
 
```text
node_modules/
dist/
.vite/
```
 
These files can be recreated by installing the project's npm dependencies.
 
---
 
## 🎨 User Interface
 
The Doctor Pocket interface was designed around a clean medical-AI aesthetic.
 
The main interface contains:
 
```text
┌──────────────────────────────────────────────────────────┐
│ Doctor Pocket                              AI Assistant  │
├────────────────┬─────────────────────────────────────────┤
│                │                                         │
│ Doctor Pocket  │              Welcome Screen             │
│                │                                         │
│ + New          │        How can I help you today?        │
│ Consultation   │                                         │
│                │       Suggested Medical Questions       │
│ QUICK ACCESS   │                                         │
│                │                                         │
│ Current        │                                         │
│ consultation   │                                         │
│                │                                         │
│                │                                         │
│ Private &      │                                         │
│ Educational    │                                         │
│                │                                         │
├────────────────┴─────────────────────────────────────────┤
│          Ask Doctor Pocket a medical question...     ➤   │
│                                                          │
│   Doctor Pocket provides educational information...      │
└──────────────────────────────────────────────────────────┘
```
 
---
 
## 🏠 Welcome Screen
 
When the application starts and there are no messages, the user is presented with a welcome screen.
 
The welcome screen includes:
 
- Doctor Pocket branding.
- Medical AI assistant description.
- Introductory message.
- Suggested medical questions.
- Question input field.
- Medical disclaimer.
Example suggested questions include:
 
- What are common symptoms of iron deficiency anemia?
- What causes frequent headaches?
- What are the symptoms of dehydration?
- How can I improve my sleep?
Clicking one of the suggested questions automatically sends it to the backend.
 
---
 
## 💬 Chat Interface
 
After a question is submitted, the interface switches from the welcome screen to the conversation view.
 
The conversation displays:
 
```text
USER
What are the symptoms of dehydration?
 
DOCTOR POCKET
[Generated medical-information response]
```
 
User messages and AI messages have different visual styles to make the conversation easy to follow.
 
---
 
## 👤 User Messages
 
User messages are displayed on the right side of the conversation.
 
They contain:
 
- User avatar.
- "You" label.
- User question.
- Teal-colored message bubble.
Example:
 
```text
                                  ┌─────────────────────────┐
                                  │ What are the symptoms   │
                                  │ of dehydration?         │
                                  └─────────────────────────┘
                                                        👤
```
 
---
 
## 🤖 Doctor Pocket Messages
 
AI responses are displayed on the left side.
 
They contain:
 
- Doctor Pocket bot avatar.
- "Doctor Pocket" label.
- AI-generated response.
- White response bubble.
Example:
 
```text
🤖
Doctor Pocket
 
┌───────────────────────────────────────────────────┐
│ Dehydration can cause several symptoms including  │
│ thirst, dry mouth, fatigue, dizziness, and dark   │
│ urine...                                          │
└───────────────────────────────────────────────────┘
```
 
---
 
## ⏳ Loading State
 
While the backend is generating a response, the frontend displays an animated loading indicator.
 
This prevents the user from thinking that the application has stopped responding.
 
The loading state consists of three animated dots:
 
```text
● ● ●
```
 
The send button is also disabled while a request is being processed.
 
---
 
## ✉️ Message Input
 
The message composer is located at the bottom of the application.
 
Users can:
 
- Type a medical question.
- Press the Send button.
- Press Enter to send.
- Press Shift + Enter to create a new line.
The input is automatically disabled while a response is being generated.
 
---
 
## 🔄 API Communication
 
The frontend communicates with the FastAPI backend using the browser's Fetch API.
 
The main request is sent to:
 
```http
POST http://127.0.0.1:8000/api/chat
```
 
The request body is:
 
```json
{
  "question": "What are the symptoms of dehydration?"
}
```
 
The backend returns a response containing the generated answer:
 
```json
{
  "answer": "Dehydration can cause several symptoms..."
}
```
 
The frontend then adds the response to the conversation.
 
---
 
## 🔁 Request Flow
 
When a user sends a question, the following process occurs:
 
```text
User types question
        │
        ▼
React state updated
        │
        ▼
User submits question
        │
        ▼
Frontend displays user message
        │
        ▼
Loading indicator appears
        │
        ▼
POST /api/chat
        │
        ▼
FastAPI Backend
        │
        ▼
Doctor Pocket Model
        │
        ▼
Generated answer
        │
        ▼
JSON response
        │
        ▼
React receives response
        │
        ▼
Assistant message displayed
```
 
---
 
## 🧩 React State Management
 
The application uses React's `useState` hook to manage the interface.
 
Important state variables include:
 
```javascript
const [question, setQuestion] = useState("");
const [messages, setMessages] = useState([]);
const [sidebarOpen, setSidebarOpen] = useState(false);
const [loading, setLoading] = useState(false);
```
 
### Question State
 
Stores the current text entered into the message composer.
 
```javascript
question
```
 
### Messages State
 
Stores the current conversation.
 
Each message follows a structure similar to:
 
```json
{
  "id": 1,
  "role": "user",
  "content": "What are the symptoms of dehydration?"
}
```
 
An assistant message follows:
 
```json
{
  "id": 2,
  "role": "assistant",
  "content": "Dehydration can cause..."
}
```
 
### Sidebar State
 
Controls whether the mobile sidebar is open.
 
```javascript
sidebarOpen
```
 
### Loading State
 
Tracks whether the frontend is waiting for a backend response.
 
```javascript
loading
```
 
---
 
## 🆕 New Consultation
 
The sidebar contains a:
 
```text
+ New consultation
```
 
button.
 
Selecting this button clears the current conversation.
 
The application resets:
 
```javascript
setMessages([]);
setQuestion("");
```
 
This allows the user to start a new consultation without refreshing the browser.
 
---
 
## 📱 Responsive Design
 
Doctor Pocket was designed to work across:
 
- Desktop computers.
- Laptops.
- Tablets.
- Mobile devices.
The CSS includes responsive breakpoints at:
 
- 800px
- 480px
---
 
## 📱 Mobile Interface
 
On smaller screens, the desktop sidebar is replaced by a mobile menu button.
 
The sidebar can be opened using the menu icon.
 
A semi-transparent overlay appears behind the sidebar.
 
The sidebar can then be closed using the close button or by selecting the overlay.
 
The interface automatically adjusts:
 
- Sidebar behavior.
- Header layout.
- Message spacing.
- Suggestion cards.
- Font sizes.
- Input width.
- Avatar sizes.
---
 
## 🎨 Design System
 
The interface uses a light medical-themed visual design.
 
The primary accent color is a teal/green tone:
 
```text
#159b8c
```
 
This color is used for:
 
- Doctor Pocket branding.
- Buttons.
- AI icons.
- Status indicators.
- Links and active states.
- User interaction highlights.
The overall interface uses:
 
- White
- Light gray
- Soft teal
- Dark gray
- Muted gray
to create a clean and professional appearance.
 
---
 
## 🩺 Doctor Pocket Branding
 
The interface uses medical-related visual elements such as:
 
- Stethoscope
- Activity
- Bot
- Shield
- Message
- User
These icons are provided through:
 
**Lucide React**
 
The branding emphasizes that Doctor Pocket is a medical-information assistant rather than a general-purpose chatbot.
 
---
 
## 🔐 Privacy & Educational Notice
 
The sidebar contains a privacy and educational-information notice:
 
```text
Private & Educational
 
Your conversations are for informational purposes.
```
 
The message composer also contains a medical disclaimer:
 
```text
Doctor Pocket provides educational information and does not replace
professional medical advice.
```
 
These notices reinforce the educational/research nature of the project.
 
---
 
## ⚠️ Error Handling
 
If the frontend cannot connect to the backend, it displays a user-friendly error message:
 
```text
I couldn't connect to the Doctor Pocket backend.
Please make sure the FastAPI server is running.
```
 
The actual error is also logged to the browser console for debugging.
 
Example:
 
```javascript
console.error("Doctor Pocket API error:", error);
```
 
---
 
## 🚀 Running the Frontend
 
### 1. Open a New Terminal
 
The FastAPI backend should remain running in its own terminal.
 
Open another PowerShell terminal.
 
Navigate to the project:
 
```powershell
cd "D:\AI\Doctor Pocket"
```
 
### 2. Enter the Frontend Directory
 
Run:
 
```powershell
cd frontend
```
 
### 3. Install Dependencies
 
If `node_modules` does not exist, install the dependencies:
 
```powershell
npm install
```
 
This installs the packages specified in:
 
```text
package.json
```
 
### 4. Start the Development Server
 
Run:
 
```powershell
npm.cmd run dev
```
 
Vite will start the development server.
 
The terminal should provide a local URL similar to:
 
```text
http://localhost:5173/
```
 
Open that URL in a browser.
 
---
 
## 🔌 Running Frontend + Backend Together
 
The complete local application requires two development servers.
 
### Terminal 1 — FastAPI
 
From the project root:
 
```powershell
cd "D:\AI\Doctor Pocket"
```
 
Activate the backend environment:
 
```powershell
cd backend
.\venv\Scripts\Activate.ps1
cd ..
```
 
Start FastAPI:
 
```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```
 
Backend:
 
```text
http://127.0.0.1:8000
```
 
### Terminal 2 — React
 
Open another terminal:
 
```powershell
cd "D:\AI\Doctor Pocket\frontend"
```
 
Start Vite:
 
```powershell
npm.cmd run dev
```
 
Frontend:
 
```text
http://localhost:5173/
```
 
---
 
## 🌐 Complete Local Development Architecture
 
When both servers are running:
 
```text
┌───────────────────────────────────────────────┐
│                 Web Browser                    │
│                                                 │
│          React / Vite Frontend                 │
│          http://localhost:5173                 │
└──────────────────────┬──────────────────────────┘
                        │
                        │ HTTP POST
                        │ /api/chat
                        ▼
┌───────────────────────────────────────────────┐
│              FastAPI Backend                   │
│          http://127.0.0.1:8000                 │
└──────────────────────┬──────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│             Doctor Pocket Model                │
│                                                 │
│       Qwen2.5-1.5B-Instruct + LoRA             │
└───────────────────────────────────────────────┘
```
 
---
 
## 🧪 Frontend Testing
 
The frontend was tested by sending medical questions through the web interface.
 
Example test categories included:
 
1. Dehydration
2. High blood pressure
3. Type 2 diabetes
4. Cold vs. flu
5. Vitamin D deficiency
6. Headaches
7. Pneumonia
8. Minor burns
9. Asthma
10. Emergency chest pain
The frontend successfully communicates with the backend and displays the generated Doctor Pocket responses.
 
The quality of the generated answers depends on the underlying fine-tuned model and should not be interpreted as clinical validation.
 
---
 
## 📸 Application Screenshots
 
Screenshots of the Doctor Pocket interface are included in the main project documentation.
 
The screenshots demonstrate:
 
- Main Doctor Pocket interface.
- Medical question-and-answer conversation.
- FastAPI Swagger API documentation.
See the main project README:
 
```text
../README.md
```
 
---
 
## 🎥 Demonstration Videos
 
Demonstration videos can be added to the main project README when available.
 
The frontend can be demonstrated through:
 
1. Opening the Doctor Pocket interface.
2. Entering a medical question.
3. Sending the question.
4. Displaying the loading animation.
5. Receiving the AI-generated answer.
6. Starting a new consultation.
---
 
## 🛠️ Frontend Development
 
The main application component is:
 
```text
src/App.jsx
```
 
The main styling file is:
 
```text
src/App.css
```
 
The application component controls:
 
- Application state.
- Chat messages.
- API requests.
- Loading state.
- Sidebar state.
- New consultation behavior.
- Suggested questions.
- Message rendering.
The CSS controls:
 
- Layout.
- Colors.
- Typography.
- Sidebar.
- Chat bubbles.
- Buttons.
- Loading animation.
- Responsive behavior.
- Mobile navigation.
---
 
## 📦 Production Build
 
For a production build, run:
 
```powershell
npm.cmd run build
```
 
Vite will generate a production build in:
 
```text
frontend/dist/
```
 
The `dist/` directory is ignored by Git because it can be generated again from the source code.
 
---
 
## 👀 Previewing the Production Build
 
After building the application, the production build can be previewed using:
 
```powershell
npm.cmd run preview
```
 
Vite will provide a local preview URL.
 
---
 
## 🔧 Configuration
 
The current frontend communicates with the local FastAPI backend using:
 
```javascript
fetch("http://127.0.0.1:8000/api/chat", ...)
```
 
For deployment, this should be changed to the URL of the deployed FastAPI backend.
 
For example:
 
```text
https://your-backend-domain.com/api/chat
```
 
A future production version should preferably use an environment variable rather than hard-coding the API URL.
 
For example:
 
```text
VITE_API_URL
```
 
---
 
## 🚧 Current Development Status
 
The Doctor Pocket frontend currently provides:
 
- React-based user interface.
- Responsive desktop layout.
- Responsive mobile layout.
- Sidebar navigation.
- New consultation functionality.
- Suggested medical questions.
- Chat interface.
- User messages.
- Doctor Pocket responses.
- Loading animation.
- Error handling.
- FastAPI integration.
- Medical disclaimer.
- Educational/privacy notice.
---
 
## 🔮 Future Improvements
 
Potential frontend improvements include:
 
- Persistent conversation history.
- Multiple saved consultations.
- User authentication.
- Dark mode.
- Markdown rendering for AI responses.
- Syntax highlighting for medical information where appropriate.
- Better formatting of lists and headings.
- Streaming AI responses.
- Copy-response button.
- Regenerate-response button.
- Feedback buttons.
- Conversation search.
- Patient/user profiles.
- Accessibility improvements.
- Improved mobile interaction.
- Production API configuration.
- Deployment to a cloud hosting platform.
---
 
## 🧩 Complete Doctor Pocket Architecture
 
The frontend is one layer of the complete Doctor Pocket system:
 
```text
                  Doctor Pocket
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
     Dataset        Backend        Frontend
        │              │              │
        ▼              ▼              ▼
    Training        FastAPI         React
        │              │              │
        ▼              ▼              │
  LoRA Adapter   AI Inference         │
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
                Medical Q&A
                Web Application
```
 
---
 
## 📌 Project Pipeline
 
The complete Doctor Pocket pipeline is:
 
```text
Medical Q&A Dataset
        ↓
Data Preprocessing
        ↓
80/10/10 Random Split
        ↓
Qwen2.5-1.5B-Instruct
        ↓
QLoRA Fine-Tuning
        ↓
Doctor Pocket LoRA Adapter
        ↓
FastAPI Backend
        ↓
React Frontend
        ↓
Medical Q&A Application
```
 
---
 
## 🔗 Related Documentation
 
For complete project documentation:
 
```text
../README.md
```
 
For the backend:
 
```text
../backend/README.md
```
 
For the trained model:
 
```text
../model/README.md
```
 
For the training notebook:
 
```text
../notebooks/
```
 
---
 
## 👨‍💻 Doctor Pocket
 
**Doctor Pocket — Medical AI Assistant**
 
A medical question-answering AI project integrating:
 
- React
- FastAPI
- PyTorch
- Transformers
- PEFT / LoRA
- QLoRA
- Qwen2.5-1.5B-Instruct
The frontend provides the user-facing interface that connects users to the Doctor Pocket AI model through the FastAPI backend.
 
---
 
## ⚠️ Disclaimer
 
Doctor Pocket is an educational and research project.
 
It does not provide professional medical advice, diagnosis, or treatment.
 
AI-generated responses may contain inaccurate, incomplete, or outdated information.
 
Users should consult qualified healthcare professionals for medical concerns and seek emergency medical care when necessary.