import React, { useState } from "react";

interface Room {
  name: string;
  isOn: boolean;
}

const initialRooms: Room[] = [
  { name: "Living Room", isOn: false },
  { name: "Kitchen", isOn: true },
  { name: "Bedroom", isOn: false },
  { name: "Bathroom", isOn: false },
];

const Light: React.FC = () => {
  const [rooms, setRooms] = useState<Room[]>(initialRooms);

  const toggleLight = (index: number) => {
    const updated = [...rooms];
    updated[index].isOn = !updated[index].isOn;
    setRooms(updated);
  };

  return (
    <div className="dashboard-box light-widget">
      <h2>Lights</h2>
      <div className="room-list">
        {rooms.map((room, index) => (
          <div
            key={room.name}
            className={`room ${room.isOn ? "light-on" : "light-off"}`}
            onClick={() => toggleLight(index)}
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

export default Light;
