import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export default function useSimulationStream() {
  const [data, setData] = useState(null);

  useEffect(() => {
    console.log("🔌 Connecting to Socket.IO...");

    const socket = io("http://localhost:5000", {
      transports: ["websocket"],
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
    });

    socket.on("connect", () => {
      console.log("Connected to backend socket.io");
      window.socketConnected = true;   // For debugging
    });

    socket.on("simulation_update", (payload) => {
      console.log(" Received simulation update:", payload);
      setData(payload);
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from backend");
      window.socketConnected = false;
    });

    return () => socket.disconnect();
  }, []);

  return data;
}
