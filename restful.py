from interfaces.fastapi import twilio
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "✩░▒▓▆▅▃▂▁𝐬𝐚𝐭𝐫𝐢𝐚.𝐭𝐞𝐜𝐡𝐧𝐨𝐥𝐨𝐠𝐲▁▂▃▅▆▓▒░✩"


app.include_router(twilio.router)
