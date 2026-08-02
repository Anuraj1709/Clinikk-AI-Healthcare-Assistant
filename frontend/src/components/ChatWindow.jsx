import { useEffect, useRef, useState } from "react";
import { sendMessage } from "../services/api";
import ChatBubble from "./ChatBubble";
import MessageInput from "./MessageInput";

function ChatWindow() {

    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content:
                "👋 Hello! I'm Clinikk AI Assistant.\n\nHow can I help you today?"
        }
    ]);

    const [loading, setLoading] = useState(false);

    // Generate one session id per browser session
    const sessionId = useRef(
        "session_" + Math.random().toString(36).substring(2, 10)
    );

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({

            behavior: "smooth"

        });

    }, [messages, loading]);

    const handleSend = async (text) => {

        const updatedMessages = [

            ...messages,

            {

                role: "user",

                content: text

            }

        ];

        setMessages(updatedMessages);

        setLoading(true);

        try {

            const response = await sendMessage(

                sessionId.current,

                text

            );

            setMessages([

                ...updatedMessages,

                {

                    role: "assistant",

                    content: response.response

                }

            ]);

        } catch (error) {

            setMessages([

                ...updatedMessages,

                {

                    role: "assistant",

                    content:
                        "⚠️ Sorry, I couldn't connect to the server."

                }

            ]);

        }

        setLoading(false);

    };

    return (

        <div className="chat-container">

            <div className="chat-header">

                🏥 Clinikk AI Assistant

            </div>

            <div className="chat-body">

                {

                    messages.map((msg, index) => (

                        <ChatBubble

                            key={index}

                            message={msg}

                        />

                    ))

                }

                {

                    loading && (

                        <div className="typing">

                            🤖 Typing...

                        </div>

                    )

                }

                <div ref={bottomRef}></div>

            </div>

            <MessageInput

                onSend={handleSend}

            />

        </div>

    );

}

export default ChatWindow;