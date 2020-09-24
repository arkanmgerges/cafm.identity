"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import hashlib
import os
import traceback
from email.utils import formatdate
from src.resource.logging.logger import logger

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import Response, FileResponse
from starlette.status import HTTP_403_FORBIDDEN, HTTP_304_NOT_MODIFIED, \
    HTTP_500_INTERNAL_SERVER_ERROR

from fastapi.security import HTTPBearer
from starlette.requests import Request

router = APIRouter()
SECRET_TOKEN = os.environ.get('SECRET_TOKEN', None)

import tarfile
import os.path


def makeTarFile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


class CustomHttpBearer(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request):
        ret = await super().__call__(request)
        if ret is not None and ret.credentials != SECRET_TOKEN:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )


def etagFrom(statResult: os.stat_result) -> str:
    etagBase = str(statResult.st_mtime) + "-" + str(statResult.st_size)
    return hashlib.md5(etagBase.encode()).hexdigest()


def lastModifiedFrom(statResult: os.stat_result) -> str:
    return formatdate(statResult.st_mtime, usegmt=True)


@router.get(path="/bundle.tar.gz", summary='Get bundle')
async def getAllOpaBundles(request: Request, _=Depends(CustomHttpBearer())):
    """Return all open policy agent bundles
    """
    try:
        # return Response(content = 'ok', media_type = 'text/html')
        # filePath = os.path.dirname(os.path.abspath(__file__)) + '/../../../artifact/bundle.tar.gz'
        filePath = os.environ.get('ARTIFACT_FOLDER_PATH', None)
        if filePath is None:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not find bundle file. Please verify that the file is in the right path",
            )
        filePath = f'{filePath}/bundle.tar.gz'
        statResult = os.stat(filePath)
        logger.info(f'Bundle file path: {filePath}')

        ifNoneMatch = request.headers.get('if-none-match')
        etag = etagFrom(statResult)
        if etag == ifNoneMatch:
            return Response(status_code=HTTP_304_NOT_MODIFIED)
        return FileResponse(filePath, media_type='application/gzip')
    except HTTPException as e:
        raise e
    except:
        logger.warning(traceback.format_exc())
        return []
