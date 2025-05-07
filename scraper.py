from firecrawl import FirecrawlApp, JsonConfig
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import json

load_dotenv()

app = FirecrawlApp()


class Product(BaseModel):
    """Schema for creating a new product"""

    url: str = Field(description="The URL of the product")
    name: str = Field(description="The product name/title")
    price: float = Field(description="The current price of the product")
    currency: str = Field(description="Currency code (USD, EUR, DKK, kr etc)")
    main_image_url: str = Field(description="The URL of the main image of the product")


GMT_PLUS_2 = timezone(timedelta(hours=2))


def scrape_product(url: str):
    extracted_data = app.scrape_url(
        url,
        formats=["extract"],
        extract={"schema": Product.model_json_schema()},
    )

    extracted_content = extracted_data.extract

    if isinstance(extracted_content, BaseModel):
        extracted_content = extracted_content.dict()

    extracted_content["timestamp"] = datetime.now(GMT_PLUS_2).isoformat()

    return extracted_content


if __name__ == "__main__":
    product = "https://www.sofanova.dk/produkt/sofa/chaiselong-sofaer/cozy-open-end-hjoernesofa/"  # "https://www.amazon.com/gp/product/B002U21ZZK/"

    print(scrape_product(product))
