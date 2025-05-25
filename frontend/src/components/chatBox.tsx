import React, { useState, useEffect, useRef, forwardRef, useImperativeHandle } from "react";
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

interface ChatBoxProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  currentTaskId: string | null;
  setCurrentTaskId: React.Dispatch<React.SetStateAction<string | null>>;
  handleSend: (input: string, owner?: string) => Promise<void>;
  addMessage: (message: Message) => void;
}

interface ChatBoxRef {
  connect: (taskId: string) => void;
}

type TabType = "chat" | "steps";

const ChatBox = forwardRef<ChatBoxRef, ChatBoxProps>(({ 
  messages, 
  setMessages, 
  currentTaskId, 
  setCurrentTaskId, 
  handleSend: parentHandleSend, 
  addMessage 
}, ref) => {
  const [input, setInput] = useState("");
  const [steps, setSteps] = useState<Step[]>([]);
  const [activeTab, setActiveTab] = useState<TabType>("chat");
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const stepsEndRef = useRef<HTMLDivElement>(null);
  
  const { isConnected, lastMessage, connect, disconnect } = useWebSocket();

  // Expose connect function to parent via ref
  useImperativeHandle(ref, () => ({
    connect
  }));

  const predeterminedQuestions = [
    "User leaves home",
    "Good morning! Update me on today!",
    "Open all the windows if it is sunny",
    "Who is the person traversing ropes to wipe windows or perform technical operations in tall buildings?",
    "Close all the windows if it is rainy",
    "Get the room temperature and humidity"
  ];

  const handleQuestionClick = (question: string) => {
    setInput(question);
  };

  const scrollToBottom = (ref: React.RefObject<HTMLDivElement | null>) => {
    if (ref.current) {
      const container = ref.current.parentElement;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  };

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      // Update steps from blackboard history
      if (lastMessage.blackboard?.history?.steps) {
        setSteps(lastMessage.blackboard.history.steps);
        setTimeout(() => scrollToBottom(stepsEndRef), 100);
      }

      // Only add messages that are completed or error
      if (lastMessage.status === "completed" || lastMessage.status === "error") {
        addMessage({
          text: formatMessage(lastMessage),
          sender: "system",
          type: lastMessage.status,
          data: lastMessage
        });
        setTimeout(() => scrollToBottom(messagesEndRef), 100);
      }
    }
  }, [lastMessage, addMessage]);

  // Scroll to bottom when messages or steps change
  useEffect(() => {
    if (activeTab === "chat") {
      scrollToBottom(messagesEndRef);
    } else {
      scrollToBottom(stepsEndRef);
    }
  }, [messages, steps, activeTab]);

  const formatMessage = (message: any): string => {
    if (message.status === "completed") {
      const steps = message.blackboard?.history?.steps || [];
      const orchestrationSteps = steps.filter((step: any) => 
        step.agent.toLowerCase().includes('orchestration')
      );
      const lastOrchestrationStep = orchestrationSteps[orchestrationSteps.length - 1];
      return lastOrchestrationStep?.description || "An error occurred. No message was generated.";
    }
    if (message.status === "error") {
      return `Error: ${message.error || "Unknown error"}`;
    }
    return JSON.stringify(message, null, 2);
  };

  const handleLocalSend = async (owner: string = "user") => {
    await parentHandleSend(input, owner);
    setInput("");
  };

  // Cleanup WebSocket connection when component unmounts
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return (
    <div className="dashboard-box chatbox-widget">
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
      
      <div className="question-cards-grid">
        {predeterminedQuestions.map((question, idx) => (
          <div 
            key={idx}
            className="question-card"
            onClick={() => handleQuestionClick(question)}
          >
            {question}
          </div>
        ))}
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
          <div ref={messagesEndRef} />
        </div>
        <div className="chatbox-input">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === "Enter" && handleLocalSend("user")}
          />
          <button onClick={() => handleLocalSend("user")}>Send</button>
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
          <div ref={stepsEndRef} />
        </div>
        <div className="chatbox-input">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === "Enter" && handleLocalSend()}
          />
          <button onClick={() => handleLocalSend()}>Send</button>
        </div>
      </div>
    </div>
  );
});

ChatBox.displayName = 'ChatBox';

export default ChatBox;
