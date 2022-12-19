import json
from bson import json_util
from fastapi.encoders import jsonable_encoder
import pydantic

from ..database import findings_collection
# convert ObjectID to string
# https://stackoverflow.com/questions/71467630/fastapi-issues-with-mongodb-typeerror-objectid-object-is-not-iterable
from bson.objectid import ObjectId

from ..models.finding_model import FindingModel

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

#####################################
# GET
#####################################

# get all findings
async def retrieve_all_findings() -> list:
    findings = []
    async for finding in findings_collection.find():
        findings.append(finding)
    return findings

# get data to known ids
# Todo weitere filter-möglichkeiten, wie zum Beispiel scan-date oder creation-date
# oder nur hinterlegte false-positive
async def retrieve_findings(findings_ids: list) -> list:
    findings = []
    for finding_id in findings_ids:
        findings.append(await retrieve_finding(finding_id))
    return findings

# get single finding
async def retrieve_finding(finding_id) -> FindingModel:
    return await findings_collection.find_one({'_id': finding_id})

#####################################
# PUT
#####################################

# set false-positive
async def set_false_positive(finding: FindingModel) -> FindingModel:
    #return await findings_collection.update_one({finding}, {'$set': finding.falsePositive})
    pass