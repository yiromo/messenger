import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const formData = new URLSearchParams();
      formData.append('username', req.body.username);
      formData.append('password', req.body.password);

      const response = await axios.post('http://localhost:8100/auth/login/', formData);
      res.status(201).json(response.data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
