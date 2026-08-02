import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

export const sendMessage = async (sessionId, message) => {

    const response = await API.post("/chat", {
        session_id: sessionId,
        message: message
    });

    return response.data;
};