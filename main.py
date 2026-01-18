import pandas as pd
import os
import openpyxl
import time
import logging
from llama_cpp import Llama
from utils.processador_narrativa import processar_narrativas, criar_csv_mestre, comparar_com_goldstandard
from utils.analise_similaridade import analyze_similarities
from utils.mapeamento_snomed import map_snomed
from utils.calculo_metricas import calculate_metrics, print_metrics_table, print_snomed_table
PASTA_NARRATIVAS = 'narrativas'
CSV_OUTPUT_FOLDER = 'data/csv_output'
RESULTADOS_EXCEL = 'data/Resultados.xlsx'

def main():
    try:
        print('\nIniciando pipeline de extração de termos clínicos...\n')
        inicio = time.time()
        try:
            llm = Llama(model_path='modelo/Llama-3.2-3B-Instruct-Q4_K_M.gguf', n_ctx=8192, n_threads=8, n_gpu_layers=20, verbose=False)
        except Exception as e:
            print(f'\nErro ao inicializar modelo LLaMA: {e}')
            print('\nCertifique-se de que o arquivo do modelo existe e está acessível.')
            return
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nProcessando narrativas XML...')
            lista_dataframes_individuais = processar_narrativas(PASTA_NARRATIVAS, CSV_OUTPUT_FOLDER, llm, temperature=0.0)
        except Exception as e:
            print(f'\nErro ao processar narrativas: {e}')
            return
        try:
            csv_mestre = criar_csv_mestre(lista_dataframes_individuais, CSV_OUTPUT_FOLDER)
            if not csv_mestre:
                print('\nFalha ao criar CSV mestre')
                return
        except Exception as e:
            print(f'\nErro ao criar CSV mestre: {e}')
            return
        try:
            df_resultado = comparar_com_goldstandard(csv_mestre, PASTA_NARRATIVAS, RESULTADOS_EXCEL)
        except Exception as e:
            print(f'\nErro durante comparação com gold standard: {e}')
            return
        try:
            workbook = openpyxl.load_workbook(RESULTADOS_EXCEL)
            planilha = workbook['Resultados']
        except Exception as e:
            print(f'\nErro ao carregar workbook Excel: {e}')
            return
        limiar_similaridade = 0.7
        try:
            analyze_similarities(planilha, limiar_similaridade)
        except Exception as e:
            print(f'\nErro durante análise de similaridade: {e}')
            return
        try:
            workbook.save(RESULTADOS_EXCEL)
        except Exception as e:
            return
        try:
            map_snomed(planilha, llm)
        except Exception as e:
            print(f'\nErro durante mapeamento SNOMED CT: {e}')
            return
        try:
            workbook.save(RESULTADOS_EXCEL)
        except Exception as e:
            print(f'\nErro ao salvar resultados finais: {e}')
            return
        try:
            df_metricas, df_contagem = calculate_metrics(planilha)
            print_metrics_table(df_metricas)
            print_snomed_table(df_contagem)
            fim = time.time()
            tempo_total = fim - inicio
            print(f'\nTEMPO TOTAL DE EXECUÇÃO: {tempo_total:.2f} segundos\n')
            print('\nPipeline concluído com sucesso!')
        except Exception as e:
            print(f'\nErro ao calcular ou exibir métricas: {e}')
            return
    except Exception as e:
        print(f'\nErro crítico na execução principal: {e}')
        return
if __name__ == '__main__':
    main()