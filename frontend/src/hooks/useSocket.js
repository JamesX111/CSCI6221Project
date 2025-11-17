// src/hooks/useSocket.js
import { useEffect, useRef } from "react";
import { io } from "socket.io-client";

const SOCKET_URL = "http://localhost:5000";

export default function useSocket() {
  const socketRef = useRef(null);

  useEffect(() => {
    // Create socket connection ONLY once
    socketRef.current = io(SOCKET_URL, {
      transports: ["websocket"],
      reconnection: true,
    });

    console.log("🔌 Socket connected:", SOCKET_URL);

    const socket = socketRef.current;

    socket.on("connect", () => {
      console.log("🟢 Socket.IO connected:", socket.id);
    });

    socket.on("disconnect", () => {
      console.log("🔴 Socket.IO disconnected");
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  return socketRef;
}
