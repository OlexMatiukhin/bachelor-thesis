
# @app.post("/encrypt/file")
# async def encrypt_file_enpoint(
#         system:str=Form(...),
#         params: str = Form(...),
#         data_type:str=Form(...),
#         file: UploadFile = File(...),
# ):
#     try:
#         original_file = await file.read()
#         params_obj = json.loads(params)
#         encrypted_content = orchestrator.execute_request(
#             system_type=system,
#             system_params=params_obj,
#             crypt_method=data_type,
#             mode="bytes",
#             content=original_file,
#             process_type="encrypt",

#         )
#         in_name = file.filename
#         file_extention=Path(in_name).suffix.lstrip(".")
#         print(file)

#         print(in_name)
#         print(file_extention)
#         return Response(
#             content=encrypted_content,
#             media_type="application/octet-stream",
#             headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
#         )
#     except RuntimeError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")





# @app.post("/decrypt/file")
# async def decrypt_file_enpoint(
#         system:str=Form(...),
#         params: str = Form(...),
#         data_type:str=Form(...),
#         file: UploadFile = File(...),
# ):
#     try:
#         original_file = await file.read()
#         params_obj = json.loads(params)
#         decrypted_content = orchestrator.execute_request(
#             system_type=system,
#             system_params=params_obj,
#             crypt_method=data_type,
#             mode="bytes",
#             content=original_file,
#             process_type="decrypt",

#         )
#         in_name = file.filename
#         file_extention = Path(in_name).suffix.lstrip(".")

#         return Response(
#             content=decrypted_content,
#             media_type="application/octet-stream",
#             headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
#         )
#     except RuntimeError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")



# @app.post("/encrypt/audio")
# async def encrypt_audio_endpoint(
#         system: str = Form(...),
#         params: str = Form(...),
#         data_type: str = Form(...),
#         file: UploadFile = File(...),
# ):
#     params_obj = json.loads(params)

#     async def chunk_reader():
#         while chunk := await file.read(64 * 1024):
#             yield chunk

#     return StreamingResponse(
#         orchestrator.execute_request_stream(
#             system_type=system,
#             system_params=params_obj,
#             crypt_method=data_type,
#             mode="bytes",
#             data_stream=chunk_reader(),
#             process_type="encrypt",
#         ),
#         media_type="application/octet-stream",
#         headers={"Content-Disposition": 'attachment; filename="processed.bin"'},
#     )

# @app.post("/decrypt/audio")
# async def decrypt_audio_endpoint(
#         system: str = Form(...),
#         params: str = Form(...),
#         data_type: str = Form(...),
#         file: UploadFile = File(...),
# ):
#     params_obj = json.loads(params)

#     async def chunk_reader():
#         while chunk := await file.read(64 * 1024):
#             yield chunk

#     return StreamingResponse(
#         orchestrator.execute_request_stream(
#             system_type=system,
#             system_params=params_obj,
#             crypt_method=data_type,
#             mode="bytes",
#             data_stream=chunk_reader(),
#             process_type="decrypt",
#         ),
#         media_type="application/octet-stream",
#         headers={"Content-Disposition": 'attachment; filename="processed.bin"'},
#     )


import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from orchestrator import CryptoOrchestrator
from fastapi import FastAPI
from pathlib import Path
orchestrator=CryptoOrchestrator()
from fastapi import HTTPException
app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
expose_headers=["Content-Disposition"]
)


CLIENT_DIR = Path(__file__).resolve().parent.parent / "ChaosCipherClient"

async def read_upload_chunked(file: UploadFile, chunk_size: int = 64 * 1024) -> bytes:
    chunks = []
    while chunk := await file.read(chunk_size):
        chunks.append(chunk)
    return b"".join(chunks)

@app.get("/")
async def root():
    return FileResponse(CLIENT_DIR / "index.html")

