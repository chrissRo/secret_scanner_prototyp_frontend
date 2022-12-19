from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body
from starlette.requests import Request

from app.server.controllers.findings_controller import retrieve_all_findings, set_false_positive, retrieve_finding
from app.server.models.false_positive import FalsePositiveModel
from app.server.models.finding_model import ResponseModel, ErrorResponseModel, FindingModel, UpdateFindingModel

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

@router.put('/{finding_id}', response_description='Update false-positive-assignment', )
async def put_false_positive(finding_id: str, update_finding_model: UpdateFindingModel = Body(...)):

    update_result = await set_false_positive(finding_id=finding_id, update_false_positive=update_finding_model)

    if update_result.modified_count == 1:
        finding = await retrieve_finding(finding_id=finding_id)
        return ResponseModel(finding, 'Finding updated successfully')
    return ErrorResponseModel('An error occurred.', 500, 'Could not update finding {}'.format(finding_id))
