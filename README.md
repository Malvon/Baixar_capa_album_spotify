# Baixar capa de albuns do Spotify

**Descrição do Projeto:**  
Anualmente, realizo uma curadoria dos lançamentos musicais dos artistas que acompanho, classificando os álbuns em uma escala de até 5 estrelas. Ao final do ano, utilizo essa base para divulgar os destaques (avaliações 4 e 5 estrelas) em minhas redes sociais. Este script automatiza o download das capas desses álbuns diretamente da API do Spotify.

### 📋 Pré-requisitos
1. Bibliotecas  
Certifique-se de ter o Python instalado e instale as dependências necessárias:

pip install pandas requests python-dotenv openpyxl

2. Planilha de Dados  
É necessário um arquivo Excel (.xlsx ou .csv) contendo, no mínimo, as colunas 'ARTISTA' e 'ALBUM'

3. Credenciais do Spotify  
Crie um arquivo chamado .env na mesma pasta do script capa.py. Ele deve conter suas credenciais (sem aspas e sem espaços):  
CLIENT_ID='XXXXXXXXXX'  
CLIENT_SECRET='XXXXXXXXXX'  
Obs: As chaves podem ser obtidas gratuitamente no Spotify for Developers.

### ⚙️ Configuração no Código  
Abra o arquivo capa.py e edite as variáveis de caminho conforme o seu computador:  

save_path: O diretório onde as imagens serão salvas.  
excel_path: O caminho onde está sua planilha.

Este projeto foi desenvolvido com auxílio de Inteligência Artificial.
