import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'PUT') {
    try {
      const response = await axios.put('http://localhost:8100/user/update_username', req.body);
      res.status(200).json(response.data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
