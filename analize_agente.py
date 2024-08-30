from deepface import DeepFace


#value = DeepFace.analyze('C:/lsProject/ls.deteccao.facial/code/vini.jpg', detector_backend='opencv', enforce_detection=True)
#print(value)

def analyze_image(image_path):
    try:
        results = DeepFace.analyze(image_path, detector_backend='opencv', enforce_detection=True)
        if len(results) > 0:
            return results[0]['dominant_gender'], results[0]['age']
        else:
            return "Nenhum resultado encontrado"
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"
    
results = analyze_image('C:/lsProject/ls.deteccao.facial/code/maria.png')
print(results)