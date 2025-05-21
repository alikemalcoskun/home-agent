import React, { useState } from "react";

interface Message {
  text: string;
  sender: "user" | "system";
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage: Message = {
      text: input,
      sender: "user",
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");
  };

  return (
    <div className="dashboard-box chatbox-widget">
      <h2>Chat Box</h2>
      <div className="chatbox-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user-msg" : "system-msg"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chatbox-input">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
