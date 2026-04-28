import os
from dotenv import load_dotenv
from groq import Groq

def create_client():
    load_dotenv()
    key=os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")
    return Groq(api_key=key)

def prompting(md):
    system_prompt= '''You must assume the role of an English writing professor.
    The user enters a specific mood or emotion. 
    Your job is to create an evocative and interesting writing prompt solely 
    in accordance with that specific mood without driving the user towards 
    a specific plot or idea.Do not end on an instructional note.
    Only output the prompt,nothing else. Keep it to 2-3 sentences, do not exceed 30 words total.
    Generate a new prompt each time, no repitition of same prompt allowed.'''

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

def printing_prompt(resp):
    prompt= resp.choices[0].message.content
    print("✒Your writing prompt is:\n")
    print(prompt)

mood = input("How are you feeling today? ").strip()
rsp=prompting(mood)
printing_prompt(rsp)
