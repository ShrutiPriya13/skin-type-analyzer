# Skin Type Detection and Recommendation Web App

## Description
Skin Type Detection and Recommendation is an AI-powered web app designed to help users determine their skin type and receive personalized skincare recommendations. The app offers two methods for skin type analysis:

1. Image Analysis: Users can upload their facial images, and the app will use machine learning models to classify their skin type.

2. Questionnaire: For those who prefer not to upload images, the app provides a series of questions to determine their skin type based on responses.

Once the skin type is detected, the app offers customized skincare tips and product recommendations to help users take better care of their skin.

## Features
- Skin Type Detection using AI and image analysis.

- Questionnaire-based Skin Type Classification for users who prefer not to upload images.

- Personalized Skincare Recommendations based on the detected skin type.

- User-friendly Web Interface for easy navigation and interaction.

## Screenshots
### Login Page 

![Login page](photos-for-readme/ss1.png)

### Home Page 
![Home page](photos-for-readme/ss2.png)

### Upload image for prediction via image
![Image page](photos-for-readme/ss3.png)

### Questionnaire-based prediction
![Question page](photos-for-readme/ss4.png)

### Recommended products after prediction
![Recommend page](photos-for-readme/ss5.png)

### Logout 
![Logout page](photos-for-readme/ss6.png)

## Technologies Used
- Frontend: HTML, CSS, JavaScript, React
- Backend: Node.js, Express
- Machine Learning: Python, TensorFlow, Keras (for skin type detection)
- Database: MongoDB (for storing user preferences and recommendations)
- Deployment: vercel

## Getting started

### Environment configuration
Create a .env file in the root directory and add necessary variables like DATABASE_URL, PORT, and SECRET_KEY.

### Installation
1. Clone the Repository
```bash
git clone https://github.com/your-username/skin-type-detection-and-recommendation.git
cd skin-type-detection-and-recommendation
```

2. Set Up the Backend
- Navigate to the backend folder:
```bash
cd backend
```

- Install the dependencies:
```bash
npm install
```

- Start the server:
```bash
npm start
```

3. Set Up the Frontend
- Navigate to the frontend folder:
```bash
cd frontend
```

- Install the dependencies:
```bash
npm install
```

- Start the frontend:
```bash
npm start
```

## Usage
1. Image Upload Method: Users can upload a clear facial image for analysis. The AI model will classify the skin type and display results.
2. Questionnaire Method: Users can answer a set of questions about their skin's characteristics. Based on their responses, the app will classify the skin type.
3. Recommendations: After determining the skin type, the app provides a set of skincare recommendations tailored to the user.

## Contributing
If you would like to contribute to this project, follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').

5. Push to the branch (git push origin feature-branch).

6. Create a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details
[MIT](LICENSE)
