import os
import re

import requests
from deepface import DeepFace
from utils.baixar import (baixar_corrigir_e_salvar_imagem,
                          baixar_e_corrigir_imagem)


def comparar_rostos(imagem_url1, imagem_url2):
    imagem1 = baixar_e_corrigir_imagem(imagem_url1)
    imagem2 = baixar_e_corrigir_imagem(imagem_url2)
    try:
        result = DeepFace.verify(
            imagem1, imagem2, model_name="Facenet", distance_metric="euclidean")
        porcentagem = (1 - result["distance"]) * 100
        return {"status": result["verified"],  "porcentagem": porcentagem}
    except Exception as e:
        return {"status": False, "error": str(e)}


path = "./images/compardar_rostos/"


def validar_semelhanca_rostos(lista_imagens):
    baixar_corrigir_e_salvar_imagem(lista_imagens, path)
    lista_de_imagens = os.listdir(path)
    agentes_agrupados = []

    for imagem_nome in lista_de_imagens:
        if imagem_nome.endswith(".pkl"):
            continue
        agente_id = int(imagem_nome.split(".")[0])
        img_path = os.path.join(path, imagem_nome)
        try:
            try:
                matches = DeepFace.find(
                    img_path=img_path, db_path=path, model_name="GhostFaceNet", distance_metric="euclidean")
                agentes_semelhantes = []
                for df in matches:
                    img_paths = df["identity"].values.tolist()
                    for matched_img_path in img_paths:
                        agente_id2 = int(os.path.basename(
                            matched_img_path).split(".")[0])
                        if agente_id2 != agente_id:
                            agentes_semelhantes.append(agente_id2)

                agentes_agrupados.append({
                    "agente_id": agente_id,
                    "agentes_semelhantes": agentes_semelhantes
                })
            except Exception as e:
                print(f"Erro ao processar a imagem {imagem_nome}: {e}")

        except Exception as e:
            print(f"Erro ao processar a imagem {imagem_nome}: {e}")

    if agentes_semelhantes:
        enviar_post(agentes_semelhantes)


def enviar_post(json):
    print('Enviando post')
    requests.post(
        'https://api-hub-ls.azurewebsites.net/hub/validar-rostos-iguais', json=json)
