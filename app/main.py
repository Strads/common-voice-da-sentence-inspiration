from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from random import sample
#%% Find missing words. 
with open("Data/da_unused_words.csv", "r") as fp:
    data = fp.read()
    unused_words = data.split("\n")

#%% Create API
# Global variable initialzed only once
# Initialize fastapi application
app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def root():
    sampled_words = sample(unused_words, 10)
    url_words = [f'<a href="{"https://ordnet.dk/ddo/ordbog?query=" + x}">{x}</a>' for x in sampled_words]
    return_str = "Disse ord optræder ikke i Common Voice sætninger på dansk - kan du finde på nogen? <br>" + '<br>'.join(url_words)
    return return_str