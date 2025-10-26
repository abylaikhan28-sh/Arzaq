const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());

// Базовый маршрут для проверки
app.get('/api/health', (req, res) => {
  res.send('OK');
});

// Mock данные food spots
const foodSpots = [
  { id: 1, latitude: 43.24, longitude: 76.89, food_type: 'bread' },
  { id: 2, latitude: 43.25, longitude: 76.88, food_type: 'fruits' },
  { id: 3, latitude: 43.23, longitude: 76.87, food_type: 'vegetables' }
];

app.get('/api/spots', (req, res) => {
  res.json(foodSpots);
});

// Mock профиль пользователя
const userProfile = {
  id: 101,
  name: 'Test Example',
  email: 'test@example.com',
  location: { latitude: 43.2389, longitude: 76.8897 },
  favorite_foods: ['bread', 'fruits']
};

app.get('/api/user', (req, res) => {
  res.json(userProfile);
});

// Запуск сервера
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
