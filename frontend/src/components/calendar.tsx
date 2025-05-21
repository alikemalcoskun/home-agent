import React, { useState } from "react";

const Calendar: React.FC = () => {
  const today = new Date();
  const [currentDate, setCurrentDate] = useState(new Date());

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    return new Date(year, month, 1).getDay();
  };

  const handlePrevMonth = () => {
    setCurrentDate((prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate((prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  };

  const daysInMonth = getDaysInMonth(currentDate);
  const firstDay = getFirstDayOfMonth(currentDate);
  const weeks: React.ReactNode[] = [];
  let day = 1;

  for (let i = 0; i < 6; i++) {
    const week: React.ReactNode[] = [];
    for (let j = 0; j < 7; j++) {
      if ((i === 0 && j < firstDay) || day > daysInMonth) {
        week.push(<td key={j}></td>);
      } else {
        const isToday =
          day === today.getDate() &&
          currentDate.getMonth() === today.getMonth() &&
          currentDate.getFullYear() === today.getFullYear();

        week.push(
          <td key={j} className={isToday ? "calendar-today" : ""}>
            {day}
          </td>
        );
        day++;
      }
    }
    weeks.push(week);
  }

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  return (
    <div className="dashboard-box calendar-widget">
      <h2>Calendar</h2>
      <div className="calendar-header">
        <button onClick={handlePrevMonth}>◀</button>
        <span>{monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}</span>
        <button onClick={handleNextMonth}>▶</button>
      </div>
      <table className="calendar-table">
        <thead>
          <tr>
            {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
              <th key={d}>{d}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeks.map((week, i) => (
            <tr key={i}>{week}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Calendar;
