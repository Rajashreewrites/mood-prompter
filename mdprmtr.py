import os #acceses environment variables from the operating system
from dotenv import load_dotenv #reads the .env file and loads the API key
from groq import Groq #the Groq library that connects to the AI API

#Loads API key from .env and returns a Groq client
def create_client():
    load_dotenv()
    key=os.getenv("GROQ_API_KEY")
    if not key:#Raises error if key is not found
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")
    return Groq(api_key=key)

#Sends the mood to the AI with instructions and returns the response(writing prompt)
def prompting(md):
     #System prompt includes specific instructions to the AI regarding the prompt that it will output
    system_prompt= '''You must assume the role of an English writing professor.
    The user enters a specific mood or emotion. 
    Your job is to create an evocative and interesting writing prompt solely 
    in accordance with that specific mood without driving the user towards 
    a specific plot or idea.Do not end on an instructional note.
    Only output the prompt,nothing else. Keep it to 2-3 sentences, do not exceed 30 words total.
    Generate a new prompt each time, no repitition of same prompt allowed.'''
    #User message sends the specific mood entered by user
    user_message=f"I'm currently feeling {md}. Give me a writing prompt"
    client= create_client()
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=300,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
             ]
    )
    return response

#Extracts and prints the writing prompt from the response
def printing_prompt(resp):
    prompt= resp.choices[0].message.content
    print("✒Your writing prompt is:\n")
    print(prompt)
    
#Main flow-- gets mood, generates prompt, prints writing prompt -- using methods
mood = input("How are you feeling today? ").strip()
rsp=prompting(mood)
printing_prompt(rsp)
