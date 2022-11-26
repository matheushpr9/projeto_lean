from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd

def tratar_dados(arquivo):
    dados = pd.read_csv(arquivo, sep=';', encoding='utf8')
    dados.columns = ['CNPJ', 'Razão Social', 'Contato']
    dados['CNPJ'] = dados['CNPJ'].apply(lambda x : x.strip("'"))
    dados['CNPJ'] = dados['CNPJ'].apply(lambda x : "0"*(14-len(x)) + str(x) )
    dados['Contato'] = dados['Contato'].apply(lambda x : x.replace("\t",""))
    dados['Razão Social'] = dados['Razão Social'].apply(lambda x : x.replace(" ",""))
    dados['Razão Social'] = dados['Razão Social'].apply(lambda x : x.replace(".",""))
    dados['Razão Social'] = dados['Razão Social'].apply(lambda x : x.replace("/",""))
    return(dados)

def acharCnpj (nomeFornecedor, plan,lista):
    try:
        linha= plan[plan["Razão Social"] == nomeFornecedor]["CNPJ"]
        return plan["Contato"][(linha.index)[0]]
    except:
        if nomeFornecedor not in lista:
            lista.append(nomeFornecedor)
        return "Nome não encontrado na base"



arquivo = 'projeto_lean/CNPJ_fornecedores.csv'
dadosForncedores = tratar_dados(arquivo)


print(dadosForncedores)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1xyITceuvLlv71iCfSEwCXeL2M4me0KIo4gWcHIvmNtY'


creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            r'/projeto_lean/token.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())



service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()






intervalo_plan_qua = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range='Falta & Sobra!A2:AE').execute()
Planilha_FeS = intervalo_plan_qua.get('values', [])

#Cria o dataframe
dados_plan_FeS = pd.DataFrame(Planilha_FeS, columns = ['STATUS',
                                                       'CONTROLE',
                                                       'DATA DE COLETA',
                                                       'COLABORADOR DEVOLUÇÃO',
                                                       'DATA NOTIFICAÇÃO',
                                                       'DATA DA TRIAGEM',
                                                       'DATA AUTORIZAÇÃO',
                                                       'JIRA',
                                                       'COLABORADOR BK',
                                                       'NFO',
                                                       'Fornecedor',
                                                       'MATERIAL',
                                                       'OCORRÊNCIA',
                                                       'QTD',
                                                       'CNPJ Transp',
                                                       'Nome Transportadora',
                                                       'QTDE SOBRA',
                                                       'Nº MIGO',
                                                       'SM',
                                                       'MIRO',
                                                       'DADOS ADICIONAIS',
                                                       'DATA NFD',
                                                       'NFD',
                                                       'RESPONSÁVEL',
                                                       'Cod_INTERNO',
                                                       'Z',
                                                       'Vol',
                                                       'POSIÇÕES',
                                                       'AC',
                                                       'REF JIRA',
                                                       'ref cod'])


sem_contatoFeS = dados_plan_FeS[dados_plan_FeS['STATUS'] == "SEM CONTATO"]
sem_contatoFeS.index = range(len(sem_contatoFeS.index))

nomesSemregistro = []

df_novo = pd.DataFrame()

df_novo['Fornecedor'] = sem_contatoFeS['Fornecedor']
df_novo['Fornecedor'] = df_novo['Fornecedor'].apply(lambda x : x.replace(" ",""),)
df_novo['Fornecedor'] = df_novo['Fornecedor'].apply(lambda x : x.replace(".",""))
df_novo['Fornecedor'] = df_novo['Fornecedor'].apply(lambda x : x.replace("/",""))
df_novo['NFO'] = sem_contatoFeS['NFO']
df_novo['MATERIAL'] = sem_contatoFeS['MATERIAL']
df_novo['OCORRÊNCIA'] = sem_contatoFeS['OCORRÊNCIA']
df_novo['QTD'] = sem_contatoFeS['QTD']
df_novo['email'] = df_novo['Fornecedor'].apply(lambda x: acharCnpj ( x, dadosForncedores,nomesSemregistro))
print(df_novo)

if len(nomesSemregistro)>0:
    print(nomesSemregistro)

print((df_novo.groupby('NFO')).groups)

for nf, itens in df_novo.groupby('NFO'):
    print('{} - > {}'.format(nf, itens))