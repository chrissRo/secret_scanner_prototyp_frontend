from fastapi import APIRouter

from app.server.controllers.findings_controller import retrieve_all_findings
from app.server.models.finding_model import ResponseModel, ErrorResponseModel

router = APIRouter()

#####################################
# GET
#####################################

@router.get('/', response_description='Get all findings')
async def get_all_findings():
    findings = await retrieve_all_findings()
    if findings:
        return ResponseModel(findings, 'All findings retrieved successfully')
    else:
        return ErrorResponseModel('An error occurred.', 500, 'Could not retrieve findings.')

#####################################
# PUT
#####################################

@router.put('/', response_description='Update false-positive-assignment')
async def put_false_positive():
    pass
