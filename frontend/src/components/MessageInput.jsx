import { useState } from "react";

function MessageInput({ onSend }) {

    const [text, setText] = useState("");

    const handleSend = () => {

        if (!text.trim()) return;

        onSend(text);

        setText("");

    };

    return (

        <div className="input-container">

            <input

                type="text"

                placeholder="Type your message..."

                value={text}

                onChange={(e) => setText(e.target.value)}

                onKeyDown={(e) => {

                    if (e.key === "Enter") {

                        handleSend();

                    }

                }}

            />

            <button onClick={handleSend}>

                Send

            </button>

        </div>

    );

}

export default MessageInput;