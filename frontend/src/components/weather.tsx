import React from "react";

interface WeatherState {
  temperature: number;
  conditionIndex: 0 | 1 | 2;
  condition: "Sunny" | "Cloudy" | "Rainy";
}

const Weather: React.FC = () => {
  const conditions = ["Sunny", "Cloudy", "Rainy"] as const;
  const index = 2 as const;

  const weather: WeatherState = {
    temperature: 23,
    conditionIndex: index,
    condition: conditions[index],
  };

  const getWeatherImage = () => {
    const imageMap = {
      0: "/images/weather/Sunny.png",
      1: "/images/weather/Cloudy.png",
      2: "/images/weather/Rainy.png"
    };
    
    return (
      <img 
        src={imageMap[weather.conditionIndex]} 
        alt={weather.condition}
        className="weather-image"
      />
    );
  };

  return (
    <div className="dashboard-box weather-widget">
      <h2>Weather</h2>
      <div className="weather-wrapper">
        <div className={`weather-tube ${weather.condition.toLowerCase()}`}>
          <div className="weather-image">{getWeatherImage()}</div>
          <div className="temperature">{weather.temperature}°C</div>
        </div>
        <div className="condition-label">{weather.condition}</div>
      </div>
    </div>
  );
};

export default Weather;
