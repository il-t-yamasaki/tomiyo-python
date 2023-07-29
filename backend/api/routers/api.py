import os
from typing import Dict, List, TypedDict

from fastapi import APIRouter, Depends, HTTPException

ENVIRON = os.environ['ENVIRON']

router = APIRouter()


@router.get("/oniku")
async def get_list_oniku() -> Dict:

    if ENVIRON == 'dev':
        response = {
                    'name': 'chiken',
                    'power': '5',
                   }
    elif ENVIRON == 'prd':
        response = {
                    'name': 'beef',
                    'power': '20',
                   }                   
        
    return response
