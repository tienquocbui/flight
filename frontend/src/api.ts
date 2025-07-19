import axios from "axios";

// API Base URL - Production (Render)
const API_BASE = process.env.REACT_APP_API_URL || "https://flight-mupy.onrender.com";

export const getAirspace = () => axios.get(`${API_BASE}/airspace`);
export const getFlights = () => axios.get(`${API_BASE}/flights`);
export const addFlight = (flight: any) => axios.post(`${API_BASE}/flights`, flight);
export const getConflicts = () => axios.get(`${API_BASE}/conflicts`);
export const suggestPath = (data: { callsign: string, start: string, goal: string }) =>
  axios.post(`${API_BASE}/suggest_path`, data);
export const getStats = () => axios.get(`${API_BASE}/stats`); 