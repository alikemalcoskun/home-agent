import React from "react";
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

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Dashboard</h1>
      <div className="dashboard-grid">
        <ChatBox />
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
