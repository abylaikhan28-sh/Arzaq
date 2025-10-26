# arzaq
arzaq backend
## Backend API

### GET /api/health
# check if server is alive
- Description: Health check of the server
- Response: OK

### GET /api/spots
# get list of food spots
- Description: Get a list of food spots
- Response: JSON array, example:
[
  { "id": 1, "latitude": 43.24, "longitude": 76.89, "food_type": "bread" },
  { "id": 2, "latitude": 43.25, "longitude": 76.88, "food_type": "fruits" },
  { "id": 3, "latitude": 43.23, "longitude": 76.87, "food_type": "vegetables" }
]

### GET /api/user
# get user profile
- Description: Get a mock user profile
- Response: JSON object, example:
{
  "id": 101,
  "name": "Test Example",
  "email": "test@example.com",
  "location": { "latitude": 43.2389, "longitude": 76.8897 },
  "favorite_foods": ["bread", "fruits"]
}
