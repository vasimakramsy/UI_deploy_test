from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


import requests
import uvicorn
import json

import re




app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_api_replys(user_message):
    # actual logic to call your API
    
    # URL of the API
    api_url = "https://qagqb32tt2gslns7bvtt4pviam0cyhph.lambda-url.us-east-1.on.aws/"

    try:
        # Make a GET request to the API with the user's message as a query parameter
        response = requests.get(api_url, params={"query": user_message})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the API's response
            
            return response.text
        else:
            # If the request was not successful, raise an exception or handle it accordingly
            response.raise_for_status()
    except Exception as e:
        # Handle exceptions, log the error, or raise it
        print(f"Error: {e}")
        return "Error occurred while fetching API response."

def get_api_reply(result,prompt):
    # Replace this with the actual logic to call your API
    

    # print("raw result")
    # print(result)
    # print(prompt)

    
    phrase_to_remove = prompt
    
    # fake_reply = "what is the rule for Tahajud namaz?\n\nTahajjud is a special prayer that is performed in the late night or early morning hours. It is considered one of the most important and rewarding prayers in Islam, as it is said to be a means of seeking forgiveness, mercy, and guidance from Allah. Here are some general rules for performing Tahajjud:\n\n1. Time: Tahajjud is typically performed in the late night or early morning hours, after the last third of the night has passed and before the dawn breaks.\n2. Purpose: The purpose of Tahajjud is to seek forgiveness, mercy, and guidance from Allah. It is a time to reflect on one's actions and seek Allah's blessings and protection.\n3. Rituals: The rituals of Tahajjud are similar to those of the regular five daily prayers, with some additional requirements. These include:\n* Standing before Allah and performing the prayer with humility and concentration.\n* Reciting certain verses of the Quran, such as Surah Al-Fatihah and Surah Al-Ikhlas, and other supplications.\n* Performing the prayer with a pure heart and mind, free from any worldly attachments or distractions.\n* Making sure to perform the prayer in a clean and purified state, both physically and spiritually.\n4. Frequency: Tahajjud is recommended to be performed regularly, but it is not obligatory to perform it every night. Some Muslims perform it every night, while others may perform it only a few times a week or as needed.\n5. Importance: Tahajjud is considered one of the most important and rewarding prayers in Islam, as it is a means of seeking forgiveness, mercy, and guidance from Allah. It is also believed to be a way to purify the soul and seek Allah's protection and blessings.\n6. Conditions: There are certain conditions that must be met in order to perform Tahajjud properly. These include:\n* Being in a state of purity, both physically and spiritually.\n* Being in a clean and quiet place, free from any distractions or interruptions.\n* Having the intention to perform the prayer with a pure heart and mind.\n* Following the proper rituals and procedures for the prayer.\n"
    # text = f'ECHO:{user_message}'
    raw_reponse = result
    qa_removed_reply = raw_reponse.replace(phrase_to_remove, "")
    processed_reply = qa_removed_reply.replace('\n\n', '\n')
     
    # print("processed result") 
    # print(processed_reply)

    
    
    return processed_reply



# Login route
@app.get("/")
async def read_root(request: Request):
 
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/chat_response")
async def chat_resonse(request: Request, prompt: str = Form(...)):
    print(prompt)
    result = get_api_replys(prompt) 
    # result ="\nIn Islam, Qurbani (also known as Eid-al-Adha) is a significant festival that commemorates the willingness of Prophet Ibrahim (Abraham) to sacrifice his son Ismail (Ishmael) as an act of obedience to God. According to Islamic tradition, God intervened and replaced Ismail with a ram, thus saving his life.\n\nThe festival of Qurbani is celebrated on the 10th day of Dhu al-Hijjah, the 12th month of the Islamic calendar. On this day, Muslims around the world perform the ritual of Qurbani, which involves the sacrifice of an animal (usually a sheep, goat, or cow) to commemorate the sacrifice of Prophet Ibrahim and his willingness to obey God's command.\n\nThe Qurbani ritual involves several steps, including:\n\n1. Prayer: Muslims perform a special prayer called the \"Takbir\" before the sacrifice, asking God to accept their sacrifice.\n2. Cleanliness: The animal is to be in a state of purity, having been bathed and having its horns and hooves trimmed.\n3. Drawing lots: The family members draw lots to determine which animal will be sacrificed.\n4. Slaughtering: The animal is then slaughtered by a trained butcher, who must be in a state of purity, and the meat is distributed among the family, friends, and the poor.\n\nQurbani is considered a meritorious act in Islam, as it symbolizes the willingness to sacrifice one's desires for the sake of God's commandments. It is also seen as a way to promote social justice and compassion, as the meat is distributed among those in need.\n\nOverall, Qurbani is an important festival in Islam that commemorates the sacrifice of Prophet Ibrahim and his willingness to obey God's commandments. It is a time for Muslims to reflect on their own lives and priorities, and to rededicate themselves to serving God and their fellow human beings."
    result = get_api_reply(result,prompt)
    # print(request)
    
   
    
    #jsonify the response
    response_data = jsonable_encoder(json.dumps({"answer": result}))
    
    res = Response(response_data)
    return res

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)