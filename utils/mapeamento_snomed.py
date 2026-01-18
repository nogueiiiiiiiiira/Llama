from utils.processador_llama import PesquisaClin_Llama

def prompt_avmap(codigo, termo, llm):
    """
    Verifica se um código SNOMED CT corresponde a um termo clínico.
    Retorna:
        0 - Código não encontrado
        1 - Código existe mas não corresponde
        2 - Código existe e corresponde
    """
    prompt = f"""
Dado um termo clínico em português e um código SNOMED CT (SCTID), determine a validade do código em relação ao termo.

Responda apenas com um dos seguintes números:
0 – O código SNOMED CT fornecido NÃO existe (nenhum resultado retornado);
1 – O código existe, mas NÃO corresponde ao termo fornecido;
2 – O código existe E corresponde corretamente ao termo fornecido.

### Dados fornecidos:
Código SNOMED CT: {codigo}
Termo em português: {termo}

### Instruções:
- Acesse o navegador SNOMED CT pelo seguinte link:
https://termbrowser.nhs.uk/?perspective=full&conceptId1={codigo}&edition=uk-edition&release=v20250604&server=https://termbrowser.nhs.uk/sct-browser-api/snomed&langRefset=999001261000000100,999000691000001104
- Verifique se o código retorna algum conceito (caso contrário, é 0).
- Caso retorne um conceito, traduza o termo principal para o português e compare com o termo fornecido.
- A comparação deve considerar correspondência clínica ou semântica (tradução precisa e direta).
- Responda somente com o número correspondente: 0, 1 ou 2. Nenhuma explicação adicional.
"""
    resposta = PesquisaClin_Llama(prompt, llm)
    for char in resposta:
        if char in "012":
            return int(char)
    return 0

def map_snomed(planilha, llm):
    """
    Realiza mapeamento SNOMED CT para termos no arquivo Excel.

    Args:
        planilha: Objeto de planilha Excel contendo os resultados
        llm: Instância do modelo LLaMA para gerar mapeamentos

    Esta função itera através de cada linha no arquivo Excel, verifica se um código SNOMED CT existe,
    e usa o modelo LLaMA para determinar se o termo corresponde ao conceito SNOMED.
    """
    def termo_abreviacao(termo, abreviacao):
        """Combina termo e abreviação para exibição."""
        return f'{termo} ({abreviacao})'

    try:
        index = 2
        while planilha[f'A{index}'].value or planilha[f'G{index}'].value:
            termo_analisado = planilha[f'D{index}'].value
            sctid_valor = planilha[f'F{index}'].value

            if sctid_valor and sctid_valor != 'NotFound':
                try:
                    SCTID = int(sctid_valor)
                    abreviacao = planilha[f'E{index}'].value
                    termo = termo_abreviacao(termo_analisado, abreviacao) if abreviacao else termo_analisado

                    resposta = prompt_avmap(SCTID, termo, llm)
                    planilha[f'K{index}'] = resposta
                except ValueError as ve:
                    print(f"\nValueError processando linha {index}: {ve}")
                    planilha[f'K{index}'] = 'Error'
                except Exception as e:
                    print(f"\nErro processando mapeamento SNOMED para linha {index}: {e}")
                    planilha[f'K{index}'] = 'Error'

            index += 1
    except Exception as e:
        print(f"\nErro crítico durante mapeamento SNOMED: {e}")
        raise
