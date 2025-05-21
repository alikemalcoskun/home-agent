import React, { useState } from "react";

interface Room {
  name: string;
  isOn: boolean;
}

const initialRooms: Room[] = [
  { name: "Kitchen", isOn: false },
  { name: "Barbecue", isOn: true },
];

const Stove: React.FC = () => {
  const [rooms, setRooms] = useState<Room[]>(initialRooms);
  
  const toggleStove = (index: number) => {
    const updated = [...rooms];
    updated[index].isOn = !updated[index].isOn;
    setRooms(updated);
  };

  return (
    <div className="dashboard-box stove-widget">
      <h2>Stoves</h2>
      <div className="room-list">
        {rooms.map((room, index) => (
          <div
            key={room.name}
            className={`room ${room.isOn ? "stove-on" : "stove-off"}`}
            onClick={() => toggleStove(index)}
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

export default Stove;
