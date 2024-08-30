import logging
from typing import List

import cv2
from deepface import DeepFace
from model.fotos_agentes import FotosRequest
from utils.baixar import baixar_e_corrigir_imagem


def detectar_rostos_na_url(imagem_url: str):
    try:

        resultados = DeepFace.extract_faces(
            img_path=baixar_e_corrigir_imagem(imagem_url), detector_backend='opencv')
        num_rostos = len(resultados)
        if num_rostos == 0:
            return {"mensagem": "Foto não possui rosto", "validado": False}
        elif num_rostos > 1:
            return {"mensagem": "Foto possui mais de um rosto", "validado": False}
        else:
            return {"mensagem": "Foto possui um rosto", "validado": True}
    except Exception as e:
        logging.error(f"Erro ao detectar rosto: {e}")
        return {"mensagem": "Erro ao detectar rosto", "validado": False}


def detectar_multiplos_rosto(imagens: List[FotosRequest]):
    lista_retorno = []
    for imagem in imagens:
        try:
            resultado = detectar_rostos_na_url(imagem.url)
            lista_retorno.append({
                "idAgente": imagem.idAgente,
                "mensagem": resultado["mensagem"],
                "validado": resultado["validado"]
            })
        except Exception as e:
            logging.error(f"Erro ao processar imagem: {e}")
            lista_retorno.append({
                "idAgente": imagem.idAgente,
                "mensagem": "Erro ao processar imagem",
                "validado": False
            })
    return lista_retorno
