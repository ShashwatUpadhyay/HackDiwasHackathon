from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from course.models import Course, CourseCategory, CourseSubCategory, Lesson, Enrollment
from account.models import Teacher, Student
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings

def get_context_data(user_message):
    """Get relevant context data based on user query"""
    context = ""
    
    try:
        # Check if query is about courses
        if any(keyword in user_message.lower() for keyword in ['course', 'class', 'learn', 'study', 'lesson']):
            courses = Course.objects.filter(is_active=True)[:5]
            if courses.exists():
                context += "\nAvailable Courses:\n"
                for course in courses:
                    teacher_name = course.teacher.full_name if course.teacher else "Unknown Teacher"
                    price = f"₹{course.discount_price}" if course.discount_price and course.discount_price > 0 else "Free"
                    context += f"- {course.title} by {teacher_name} ({price})\n"
        
        # Check if query is about teachers/instructors
        if any(keyword in user_message.lower() for keyword in ['teacher', 'instructor', 'tutor', 'mentor']):
            teachers = Teacher.objects.filter(verified=True)[:5]
            if teachers.exists():
                context += "\nAvailable Teachers:\n"
                for teacher in teachers:
                    category_name = teacher.category.name if teacher.category else 'General'
                    course_count = getattr(teacher, 'course_count', 0)
                    context += f"- {teacher.full_name} - {category_name} ({course_count} courses)\n"
        
        # Check if query is about categories
        if any(keyword in user_message.lower() for keyword in ['category', 'type', 'subject', 'dance', 'yoga', 'music']):
            categories = CourseCategory.objects.all()
            if categories.exists():
                context += "\nCourse Categories:\n"
                for category in categories:
                    description = category.description if hasattr(category, 'description') and category.description else 'Various courses available'
                    context += f"- {category.name}: {description}\n"
        
        # Check if query is about pricing
        if any(keyword in user_message.lower() for keyword in ['price', 'cost', 'fee', 'payment', 'free']):
            free_courses = Course.objects.filter(is_free=True, is_active=True).count()
            paid_courses = Course.objects.filter(is_free=False, is_active=True).count()
            context += f"\nPricing Info:\n- Free courses available: {free_courses}\n- Paid courses available: {paid_courses}\n"
    
    except Exception as e:
        context = "\nPlatform: Rythm Connect - Online learning platform for dance, music, and cultural arts."
    
    return context

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Get context data based on user query
            context = get_context_data(user_message)
            
            # Prepare the prompt for Gemini
            system_prompt = f"""You are a helpful assistant for Rythm Connect, an online learning platform for dance, music, and cultural arts. 
            
            Platform Context:
            {context}
            
            Please provide helpful, accurate, and friendly responses about courses, teachers, categories, pricing, and general platform information. 
            If users ask about specific courses or teachers, provide relevant details from the context above.
            Keep responses concise but informative."""
            
            # Call Gemini API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
                    }]
                }]
            }
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        bot_response = candidate['content']['parts'][0]['text']
                        return JsonResponse({'response': bot_response})
                    else:
                        return JsonResponse({'error': 'Invalid response structure from AI'}, status=500)
                else:
                    return JsonResponse({'error': 'No candidates in AI response'}, status=500)
            else:
                return JsonResponse({'error': f'API Error: {response.status_code}'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Provide a fallback response
            fallback_responses = {
                'hi': 'Hello! Welcome to Rythm Connect! How can I help you today?',
                'hello': 'Hi there! I\'m here to help you with information about our courses, teachers, and platform. What would you like to know?',
                'help': 'I can help you with information about courses, teachers, pricing, and general platform questions. Just ask me anything!'
            }
            
            user_msg_lower = user_message.lower().strip()
            if user_msg_lower in fallback_responses:
                return JsonResponse({'response': fallback_responses[user_msg_lower]})
            else:
                return JsonResponse({'response': 'Hello! I\'m your Rythm Connect assistant. I can help you with information about our courses, teachers, and platform. What would you like to know?'})
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
