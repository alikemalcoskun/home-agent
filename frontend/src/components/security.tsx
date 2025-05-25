import React, { useState, useEffect, useCallback, useRef } from "react";

interface SecurityState {
  occupancy: boolean | null;
  safeBoxDoorStatus: "open" | "close" | null;
  status: "normal" | "error" | "loading" | "network_error";
  loading: boolean;
  error: string | null;
  previousOccupancy: boolean | null;
  previousSafeBoxDoorStatus: "open" | "close" | null;
}

interface SecurityProps {
  handleSend: (input: string, owner?: string) => Promise<void>;
}

const Security: React.FC<SecurityProps> = ({ handleSend }) => {
  const [securityData, setSecurityData] = useState<SecurityState>({
    occupancy: null,
    safeBoxDoorStatus: null,
    status: "loading",
    loading: true,
    error: null,
    previousOccupancy: null,
    previousSafeBoxDoorStatus: null,
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

  const sendSafeBoxDoorMessage = async () => {
    if (alertInProgress.current) {
      console.log("Alert already in progress, skipping safe box door alert...");
      return;
    }
    
    alertInProgress.current = true;
    const message = `Safe box door opened. Inform user and take action`;
    
    try {
      await handleSend(message, "security_agent");
      console.log("Safe box door alert sent successfully");
    } catch (error) {
      console.error("Error sending safe box door alert:", error);
    } finally {
      // Reset the flag after a short delay
      setTimeout(() => {
        alertInProgress.current = false;
      }, 1000);
    }
  };

  const fetchOccupancy = async () => {
    const response = await fetch("https://sensors.davidoglu.vip/api/v1/iot-2/occupancy");
    
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

  const fetchSafeBoxDoorStatus = async () => {
    const response = await fetch("https://sensors.davidoglu.vip/api/v1/iot-2/heading");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Safe box door API response:", data);
    
    if (data.status === "success") {
      const heading = data.message;
      if (heading !== undefined && heading !== null) {
        // if heading is in range of 0-180, it is open, close otherwise
        return heading < 180 ? "open" : "close";
      }
    }
    
    // API returned error status but it's not a network error
    console.warn("Safe box door API returned error status:", data);
    return null;
  };

  const fetchSecurityData = useCallback(async () => {
    try {
      setSecurityData(prev => ({ ...prev, loading: true, error: null }));
      
      const [occupancy, safeBoxDoorStatus] = await Promise.all([
        fetchOccupancy(),
        fetchSafeBoxDoorStatus()
      ]);

      setSecurityData(prev => {
        // Only alert if occupancy changes from false/null to true
        const shouldAlertOccupancy = occupancy === true && 
                                   prev.occupancy !== true; // Previous was not true (either false or null)
        
        // Only alert if safe box door changes from close/null to open
        const shouldAlertSafeBox = safeBoxDoorStatus === "open" && 
                                 prev.safeBoxDoorStatus !== "open"; // Previous was not open (either close or null)
        
        console.log("Security Debug:", {
          previousOccupancy: prev.occupancy,
          currentOccupancy: occupancy,
          previousSafeBoxDoorStatus: prev.safeBoxDoorStatus,
          currentSafeBoxDoorStatus: safeBoxDoorStatus,
          shouldAlertOccupancy,
          shouldAlertSafeBox
        });
        
        if (shouldAlertOccupancy) {
          console.log("Sending occupancy alert!");
          sendSecurityMessage(occupancy);
        }
        
        if (shouldAlertSafeBox) {
          console.log("Sending safe box door alert!");
          sendSafeBoxDoorMessage();
        }

        return {
          occupancy,
          safeBoxDoorStatus,
          status: "normal",
          loading: false,
          error: null,
          previousOccupancy: prev.occupancy, // Store current as previous for next comparison
          previousSafeBoxDoorStatus: prev.safeBoxDoorStatus,
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

    // Set up polling every 2 seconds
    const interval = setInterval(fetchSecurityData, 1000);

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

  const getSafeBoxDoorText = () => {
    if (securityData.safeBoxDoorStatus === null) return "N/A";
    return securityData.safeBoxDoorStatus === "open" ? "Open" : "Closed";
  };

  const getSafeBoxDoorIcon = () => {
    if (securityData.safeBoxDoorStatus === null) return "help_outline";
    return securityData.safeBoxDoorStatus === "open" ? "lock_open" : "lock";
  };

  const getSafeBoxDoorColor = () => {
    if (securityData.safeBoxDoorStatus === null) return "var(--color-dark)";
    return securityData.safeBoxDoorStatus === "open" ? "#E94B3C" : "#7ED321"; // Red if open, Green if closed
  };

  const getSafeBoxDoorClass = () => {
    if (securityData.safeBoxDoorStatus === null) return "unknown";
    return securityData.safeBoxDoorStatus === "open" ? "occupied" : "empty"; // Reuse occupied/empty classes for open/closed
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
          
          <div className={`occupancy-section ${getSafeBoxDoorClass()}`}>
            <div 
              className="occupancy-display"
              style={{ color: getSafeBoxDoorColor() }}
            >
              <div className="security-icon">
                <span className="material-icons">{getSafeBoxDoorIcon()}</span>
              </div>
              <span className="occupancy-value">
                {getSafeBoxDoorText()}
              </span>
              <span className="occupancy-label">Safe Box</span>
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
