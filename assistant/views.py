# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY
from django.template.loader import render_to_string
from django.template.loader import get_template
# this is the home view for handling home page logic
def home(request):
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            formatted_response = openai.Completion.create(
                    model="davinci:ft-personal-2023-05-17-11-29-54",
                    prompt=prompt)

            # call the openai API
            a=formatted_response.choices
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": a[0].text})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }   
            return render(request, 'home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'home.html', context)

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')

# this is the view for handling errors
def error_handler(request):
    return render(request, 'error.html')
#def generate_sql_query(question):
#    response = openai.Completion.create(
#     model="davinci:ft-personal-2023-05-17-11-29-54"
#     prompt=f"Convert the following natural language question into a SQL query:\n\n{question}\n\nSQL Query:",
#      max_tokens=1000,
#      n=1,
#      stop=None,
#      temperature=0.5,
#    )
#    return response.choices[0].text.strip()