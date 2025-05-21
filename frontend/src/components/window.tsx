import React, { useState } from "react";

interface Room {
  name: string;
  isOn: boolean;
}

const initialRooms: Room[] = [
  { name: "Living Room", isOn: false },
  { name: "Kitchen", isOn: false },
  { name: "Bedroom", isOn: true },
  { name: "Bathroom", isOn: false },
];

const Window: React.FC = () => {
  const [rooms, setRooms] = useState<Room[]>(initialRooms);
    
  const toggleWindow = (index: number) => {
    const updated = [...rooms];
    updated[index].isOn = !updated[index].isOn;
    setRooms(updated);
  };

  return (
    <div className="dashboard-box window-widget">
      <h2>Windows</h2>
      <div className="room-list">
        {rooms.map((room, index) => (
          <div
            key={room.name}
            className={`room ${room.isOn ? "window-on" : "window-off"}`}
            onClick={() => toggleWindow(index)}
          >
            <span className="room-name">{room.name}</span>
            <div className="switch">
              <div className="knob" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Window;
