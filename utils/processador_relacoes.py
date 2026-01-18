import xml.etree.ElementTree as ET
from .processador_xml import padronizar_string

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

def tagDesejada(tag):
    if "Diagnostic Procedure" in tag:
        return False 

    return (
        "Sign or Symptom" in tag
        or "Disease or Syndrome" in tag
        or "Body Location or Region" in tag
    )

def dados_relacionados(dicionarioRelacao, id, root, dado):
    dadoFinal = ""
    verNegado = False

    anotacaoPrincipal = root.find(f".//annotation[@id='{id}']")
    if anotacaoPrincipal is None:
        return "", False

    tagPrincipal = anotacaoPrincipal.get('tag')

    for key, value_list in dicionarioRelacao.items():
        for value in value_list:
            if id == value['id_relacionado']:
                anotRel = root.find(f".//annotation[@id='{key}']")
                if anotRel is not None and "Diagnostic Procedure" in anotRel.get('tag'):
                    return "", False

    if "Diagnostic Procedure" in tagPrincipal:
        return "", False

    if "Negation" in tagPrincipal:
        verNegado = True

    for key, value_list in dicionarioRelacao.items():
        for value in value_list:
            if id == value['id_relacionado']:
                anotRel = root.find(f".//annotation[@id='{key}']")
                if anotRel is None:
                    continue
                tagRel = anotRel.get('tag')
                if "Diagnostic Procedure" in tagRel:
                    continue 
                if "Negation" in tagRel:
                    verNegado = True 
                if tagDesejada(tagRel) or value['tipo_relacionamento'] == 'negation_of':
                    relacao = padronizar_string(anotRel.get('text')) + " "
                    dadoFinal += relacao
                    if value['tipo_relacionamento'] == 'negation_of':
                        verNegado = True

    dadoFinal += dado
    return dadoFinal, verNegado
