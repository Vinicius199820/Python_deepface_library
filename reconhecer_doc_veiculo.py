import os

import numpy as np
import tensorflow as tf
from PIL import Image
from utils.baixar import baixar_e_corrigir_imagem

model_path = "./code/model/model_doc.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def classify_image(image, interpreter, input_details, output_details):
    image = Image.fromarray(image)
    image = image.resize((224, 224))
    input_image = np.expand_dims(np.array(image, dtype=np.float32), axis=0)
    input_image = input_image / 255.0
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_label = int(np.argmax(output_data))
    return predicted_label


def reconhecer_doc_veiculo(imagem_url):
    imagem = baixar_e_corrigir_imagem(imagem_url)
    try:
        resultado = classify_image(
            imagem, interpreter, input_details, output_details)
        return {"liberar": resultado == 0}
    except Exception as e:
        return {"liberar": False}
