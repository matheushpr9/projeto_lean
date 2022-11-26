import pandas as pd

def tratar_dados(arquivo):
    dados = pd.read_csv(arquivo, sep=';', encoding='utf8')
    dados.columns = ['CNPJ', 'Razão Social', 'Contato']
    dados['Razão Social'] = dados['Razão Social'].apply(lambda x : x.strip("'"))
    dados['Razão Social'] = dados['Razão Social'].apply(lambda x : "0"*(14-len(x)) + str(x) )
    dados['Contato'] = dados['Contato'].apply(lambda x : x.replace("\t",""))
    return(dados)

arquivo = 'projeto_lean/CNPJ_fornecedores.csv'
dados = tratar_dados(arquivo)

print(dados)