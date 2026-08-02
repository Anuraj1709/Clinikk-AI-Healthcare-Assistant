function ChatBubble({ message }) {

    const isUser = message.role === "user";

    return (

        <div className={isUser ? "user-row" : "bot-row"}>

            <div className={isUser ? "user-bubble" : "bot-bubble"}>

                {message.content}

            </div>

        </div>

    );

}

export default ChatBubble;