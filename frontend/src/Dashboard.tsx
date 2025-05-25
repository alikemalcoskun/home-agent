import React, { useState, useRef, useCallback } from "react";
import Calendar from "./components/calendar";
import Email from "./components/email";
import Light from "./components/light";
import News from "./components/newspaper";
import Shopping from "./components/shopping";
import Stove from "./components/stove";
import WaterTank from "./components/waterTank";
import Weather from "./components/weather";
import Window from "./components/window";
import ChatBox from "./components/chatBox";
import RoomTemperature from "./components/roomTemperature";
import Security from "./components/security";

interface Message {
  text: string;
  sender: "user" | "system";
  type?: "processing" | "completed" | "error";
  data?: any;
}

interface TaskResponse {
  task_id: string;
}

interface ChatBoxRef {
  connect: (taskId: string) => void;
}

const Dashboard: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const chatBoxRef = useRef<ChatBoxRef>(null);

  const addMessage = useCallback((message: Message) => {
    setMessages((prev: Message[]) => [...prev, message]);
  }, []);

  const handleSend = useCallback(async (input: string, owner: string = "user") => {
    if (input.trim() === "") return;

    const userMessage: Message = {
      text: input,
      sender: "user",
    };

    setMessages((prev: Message[]) => [...prev, userMessage]);

    try {
      const response = await fetch("http://localhost:5172/api/v2/async/agent/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input, owner: owner }),
      });

      const data: TaskResponse = await response.json();

      if (response.ok) {
        setCurrentTaskId(data.task_id);
        // Connect to WebSocket if chatBox is available
        if (chatBoxRef.current) {
          chatBoxRef.current.connect(data.task_id);
        }
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
  }, [addMessage]);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Dashboard</h1>
      <div className="dashboard-grid">
        <ChatBox 
          ref={chatBoxRef}
          messages={messages}
          setMessages={setMessages}
          currentTaskId={currentTaskId}
          setCurrentTaskId={setCurrentTaskId}
          handleSend={handleSend}
          addMessage={addMessage}
        />
        <RoomTemperature />
        <Security handleSend={handleSend} />
        <Calendar />
        <Email />
        <Light />
        <News />
        <Shopping />
        <Stove />
        <WaterTank />
        <Weather />
        <Window />
      </div>
    </div>
  );
};

export default Dashboard;
