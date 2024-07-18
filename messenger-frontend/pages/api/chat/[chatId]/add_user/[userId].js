import axios from 'axios';

export default async function handler(req, res) {
  const { chatId, userId } = req.query;
  if (req.method === 'POST') {
    try {
      const response = await axios.post(`http://localhost:8100/chat/${chatId}/add_user/${userId}`);
      res.status(200).json(response.data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