@app.post("/encrypt/image")
async def encrypt_image_enpoint(
        system:str=Form(...),
        params: str = Form(...),
        data_type:str=Form(...),
        mode: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        original_file=await file.read()
        params_obj = json.loads(params)
        # mode = mode.strip().lower()
        # in_name = file.filename

        encrypted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            mode="",
            content=original_file,
            process_type="encrypt"
        )
        return Response(
            content=encrypted_content,
            media_type="image/png",
            headers={"Content-Disposition": 'attachment; filename=f"processed{}.png"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")

@app.post("/decrypt/image")
async def decrypt_image_enpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        mode: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        original_file = await file.read()
        mode = mode.strip().lower()
        params_obj = json.loads(params)
        decrted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            content=original_file,
            mode="",
            process_type="decrypt"
        )

        new_filename = f"processed_{file.filename}"
        return Response(
            content=decrted_content,
            media_type="image/png",
            headers={"Content-Disposition": 'attachment; filename="processed.png"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")
@app.post("/encrypt/text")
async def encrypt_text_ednpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        mode: str = Form(...),
        text:str=Form(...)
):
    try:
        mode = mode.strip().lower()
        params_obj = json.loads(params)
        encrypted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            mode=mode,
            content=text,
            process_type="encrypt"
        )
        print(mode)
        return {
            "status": "success",
            "processed_text": encrypted_content,
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")
@app.post("/decrypt/text")
async def decrypt_text_ednpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        mode: str = Form(...),
        text: str = Form(...)
):
    try:
        mode = mode.strip().lower()
        params_obj = json.loads(params)
        decrypted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            mode=mode,
            content=text,
            process_type="decrypt"
        )

        return {
            "status": "success",
            "processed_text": decrypted_content,
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")




@app.post("/encrypt/audio")
async def encrypt_audio_enpoint(
        system:str=Form(...),
        params: str = Form(...),
        data_type:str=Form(...),
        file: UploadFile = File(...),
):
    try:
        original_file = await file.read()
        params_obj = json.loads(params)
        encrypted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            mode="bytes",
            content=original_file,
            process_type="encrypt"
        )
        in_name = file.filename
        file_extention=Path(in_name).suffix.lstrip(".")
        print(in_name)
        return Response(
            content=encrypted_content,
            media_type=file.content_type,
            headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")



@app.post("/decrypt/audio")
async def decrypt_audio_enpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        original_file = await file.read()
        params_obj = json.loads(params)
        decrypted_content = orchestrator.execute_request(
            system_type=system,
            system_params=params_obj,
            crypt_method=data_type,
            mode="bytes",
            content=original_file,
            process_type="decrypt",
        )
        in_name = file.filename
        file_extention=Path(in_name).suffix.lstrip(".")
        return Response(
            content=decrypted_content,
            media_type=file.content_type,
            headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")







@app.post("/encrypt/file")
async def encrypt_file_endpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        params_obj = json.loads(params)
        print(params_obj)
        content = await read_upload_chunked(file)
        in_name = file.filename
        file_extention=Path(in_name).suffix.lstrip(".")
        def chunk_iter():
            for i in range(0, len(content), 64 * 1024):
                yield content[i:i + 64 * 1024]

        return StreamingResponse(
            orchestrator.execute_request_stream(
                system_type=system,
                system_params=params_obj,
                crypt_method=data_type,
                mode="bytes",
                data_stream=chunk_iter(),
                process_type="encrypt",
            ),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")

@app.post("/decrypt/file")
async def decrypt_file_endpoint(
        system: str = Form(...),
        params: str = Form(...),
        data_type: str = Form(...),
        file: UploadFile = File(...),
):
    try:
        params_obj = json.loads(params)
        print(params_obj)
        content = await read_upload_chunked(file)
        in_name = file.filename
        file_extention=Path(in_name).suffix.lstrip(".")
        def chunk_iter():
            for i in range(0, len(content), 64 * 1024):
                yield content[i:i + 64 * 1024]

        return StreamingResponse(
            orchestrator.execute_request_stream(
                system_type=system,
                system_params=params_obj,
                crypt_method=data_type,
                mode="bytes",
                data_stream=chunk_iter(),
                process_type="decrypt",
            ),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="processed.{file_extention}"'}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутрішня помилка: {str(e)}")


app.mount("/", StaticFiles(directory=CLIENT_DIR), name="client")


