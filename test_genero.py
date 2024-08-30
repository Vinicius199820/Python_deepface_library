import unittest
from unittest.mock import patch
from genero import genero_agente

class GeneroAgenteTests(unittest.TestCase):

    @patch('builtins.print')
    def test_genero_agente_feminino(self, mock_print):
        api_key = 'your_api_key'
        nome = 'Maria'
        expected_output = 'Maria é um nome Feminino'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b'{"results": [{"classification": "F"}]}'

            result = genero_agente(api_key, nome)

            mock_get.assert_called_once_with('https://api.brasil.io/v1/dataset/genero-nomes/nomes/data/?first_name=MARIA', headers={"Authorization": "Token your_api_key"})
            mock_print.assert_called_once_with('{"results": [{"classification": "F"}]}')
            self.assertEqual(result, expected_output)

    @patch('builtins.print')
    def test_genero_agente_masculino(self, mock_print):
        api_key = 'your_api_key'
        nome = 'João'
        expected_output = 'João é um nome Masculino'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b'{"results": [{"classification": "M"}]}'

            result = genero_agente(api_key, nome)

            mock_get.assert_called_once_with('https://api.brasil.io/v1/dataset/genero-nomes/nomes/data/?first_name=JOÃO', headers={"Authorization": "Token your_api_key"})
            mock_print.assert_called_once_with('{"results": [{"classification": "M"}]}')
            self.assertEqual(result, expected_output)

    @patch('builtins.print')
    def test_genero_agente_nao_identificado(self, mock_print):
        api_key = 'your_api_key'
        nome = 'Alex'
        expected_output = 'Não identificado'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b'{"results": []}'

            result = genero_agente(api_key, nome)

            mock_get.assert_called_once_with('https://api.brasil.io/v1/dataset/genero-nomes/nomes/data/?first_name=ALEX', headers={"Authorization": "Token your_api_key"})
            mock_print.assert_called_once_with('Nome não encontrado')
            self.assertEqual(result, expected_output)

    @patch('builtins.print')
    def test_genero_agente_erro(self, mock_print):
        api_key = 'your_api_key'
        nome = 'John'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 500

            result = genero_agente(api_key, nome)

            mock_get.assert_called_once_with('https://api.brasil.io/v1/dataset/genero-nomes/nomes/data/?first_name=JOHN', headers={"Authorization": "Token your_api_key"})
            mock_print.assert_called_once_with('Erro')
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()