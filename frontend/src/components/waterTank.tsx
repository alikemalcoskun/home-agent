import React, { useState } from "react";

const WaterTank: React.FC = () => {
  const [level] = useState<number>(56);

  return (
    <div className="dashboard-box water-widget">
      <h2>Water Level</h2>
      <div className="tank-wrapper">
        <div className="tank">
          <div
            className="water"
            style={{ height: `${level}%` }}
          />
        </div>
        <div className="level-label">{level}% left in the tank.{level <= 15 ? " More water is ordered." : ""}</div>
      </div>
    </div>
  );
};

export default WaterTank;
