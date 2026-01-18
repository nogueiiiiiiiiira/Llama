from nltk.stem import RSLPStemmer
import unidecode
import xml.etree.ElementTree as ET

stemmer = RSLPStemmer()

def padronizar_string(string):
    if isinstance(string, str):
        return unidecode.unidecode(string.lower().strip())
    else:
        return str(string) if string is not None else ""

def stem_frase(frase):
    frase_str = str(frase)
    return " ".join(stemmer.stem(w) for w in frase_str.split())

def carregar_xml(caminho):
    try:
        tree = ET.parse(caminho)
        root = tree.getroot()
        return root
    except FileNotFoundError:
        print(f"\nErro: arquivo {caminho} não encontrado.")
        return None
    except Exception as e:
        print(f"\nErro ao processar {caminho}: {e}")
        return None

def extrair_achados(root):
    achados = []
    if root is None:
        return achados  
    for annotation in root.find('TAGS'):
        termo = padronizar_string(annotation.get('text'))
        categoria = annotation.get('tag')
        if termo != "":
            achados.append({"termo": termo, "categoria": categoria})
    return achados

def relacoes(root):
    relacaoDicionario = {}
    for rel in root.find('RELATIONS'):
        an1 = rel.get('annotation1') 
        an2 = rel.get('annotation2') 
        tipo = rel.get('reltype') 

        if an1 in relacaoDicionario:
            relacaoDicionario[an1].append({'id_relacionado': an2, 'tipo_relacionamento': tipo})
        else:
            relacaoDicionario[an1] = [{'id_relacionado': an2, 'tipo_relacionamento': tipo}]
    return relacaoDicionario
