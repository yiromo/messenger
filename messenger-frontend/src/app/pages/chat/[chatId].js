import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import axios from 'axios';

const ChatDetail = () => {
  const router = useRouter();
  const { chatId } = router.query;
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`/api/chat/chat_history?chat_id=${chatId}`);
        setMessages(response.data);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    if (chatId) {
      fetchMessages();
    }
  }, [chatId]);

  const handleSendMessage = async () => {
    try {
      await axios.post(`/api/chat/${chatId}/send_message`, { message: newMessage });
      setNewMessage('');
      // Optionally refetch messages or update state directly
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-xl font-bold mb-4">Chat</h1>
      <div className="mb-4">
        {messages.map((msg, index) => (
          <div key={index}>{msg.text}</div>
        ))}
      </div>
      <input
        type="text"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        className="border p-2 w-full mb-2"
      />
      <button onClick={handleSendMessage} className="bg-blue-500 text-white py-2 px-4 rounded">
        Send
      </button>
    </div>
  );
};

export default ChatDetail;
