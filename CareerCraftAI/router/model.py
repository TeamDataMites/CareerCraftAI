from fastapi import APIRouter
from utils.chat.mindmap.agent import mindmap_agent

router = APIRouter(
    prefix="/prediction",
    tags=["models"]
)


@router.get("/mindmap/", 
            description="Generate a mindmap from a job description.", 
            summary="endpoint access the llm agents to generate mindmap"
            )
async def mindmap(desc: str):
    mermaid_code: str = mindmap_agent(
        desc
    )
    return {"code": mermaid_code}
