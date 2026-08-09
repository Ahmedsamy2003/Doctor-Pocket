import { useState } from "react";
import {
  Activity,
  Bot,
  ChevronDown,
  Menu,
  MessageCircle,
  Plus,
  Send,
  ShieldCheck,
  Stethoscope,
  User,
  X,
} from "lucide-react";
import "./App.css";

const suggestedQuestions = [
  "What are common symptoms of iron deficiency anemia?",
  "What causes frequent headaches?",
  "What are the symptoms of dehydration?",
  "How can I improve my sleep?",
];

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text = question) => {
    const trimmedQuestion = text.trim();

    if (!trimmedQuestion || loading) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [...previous, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.answer,
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: `Backend error: ${error.message}`,
        error: true,
      };

      setMessages((previous) => [...previous, errorMessage]);

      console.error("Doctor Pocket API error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  const startNewChat = () => {
    setMessages([]);
    setQuestion("");
  };

  return (
    <div className="app-shell">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-header">
          <div className="brand">
            <div className="brand-icon">
              <Stethoscope size={22} strokeWidth={2.2} />
            </div>

            <div>
              <h1>Doctor Pocket</h1>
              <span>Medical AI Assistant</span>
            </div>
          </div>

          <button
            className="mobile-close"
            onClick={() => setSidebarOpen(false)}
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        </div>

        <button className="new-chat-button" onClick={startNewChat}>
          <Plus size={19} />
          <span>New consultation</span>
        </button>

        <div className="sidebar-section">
          <div className="section-label">QUICK ACCESS</div>

          <button className="sidebar-item active">
            <MessageCircle size={18} />
            <span>Current consultation</span>
          </button>
        </div>

        <div className="sidebar-spacer" />

        <div className="sidebar-footer">
          <div className="privacy-card">
            <ShieldCheck size={18} />
            <div>
              <strong>Private & Educational</strong>
              <p>Your conversations are for informational purposes.</p>
            </div>
          </div>

          <div className="version">
            Doctor Pocket <span>v1.0</span>
          </div>
        </div>
      </aside>

      {/* Main application */}
      <main className="main-content">
        {/* Top bar */}
        <header className="topbar">
          <button
            className="menu-button"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={22} />
          </button>

          <div className="mobile-brand">
            <div className="brand-icon small">
              <Stethoscope size={18} />
            </div>
            <span>Doctor Pocket</span>
          </div>

          <div className="topbar-status">
            <span className="status-dot" />
            AI Assistant
            <ChevronDown size={15} />
          </div>
        </header>

        {/* Chat area */}
        <section className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-icon">
                <Activity size={30} strokeWidth={1.8} />
              </div>

              <span className="eyebrow">YOUR PERSONAL AI HEALTH COMPANION</span>

              <h2>
                How can I help you
                <span> today?</span>
              </h2>

              <p className="welcome-description">
                Ask Doctor Pocket about symptoms, health conditions,
                medications, nutrition, or general medical information.
              </p>

              <div className="suggestions">
                {suggestedQuestions.map((item) => (
                  <button
                    key={item}
                    className="suggestion-card"
                    onClick={() => sendMessage(item)}
                  >
                    <MessageCircle size={17} />
                    <span>{item}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message-row ${
                    message.role === "user" ? "user-row" : "assistant-row"
                  }`}
                >
                  <div
                    className={`avatar ${
                      message.role === "user"
                        ? "user-avatar"
                        : "assistant-avatar"
                    }`}
                  >
                    {message.role === "user" ? (
                      <User size={17} />
                    ) : (
                      <Bot size={18} />
                    )}
                  </div>

                  <div className="message-content">
                    <span className="message-author">
                      {message.role === "user" ? "You" : "Doctor Pocket"}
                    </span>

                    <div
                      className={`message-bubble ${
                        message.error ? "error-message" : ""
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant-row">
                  <div className="avatar assistant-avatar">
                    <Bot size={18} />
                  </div>

                  <div className="message-content">
                    <span className="message-author">Doctor Pocket</span>

                    <div className="message-bubble loading-bubble">
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        {/* Input */}
        <div className="composer-wrapper">
          <form className="composer" onSubmit={handleSubmit}>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  handleSubmit(event);
                }
              }}
              placeholder="Ask Doctor Pocket a medical question..."
              rows={1}
              disabled={loading}
            />

            <button
              type="submit"
              className="send-button"
              disabled={!question.trim() || loading}
              aria-label="Send message"
            >
              <Send size={18} />
            </button>
          </form>

          <p className="disclaimer">
            <ShieldCheck size={14} />
            Doctor Pocket provides educational information and does not replace
            professional medical advice.
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;