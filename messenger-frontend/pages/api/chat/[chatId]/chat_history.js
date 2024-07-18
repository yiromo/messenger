import axios from 'axios';

export default async function handler(req, res) {
  const { chatId } = req.query;
  if (req.method === 'GET') {
    try {
      const response = await axios.get(`http://localhost:8100/chat/chat_history?chat_id=${chatId}`);
      res.status(200).json(response.data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
