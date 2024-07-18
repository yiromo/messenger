import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

const Chat = () => {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await axios.get('/api/chat');
        setChats(response.data);
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    };

    fetchChats();
  }, []);

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-xl font-bold mb-4">Chats</h1>
      <ul>
        {chats.map(chat => (
          <li key={chat.id}>
            <Link href={`/chat/${chat.id}`}>
              <a>{chat.name}</a>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Chat;
