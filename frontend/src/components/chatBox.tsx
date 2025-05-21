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

interface Step {
  agent: string;
  description: string;
  status: string;
}

type TabType = "chat" | "steps";

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [steps, setSteps] = useState<Step[]>([]);
  const [activeTab, setActiveTab] = useState<TabType>("chat");
  
  const { isConnected, lastMessage, connect, disconnect } = useWebSocket();

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      // Update steps from blackboard history
      if (lastMessage.blackboard?.history?.steps) {
        setSteps(lastMessage.blackboard.history.steps);
      }

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
          @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
          
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
            height: calc(100% - 60px);
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 10px;
          }
          .steps-container {
            height: calc(100% - 60px);
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 10px;
          }
          .chatbox-input {
            display: flex;
            gap: 10px;
            padding: 10px 0;
            position: sticky;
            bottom: 0;
            background-color: white;
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
          .tabs {
            display: flex;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 15px;
          }
          .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            color: #757575;
          }
          .tab.active {
            color: #2196f3;
            border-bottom-color: #2196f3;
          }
          .tab-content {
            display: none;
            height: 500px;
            position: relative;
          }
          .tab-content.active {
            display: flex;
            flex-direction: column;
          }
          .steps-list {
            list-style: none;
            padding: 0;
            margin: 0;
          }
          .step-item {
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            background-color: white;
            border: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
            gap: 12px;
          }
          .step-agent {
            font-weight: bold;
            color: #2196f3;
            text-transform: uppercase;
            min-width: 120px;
            display: flex;
            align-items: center;
            gap: 8px;
          }
          .step-description {
            flex: 1;
            color: #424242;
          }
          .step-status {
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.8em;
            white-space: nowrap;
          }
          .agent-icon {
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background-color: #e3f2fd;
            color: #2196f3;
            font-weight: bold;
          }
          .agent-icon .material-icons {
            font-size: 16px;
          }
          .planner-icon {
            background-color: #e8f5e9;
            color: #2e7d32;
          }
          .orchestration-icon {
            background-color: #fff3e0;
            color: #ef6c00;
          }
          .edge-icon {
            background-color: #e3f2fd;
            color: #2196f3;
          }
          .status-completed {
            background-color: #e8f5e9;
            color: #2e7d32;
          }
          .status-pending {
            background-color: #fff3e0;
            color: #ef6c00;
          }
          .status-error {
            background-color: #ffebee;
            color: #c62828;
          }
        `}
      </style>
      <h2>Chat Box</h2>
      <div className="tabs">
        <div 
          className={`tab ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          Chat
        </div>
        <div 
          className={`tab ${activeTab === "steps" ? "active" : ""}`}
          onClick={() => setActiveTab("steps")}
        >
          Steps
        </div>
      </div>
      
      <div className={`tab-content ${activeTab === "chat" ? "active" : ""}`}>
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

      <div className={`tab-content ${activeTab === "steps" ? "active" : ""}`}>
        <div className="steps-container">
          <ul className="steps-list">
            {steps.map((step, idx) => (
              <li key={idx} className="step-item">
                <span className="step-agent">
                  <span className={`agent-icon ${
                    step.agent.toLowerCase().includes('planner') ? 'planner-icon' :
                    step.agent.toLowerCase().includes('orchestration') ? 'orchestration-icon' :
                    'edge-icon'
                  }`}>
                    <span className="material-icons">
                      {step.agent.toLowerCase().includes('planner') ? 'architecture' :
                       step.agent.toLowerCase().includes('orchestration') ? 'hub' :
                       'extension'}
                    </span>
                  </span>
                  {step.agent}
                </span>
                <span className="step-description">{step.description}</span>
                <span className={`step-status status-${step.status.toLowerCase()}`}>
                  {step.status}
                </span>
              </li>
            ))}
          </ul>
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
    </div>
  );
};

export default ChatBox;
