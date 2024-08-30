from requests import get
from json import loads

api_key = "a3869822acbcade94520c3406e65cb6f18fc0a39"


def genero(nome):
    url_base = 'https://api.brasil.io'
    nome = nome.upper().replace(" ","")

    link = f'{url_base}/v1/dataset/genero-nomes/nomes/data/?first_name={nome}'
    response = get(link, headers={"Authorization": f"Token {api_key}"})

    if response.status_code == 200:
        pass
    else:
        print('Erro')
        print(response)

    response = loads(response.content)
    print(response)  # Print da primeira parte da resposta completa, tire caso queira menos informações
  
    try:
        results = response.get('results')
        if results:
            response = results[0]
            print(response)  # Print da segunda parte da resposta completa, tire caso queira menos informações
            genero = response.get('classification')
            if genero == 'F':
                return f'F'
            elif genero == 'M':
                return f'M'
            else:
                return 'Não identificado'
        else:
            print('Nome não encontrado')
            return None
    except Exception as e:
        print(f'Erro: {e}')
