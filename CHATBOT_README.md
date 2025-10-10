# Rythm Connect Chatbot Implementation

## Overview
A smart chatbot powered by Google's Gemini AI that helps users with queries about courses, teachers, pricing, and general platform information.

## Features
- **AI-Powered Responses**: Uses Google Gemini API for intelligent responses
- **Context-Aware**: Provides relevant information based on database content
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Chat**: Instant responses with typing indicators
- **Always Available**: Fixed position in bottom-right corner of all pages

## Implementation Details

### Backend (Django)
- **API Endpoint**: `/chatbot/` (POST)
- **View**: `chatbot.views.gemini_chat`
- **Context Data**: Automatically fetches relevant course, teacher, and category information
- **Error Handling**: Comprehensive error handling for API failures

### Frontend (HTML/CSS/JavaScript)
- **Component**: `templates/components/chatbot.html`
- **JavaScript**: `static/js/chatbot.js`
- **Styling**: Embedded CSS with modern design
- **Integration**: Included in base template for all pages

### Key Files Modified/Created
1. `hd/settings.py` - Added Gemini API key configuration
2. `hd/urls.py` - Added chatbot URL routing
3. `chatbot/views.py` - Complete chatbot logic with context awareness
4. `chatbot/urls.py` - Chatbot URL patterns
5. `templates/components/chatbot.html` - Chatbot UI component
6. `static/js/chatbot.js` - Frontend JavaScript functionality
7. `templates/index.html` - Added chatbot to base template

## API Configuration
The Gemini API key is configured in `hd/settings.py`:
```python
GEMINI_API_KEY = "AIzaSyBlQjtNAQblwQ3Az4jYG4hCmEbQhzfHqF4"
```

## Usage
1. The chatbot appears as a floating button in the bottom-right corner
2. Click the button to open the chat window
3. Type any question about courses, teachers, pricing, etc.
4. The AI will provide contextual responses based on your platform data

## Context Awareness
The chatbot automatically provides relevant information based on user queries:
- **Course queries**: Lists available courses with prices and teachers
- **Teacher queries**: Shows verified teachers with their specializations
- **Category queries**: Displays course categories and descriptions
- **Pricing queries**: Shows free vs paid course statistics

## Error Handling
- Network connectivity issues
- API rate limiting
- Invalid responses
- User-friendly error messages

## Responsive Design
- Desktop: 350px width chat window
- Mobile: Full-width chat window with adjusted positioning
- Smooth animations and transitions
- Modern gradient design with Bootstrap Icons

## Security
- CSRF protection enabled
- Input validation and sanitization
- API key stored securely in Django settings
- No sensitive data exposed in frontend
