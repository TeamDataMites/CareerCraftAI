import requests
import os
import json
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from unstructured_client import UnstructuredClient
from unstructured_client.models import operations, shared

load_dotenv()

lixApiKey = os.getenv("LIX_API_KEY")
UnstructuredApiKey = os.getenv("UNSTRUCTURED_API_KEY")


client = UnstructuredClient(
    api_key_auth=UnstructuredApiKey,
    server_url='https://api.unstructured.io/general/v0/general'
)


class Profile(BaseModel):
    profile: str = Field(description="linkdin profile link")


class Posts(BaseModel):
    profile_id: str = Field(description="linkdin profile id")


@tool("get_linkdin_profile_tool", args_schema=Profile)
def get_linkdin_profile(profile: str) -> str:
    "used to get linkdin profile infomation of the individual."
    url = f"https://api.lix-it.com/v1/person?profile_link={profile}"

    payload={}

    headers = {
    'Authorization': lixApiKey
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def pdf_extractor(file_path: str) -> str:
    "used to extract text from pdf file."
    with open(file_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=file_path,
        )
    
    req = operations.PartitionRequest(
        shared.PartitionParameters(files=files, strategy=shared.Strategy.AUTO)
    )

    try:
        resp = client.general.partition(req)
        print(json.dumps(resp.elements, indent=2))
    except Exception as e:
        print(e)    
