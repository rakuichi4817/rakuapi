from fastapi import APIRouter, Depends

from app.schemas import samples


router = APIRouter()


@router.get("/plus", response_model=samples.AddOut)
def add(query: samples.AddIn = Depends()):
    """# 足し算

    ## Parameters

    - a (int | float): 足される数
    - b (int | float): 足す数
    """
    return {"result": query.a + query.b}
