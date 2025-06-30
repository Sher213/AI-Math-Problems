# StudyAI - AI Study Companion App

A real-time AI study companion that uses your camera to provide instant tutoring help. The app overlays study assistance in a chat interface while maintaining focus on your study materials.

## Features

- Real-time camera feed for study material capture
- AI-powered study assistance
- Voice feedback with visual audio visualization
- Gesture-controlled chat interface
- Seamless interaction without breaking focus

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8 or higher
- Expo CLI
- OpenAI API key

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with:
```
OPENAI_API_KEY=your_openai_api_key
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the StudyAI directory:
```bash
cd StudyAI
```

2. Install dependencies:
```bash
npm install
```

3. Start the Expo development server:
```bash
npm start
```

4. Use the Expo Go app on your mobile device to scan the QR code, or press 'a' to run on an Android emulator.

## Usage

1. Open the app and grant camera permissions
2. Point your camera at the study material you need help with
3. Tap the record button to capture and process the material
4. The AI will respond with voice feedback and text in the chat interface
5. Swipe up to view the chat history
6. Swipe down to minimize the chat interface

## Development

- The backend is built with FastAPI and uses WebSocket for real-time communication
- The frontend is built with React Native and Expo
- The app uses the OpenAI API for AI-powered responses
- Voice synthesis is handled by Expo's Speech API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 