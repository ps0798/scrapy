from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
from Scraper.scrape import Scraper
from fastapi.staticfiles import StaticFiles
from constants import SEED_URL
from utilities.authenticate import verify_token
from config import get_settings


scrapy = Scraper(base_url=SEED_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("MSG:: I'm getting loaded....")
    yield
    print("MSG:: I'm getting shutdown....")
    await scrapy.shut_down()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/scrape", dependencies=[Depends(verify_token)])
async def entry_point(req: Request):
    result = await scrapy.scrape(skip_index_in_first_page=True, page_limit=5)
    return {
        "scraped_data": result
    }
