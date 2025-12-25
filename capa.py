import pandas as pd
import requests
import os
import re
from dotenv import load_dotenv
import base64

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações da API do Spotify vindas do .env
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTH_URL = 'https://accounts.spotify.com/api/token'
SEARCH_URL = 'https://api.spotify.com/v1/search'

# Função para limpar caracteres inválidos para nome de arquivo (ex: : / \ ? *)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Função para obter o token de acesso
def get_access_token():
    # Autenticação Client Credentials Flow
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    
    if auth_response.status_code != 200:
        raise Exception(f"Falha na autenticação: {auth_response.status_code} - {auth_response.text}")
        
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Função para buscar informações do álbum
def search_album(access_token, query):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # type=album e limit=1 para pegar o primeiro resultado
    params = {
        'q': query,
        'type': 'album',
        'limit': 1
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    return response.json()

# Função para baixar a capa
def download_album_cover(image_url, file_name, save_path):
    img_data = requests.get(image_url).content
    
    # Garante que o diretório existe
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    full_path = os.path.join(save_path, f'{file_name}.jpg')
    
    with open(full_path, 'wb') as handler:
        handler.write(img_data)

def main():
    # Caminhos
    save_path = r'C:/Users/Malvo/Desktop/Albuns2025'
    excel_path = r'C:/Users/Malvo/Desktop/Musgas.xlsx' # Se for CSV, mude a extensão aqui

    try:
        # Tenta ler como Excel, se falhar, avisa
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Erro ao ler arquivo. Se for um CSV, mude pd.read_excel para pd.read_csv. Erro: {e}")
        return

    try:
        access_token = get_access_token()
    except Exception as e:
        print(e)
        return
    
    # Iterar sobre as linhas
    for index, row in df.iterrows():
        # Verificação se as colunas existem (baseado no seu arquivo enviado)
        if 'ARTISTA' not in row or 'ALBUM' not in row:
            print("Colunas 'ARTISTA' ou 'ALBUM' não encontradas na planilha.")
            break
            
        artist = str(row['ARTISTA']).strip()
        album_name = str(row['ALBUM']).strip()
        
        # Pula linhas vazias
        if artist == 'nan' or album_name == 'nan' or not artist:
            continue

        # Termo de busca: "Artista Album"
        search_query = f"{artist} {album_name}"
        
        # Busca na API
        data = search_album(access_token, search_query)
        
        if 'albums' in data and data['albums']['items']:
            album_info = data['albums']['items'][0]
            if album_info['images']:
                image_url = album_info['images'][0]['url']
                
                # Cria o nome do arquivo: "Artista Album"
                raw_filename = f"{artist} {album_name}"
                # Remove caracteres proibidos do Windows
                safe_filename = sanitize_filename(raw_filename)
                
                download_album_cover(image_url, safe_filename, save_path)
                print(f'[OK] Baixado: {safe_filename}')
            else:
                print(f'[X] Imagem não encontrada para: {search_query}')
        else:
            print(f'[X] Álbum não encontrado no Spotify: {search_query}')

if __name__ == '__main__':
    main()