import React, { useState, useEffect, useCallback } from "react";

interface RoomTemperatureState {
  temperature: number | null;
  humidity: number | null;
  status: "normal" | "error" | "loading" | "network_error";
  loading: boolean;
  error: string | null;
}

const RoomTemperature: React.FC = () => {
  const [roomData, setRoomData] = useState<RoomTemperatureState>({
    temperature: null,
    humidity: null,
    status: "loading",
    loading: true,
    error: null
  });

  const fetchTemperature = async () => {
    const response = await fetch("https://sensors.davidoglu.vip/api/v1/iot-1/temperature");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Temperature API response:", data);
    
    if (data.status === "success") {
      return data.message !== undefined ? data.message : null;
    }
    
    // API returned error status but it's not a network error
    console.warn("Temperature API returned error status:", data);
    return null;
  };

  const fetchHumidity = async () => {
    const response = await fetch("https://sensors.davidoglu.vip/api/v1/iot-1/humidity");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Humidity API response:", data);
    
    if (data.status === "success") {
      return data.message !== undefined ? data.message : null;
    }
    
    // API returned error status but it's not a network error
    console.warn("Humidity API returned error status:", data);
    return null;
  };

  const fetchRoomData = useCallback(async () => {
    try {
      setRoomData(prev => ({ ...prev, loading: true, error: null }));
      
      const [temperature, humidity] = await Promise.all([
        fetchTemperature(),
        fetchHumidity()
      ]);

      setRoomData({
        temperature,
        humidity,
        status: "normal",
        loading: false,
        error: null
      });
    } catch (error) {
      console.error("Network error:", error);
      setRoomData(prev => ({
        ...prev,
        loading: false,
        status: "network_error",
        error: "Network problem"
      }));
    }
  }, []);

  useEffect(() => {
    // Initial fetch
    fetchRoomData();

    // Set up polling every 10 seconds
    const interval = setInterval(fetchRoomData, 10000);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, [fetchRoomData]);

  const getTemperatureColor = () => {
    if (roomData.temperature === null) return "var(--color-dark)";
    if (roomData.temperature < 5) return "#4A90E2"; // Cold - Blue
    if (roomData.temperature > 30) return "#E94B3C"; // Hot - Red
    return "#7ED321"; // Normal - Green
  };

  const getHumidityColor = () => {
    if (roomData.humidity === null) return "var(--color-dark)";
    if (roomData.humidity < 30) return "#F5A623"; // Low - Orange
    if (roomData.humidity > 70) return "#4A90E2"; // High - Blue
    return "#7ED321"; // Normal - Green
  };

  const getStatusMessage = () => {
    if (roomData.loading) return "Updating...";
    if (roomData.status === "network_error") return "Network problem";
    return "Live data";
  };

  const getStatusIcon = () => {
    if (roomData.loading) return "sync";
    if (roomData.status === "network_error") return "wifi_off";
    return "wifi";
  };

  const getStatusColor = () => {
    if (roomData.status === "network_error") return "var(--color-orange)";
    return "var(--color-dark)";
  };    

  return (
    <div className="dashboard-box room-temperature-widget">
      <h2>
        <span className="material-icons" style={{ marginRight: "8px", verticalAlign: "middle" }}>
          thermostat
        </span>
        Room Temperature
      </h2>
      <div className="room-temperature-wrapper">
        <div className="climate-data">
          <div className="temperature-section">
            <div 
              className="temperature-display"
              style={{ color: getTemperatureColor() }}
            >
              <div className="climate-icon">
                <span className="material-icons">device_thermostat</span>
              </div>
              <span className="temperature-value">
                {roomData.temperature !== null ? `${roomData.temperature}°C` : "N/A"}
              </span>
              <span className="temperature-label">Temperature</span>
            </div>
          </div>
          
          <div className="humidity-section">
            <div 
              className="humidity-display"
              style={{ color: getHumidityColor() }}
            >
              <div className="climate-icon">
                <span className="material-icons">water_drop</span>
              </div>
              <span className="humidity-value">
                {roomData.humidity !== null ? `${roomData.humidity}%` : "N/A"}
              </span>
              <span className="humidity-label">Humidity</span>
            </div>
          </div>
        </div>
        
        <div className={`status-indicator ${roomData.status}`} style={{ color: getStatusColor() }}>
          <span className="material-icons status-icon">{getStatusIcon()}</span>
          <span className="status-text">{getStatusMessage()}</span>
        </div>
      </div>
    </div>
  );
};

export default RoomTemperature; 