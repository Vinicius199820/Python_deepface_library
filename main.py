import os

from analizar_semelanca_rostos import (comparar_rostos,
                                       validar_semelhanca_rostos)
from analize_agente import analyze_image
from cortar_rosto import cortar_rosto_e_salvar
from detectar_rosto import detectar_multiplos_rosto, detectar_rostos_na_url
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.background import BackgroundTasks
from genero import genero
from model.fotos_agentes import Foto, FotosRequest
from reconhecer_cnh import reconhecer_cnh
from reconhecer_doc_veiculo import reconhecer_doc_veiculo

app = FastAPI()
router = APIRouter()


@router.post("/detectar_rosto")
async def detectar_rosto_endpoint(image_path: str):
    try:
        return detectar_rostos_na_url(image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validar_pacote_de_rostos")
async def validar_pacote_de_rostos_endpoint(request: FotosRequest):
    try:
        faces = detectar_multiplos_rosto(request.fotos)
        return faces
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/semelhanca_rostos")
async def semelhanca_rostos_endpoint(image1: str, image2: str):
    try:
        return comparar_rostos(image1, image2)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validar_pacote_de_semelhanca")
async def validar_pacote_de_semelhanca_endpoint(background_tasks: BackgroundTasks, request: FotosRequest):
    background_tasks.add_task(validar_semelhanca_rostos, request.fotos)
    url = "https://api-hub-ls.azurewebsites.net/hub/validar-rostos-iguais"
    return {"O resultado será enviado para": url}


@router.post("/reconhecer_cnh")
async def reconhecer_cnh_endpoint(image_path: str):
    try:
        return reconhecer_cnh(image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validar_pacote_de_cnhs")
async def validar_pacote_de_cnh_endpoint(request: FotosRequest):
    try:
        resultado = [{"idAgente": foto.idAgente, "validado":  reconhecer_cnh(
            foto.url)["liberar"]} for foto in request.fotos]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reconhecer_doc_veiculo")
async def reconhecer_doc_veiculo_endpoint(image_path: str):
    try:
        return reconhecer_doc_veiculo(image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validar_pacote_de_doc_veiculos")
async def validar_pacote_de_doc_veiculo_endpoint(request: FotosRequest):
    try:
        resultado = [{"idAgente": foto.idAgente, "validado":  reconhecer_doc_veiculo(
            foto.url)["liberar"]} for foto in request.fotos]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cortar_rosto")
async def cortar_rosto_endpoint(image_path: str):
    try:
        return cortar_rosto_e_salvar(image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validar_se_ja_existe_rosto")
async def validar_se_ja_existe_rosto_endpoint(image_path: Foto, Lista_imagens: FotosRequest):
    try:
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/limpar_temporarios")
async def limpar_temporarios_endpoint():
    try:
        for file in os.listdir("temp"):
            os.remove(f"temp/{file}")
        for file in os.listdir("images/compardar_rostos"):
            os.remove(f"images/compardar_rostos/{file}")

        return {"mensagem": "Temporários limpos."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validar_agente")
async def validar_agente_endpoint(image_agente: str, image_cnh: str, nome_agente: str):
    Nome_e_Foto_Sexo = False
    genero_pessoa = genero(nome_agente)
    genero_da_foto, idade_da_foto = analyze_image(image_agente)

    dados = {
        "genero_nome": genero_pessoa,
        "validar_rosto": detectar_rostos_na_url(image_agente),
        "validar_cnh": reconhecer_cnh(image_cnh),
        "semelhaca_entre_cnh_rosto": comparar_rostos(image_agente, image_cnh),
        "genero_foto": Nome_e_Foto_Sexo,
        "genero_foto_teste": genero_da_foto,
        "idade_foto_teste": idade_da_foto
    }
    return dados
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
