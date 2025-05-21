import React, { useState, useEffect } from "react";
import { useWebSocket } from "../hooks/useWebSocket";

interface Message {
  text: string;
  sender: "user" | "system";
  type?: "processing" | "completed" | "error";
  data?: any;
}

interface TaskResponse {
  task_id: string;
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  
  const { isConnected, lastMessage, connect, disconnect } = useWebSocket();

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      // Only add messages that are completed or error
      if (lastMessage.status === "completed" || lastMessage.status === "error") {
        addMessage({
          text: formatMessage(lastMessage),
          sender: "system",
          type: lastMessage.status,
          data: lastMessage
        });
      }
    }
  }, [lastMessage]);

  const formatMessage = (message: any): string => {
    if (message.status === "completed") {
      return `${message.blackboard?.history?.steps?.map((step: any) => step.description).join(", ") || "No steps"}`;
    }
    if (message.status === "error") {
      return `Error: ${message.error || "Unknown error"}`;
    }
    return JSON.stringify(message, null, 2);
  };

  const addMessage = (message: Message) => {
    setMessages((prev: Message[]) => [...prev, message]);
  };

  const handleSend = async () => {
    if (input.trim() === "") return;

    const userMessage: Message = {
      text: input,
      sender: "user",
    };

    setMessages((prev: Message[]) => [...prev, userMessage]);
    setInput("");

    try {
      const response = await fetch("http://localhost:5172/api/v2/async/agent/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input, owner: "user" }),
      });

      const data: TaskResponse = await response.json();

      if (response.ok) {
        setCurrentTaskId(data.task_id);
        connect(data.task_id);
      } else {
        addMessage({
          text: `Failed to start task: ${data}`,
          sender: "system",
          type: "error"
        });
      }
    } catch (error) {
      addMessage({
        text: `Error: ${error}`,
        sender: "system",
        type: "error"
      });
    }
  };

  // Cleanup WebSocket connection when component unmounts
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return (
    <div className="dashboard-box chatbox-widget">
      <style>
        {`
          .chat-message {
            margin: 8px 0;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
          }
          .user-msg {
            background-color: #e3f2fd;
            margin-left: auto;
          }
          .system-msg {
            background-color: #f5f5f5;
            margin-right: auto;
          }
          .error {
            background-color: #ffebee !important;
            color: #c62828;
            border: 1px solid #ef9a9a;
          }
          .completed {
            background-color: #e8f5e9 !important;
            color: #2e7d32;
            border: 1px solid #a5d6a7;
          }
          .chatbox-messages {
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 10px;
          }
          .chatbox-input {
            display: flex;
            gap: 10px;
          }
          .chatbox-input input {
            flex: 1;
            padding: 8px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
          }
          .chatbox-input button {
            padding: 8px 16px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          }
          .chatbox-input button:hover {
            background-color: #1976d2;
          }
        `}
      </style>
      <h2>Chat Box</h2>
      <div className="chatbox-messages">
        {messages.map((msg: Message, idx: number) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user-msg" : "system-msg"} ${msg.type || ""}`}
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
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
          onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
