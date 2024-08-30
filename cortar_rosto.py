import os
import tempfile

import cv2
from deepface import DeepFace
from utils.baixar import baixar_e_corrigir_imagem


def cortar_rosto(imagem, margem=0.8):
    resultado = DeepFace.extract_faces(
        img_path=imagem, detector_backend='detector_backend')
    if len(resultado) > 0:
        facial_area = resultado[0]['facial_area']
        x1, y1, x2, y2 = facial_area
        altura, largura = imagem.shape[:2]
        margem_x = int((x2 - x1) * margem)
        margem_y = int((y2 - y1) * margem)
        x1 = max(0, x1 - margem_x)
        y1 = max(0, y1 - margem_y)
        x2 = min(largura, x2 + margem_x)
        y2 = min(altura, y2 + margem_y)
        return imagem[y1:y2, x1:x2]


def cortar_rosto_e_salvar(url):
    imagem = baixar_e_corrigir_imagem(url)
    rosto_cortado = cortar_rosto(imagem)
    if rosto_cortado is not None:
        # Especifique o caminho correto do diretório temporário se necessário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir='/path/to/temp/dir') as temp_file:
            cv2.imwrite(temp_file.name, rosto_cortado)
            temp_file_url = "https://facial.servidor.lstranslog.log.br/" + \
                os.path.basename(temp_file.name)
            return {"url": temp_file_url}
    else:
        return {"mensagem": "Nenhum rosto detectado."}
