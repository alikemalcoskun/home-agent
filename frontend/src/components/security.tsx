import React, { useState, useEffect, useCallback, useRef } from "react";

interface SecurityState {
  occupancy: boolean | null;
  status: "normal" | "error" | "loading" | "network_error";
  loading: boolean;
  error: string | null;
  previousOccupancy: boolean | null;
}

interface SecurityProps {
  handleSend: (input: string, owner?: string) => Promise<void>;
}

const Security: React.FC<SecurityProps> = ({ handleSend }) => {
  const [securityData, setSecurityData] = useState<SecurityState>({
    occupancy: null,
    status: "loading",
    loading: true,
    error: null,
    previousOccupancy: null,
  });

  const alertInProgress = useRef(false);

  const sendSecurityMessage = async (occupancyStatus: boolean) => {
    if (alertInProgress.current) {
      console.log("Alert already in progress, skipping...");
      return;
    }
    
    alertInProgress.current = true;
    const message = `Occupancy: ${occupancyStatus ? 'True' : 'False'}. Inform user and take action`;
    
    try {
      await handleSend(message, "security_agent");
      console.log("Security alert sent successfully");
    } catch (error) {
      console.error("Error sending security alert:", error);
    } finally {
      // Reset the flag after a short delay
      setTimeout(() => {
        alertInProgress.current = false;
      }, 1000);
    }
  };

  const fetchOccupancy = async () => {
    const response = await fetch("https://sensors.davidoglu.vip/api/v1/iot-1/occupancy");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Occupancy API response:", data);
    
    if (data.status === "success") {
      return data.message !== undefined ? (data.message === 1) : null;
    }
    
    // API returned error status but it's not a network error
    console.warn("Occupancy API returned error status:", data);
    return null;
  };

  const fetchSecurityData = useCallback(async () => {
    try {
      setSecurityData(prev => ({ ...prev, loading: true, error: null }));
      
      const occupancy = await fetchOccupancy();

      setSecurityData(prev => {
        // Only alert if occupancy changes from false/null to true
        const shouldAlert = occupancy === true && 
                           prev.occupancy !== true; // Previous was not true (either false or null)
        
        console.log("Security Debug:", {
          previousOccupancy: prev.occupancy,
          currentOccupancy: occupancy,
          shouldAlert
        });
        
        if (shouldAlert) {
          console.log("Sending security alert!");
          sendSecurityMessage(occupancy);
        }

        return {
          occupancy,
          status: "normal",
          loading: false,
          error: null,
          previousOccupancy: prev.occupancy, // Store current as previous for next comparison
        };
      });
    } catch (error) {
      console.error("Network error:", error);
      setSecurityData(prev => ({
        ...prev,
        loading: false,
        status: "network_error",
        error: "Network problem"
      }));
    }
  }, []);

  useEffect(() => {
    // Initial fetch
    fetchSecurityData();

    // Set up polling every 10 seconds
    const interval = setInterval(fetchSecurityData, 10000);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, [fetchSecurityData]);

  const getOccupancyColor = () => {
    if (securityData.occupancy === null) return "var(--color-dark)";
    return securityData.occupancy ? "#E94B3C" : "#7ED321"; // Green if not occupied, Red if
  };

  const getStatusMessage = () => {
    if (securityData.loading) return "Updating...";
    if (securityData.status === "network_error") return "Network problem";
    return "Live data";
  };

  const getStatusIcon = () => {
    if (securityData.loading) return "sync";
    if (securityData.status === "network_error") return "wifi_off";
    return "wifi";
  };

  const getStatusColor = () => {
    if (securityData.status === "network_error") return "var(--color-orange)";
    return "var(--color-dark)";
  };

  const getOccupancyText = () => {
    if (securityData.occupancy === null) return "N/A";
    return securityData.occupancy ? "Occupied" : "Empty";
  };

  const getOccupancyIcon = () => {
    if (securityData.occupancy === null) return "help_outline";
    return securityData.occupancy ? "person" : "person_off";
  };

  const getOccupancyClass = () => {
    if (securityData.occupancy === null) return "unknown";
    return securityData.occupancy ? "occupied" : "empty";
  };

  return (
    <div className="dashboard-box security-widget">
      <h2>
        <span className="material-icons" style={{ marginRight: "8px", verticalAlign: "middle" }}>
          security
        </span>
        Security
      </h2>
      <div className="security-wrapper">
        <div className="security-data">
          <div className={`occupancy-section ${getOccupancyClass()}`}>
            <div 
              className="occupancy-display"
              style={{ color: getOccupancyColor() }}
            >
              <div className="security-icon">
                <span className="material-icons">{getOccupancyIcon()}</span>
              </div>
              <span className="occupancy-value">
                {getOccupancyText()}
              </span>
              <span className="occupancy-label">Occupancy</span>
            </div>
          </div>
        </div>
        
        <div className={`status-indicator ${securityData.status}`} style={{ color: getStatusColor() }}>
          <span className="material-icons status-icon">{getStatusIcon()}</span>
          <span className="status-text">{getStatusMessage()}</span>
        </div>
      </div>
    </div>
  );
};

export default Security;
