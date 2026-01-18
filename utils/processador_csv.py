import pandas as pd
import re
import os
from typing import Optional, List

def encontrar_linha_final_anotacao(lines: List[str]) -> int:
    last_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if ']' in lines[i] and '[' in lines[i] and 'Texto analisado:' in lines[i]:
            last_index = i
            break
    return last_index

def criar_dataframe_e_exportar_csv(input_text: str, csv_filename: str, narrative_name: str) -> Optional[pd.DataFrame]:
    
    if not input_text or not input_text.strip():
        print("\nErro: O texto de entrada está vazio ou contém apenas espaços.")
        return None

    try:
        linhas = input_text.strip().split('\n') 
        texto_narrativa = ""
        linhas_listas_raw = []
        indice_fim_narrativa = encontrar_linha_final_anotacao(linhas)

        if indice_fim_narrativa != -1:
            texto_narrativa = "\n".join(linhas[:indice_fim_narrativa + 1]).strip()
            linhas_listas_raw = linhas[indice_fim_narrativa + 1:]
        else:
            print("\nAviso: Nenhuma anotação [...] encontrada no texto. Tentando processar linhas como listas.")
            texto_narrativa = ""
            linhas_listas_raw = linhas

        while linhas_listas_raw and not linhas_listas_raw[0].strip():
            linhas_listas_raw.pop(0)

    except Exception as e:
        print(f"\nErro ao separar texto e listas: {e}")
        return None

    dados_extraidos = []
    regex_tupla_interna_4 = re.compile(r'\[\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\]') 

    for linha_lista in linhas_listas_raw:
        linha_strip = linha_lista.strip()

        matches_internos = regex_tupla_interna_4.findall(linha_strip)
        print(matches_internos)

        for match_tuple in matches_internos:
            try:
                if len(match_tuple) == 4:
                    texto_analisado = match_tuple[0].strip()
                    abreviacao = match_tuple[1].strip()
                    categoria = match_tuple[2].strip()
                    sctid = match_tuple[3].strip()
                else:
                    print(f"\nAviso: Ignorando item com número incorreto de campos: '{match_tuple}'")
                    continue

                dados_extraidos.append({
                    "nomeNarrativa": narrative_name,
                    "textoPrompt": texto_narrativa,
                    "categoria": categoria,
                    "textoAnalisado": texto_analisado,
                    "abreviacao": abreviacao if abreviacao.lower() != 'none' else None,
                    "SCTID": sctid if sctid.lower() != 'notfound' else None
                })
            except IndexError as e:
                print(f"\nErro de índice ao processar item da tupla: '{match_tuple}'. Erro: {e}")
            except Exception as e:
                print(f"\nErro inesperado ao processar item '{match_tuple}': {e}")

    if not dados_extraidos:
        print(f"\nAviso: Nenhum item [...] válido foi extraído das linhas de lista para a narrativa '{narrative_name}'. Nenhum CSV será gerado.")
        return None
    try:
        df = pd.DataFrame(dados_extraidos)
        df = df[["nomeNarrativa", "textoPrompt", "categoria", "textoAnalisado", "abreviacao", "SCTID"]]
    except Exception as e:
        print(f"\nErro ao criar o DataFrame para '{narrative_name}': {e}")
        return None

    try:
        output_dir = os.path.dirname(csv_filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        df.to_csv(csv_filename, index=False, encoding='utf-8', sep=',')
        print(f"\nDataFrame exportado com sucesso para '{csv_filename}'")
        return df
    except Exception as e:
        print(f"\nErro ao exportar o DataFrame para CSV '{csv_filename}': {e}")
        return None
