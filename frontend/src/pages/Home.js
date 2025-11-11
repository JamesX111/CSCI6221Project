import React, { useState } from "react";

const Home = () => {
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [error, setError] = useState("");

  const handleSend = async () => {
    if (!userMessage.trim()) return;

    // Add user message to chat history
    const updatedHistory = [...chatHistory, { role: "user", content: userMessage }];
    setChatHistory(updatedHistory);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/gpt/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: userMessage,
          chat_history: chatHistory,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Add assistant reply to chat
        setChatHistory([...updatedHistory, { role: "assistant", content: data.reply }]);
        setUserMessage(""); // clear input
        setError("");
      } else {
        setError(data.error || "Error communicating with GPT.");
      }
    } catch (err) {
      setError("Failed to connect to server.");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto", padding: "1rem" }}>
      <h2 style={{ marginBottom: "1rem", color: "#082c6c" }}>Chat with GPT</h2>

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "8px",
          padding: "1rem",
          height: "400px",
          overflowY: "auto",
          marginBottom: "1rem",
          backgroundColor: "#f9f9f9",
        }}
      >
        {chatHistory.length === 0 && (
          <p className="text-muted">Start the conversation below...</p>
        )}
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              marginBottom: "0.75rem",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "0.5rem 1rem",
                borderRadius: "12px",
                backgroundColor: msg.role === "user" ? "#0b3d91" : "#e0e0e0",
                color: msg.role === "user" ? "white" : "black",
                maxWidth: "70%",
                wordWrap: "break-word",
              }}
            >
              {msg.content}
            </span>
          </div>
        ))}
      </div>

      {error && <p style={{ color: "red", marginBottom: "0.5rem" }}>{error}</p>}

      <div style={{ display: "flex", gap: "0.5rem" }}>
        <textarea
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          style={{
            flexGrow: 1,
            padding: "0.5rem",
            borderRadius: "8px",
            border: "1px solid #ccc",
            resize: "none",
            height: "60px",
          }}
        />
        <button
          onClick={handleSend}
          style={{
            backgroundColor: "#0b3d91",
            color: "white",
            border: "none",
            padding: "0 1.5rem",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = "black";
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = "#0b3d91";
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Home;
