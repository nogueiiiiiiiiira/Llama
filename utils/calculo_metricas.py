import pandas as pd

def calculate_metrics(planilha):

    index = 2
    VP = FP = FN = VPP = 0

    while planilha[f'A{index}'].value or planilha[f'G{index}'].value:
        classificacao = planilha[f'J{index}'].value
        if classificacao == 'VP':
            VP += 1
        elif classificacao == 'FP':
            FP += 1
        elif classificacao == 'FN':
            FN += 1
        elif classificacao == 'VPP':
            VPP += 1
        index += 1

    precisao = (VP + VPP) / (VP + VPP + FP) if (VP + VPP + FP) > 0 else 0
    recall = (VP + VPP) / (VP + VPP + FN) if (VP + VPP + FN) > 0 else 0
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0

    metricas = {
        "VP": [VP], "FP": [FP], "FN": [FN], "VPP": [VPP],
        "precisao": [precisao], "Recall": [recall], "F1-Score": [f1]
    }
    df_metricas = pd.DataFrame(metricas)

    index = 2
    resultados = [0, 0, 0]

    while planilha[f'A{index}'].value or planilha[f'G{index}'].value:
        classificacao = planilha[f'K{index}'].value
        try:
            numero = int(classificacao)
            resultados[numero] += 1
        except:
            pass
        index += 1

    contagem = {
        "Códigos SNOMED CT NÃO ENCONTRADOS": [resultados[0]],
        "Códigos EXISTEM mas NÃO CORRESPONDEM": [resultados[1]],
        "Códigos EXISTEM e CORRESPONDEM": [resultados[2]],
        "\nTotal de códigos verificados": [sum(resultados)]
    }

    df_contagem = pd.DataFrame(contagem)

    return df_metricas, df_contagem

def print_metrics_table(df_metricas):

    print("\nRESULTADOS DA EXTRAÇÃO DE TERMOS CLÍNICOS\n")
    print(df_metricas.to_string(index=False))

def print_snomed_table(df_contagem):
    print("\nRESULTADOS DO MAPEAMENTO SNOMED CT\n")
    for col in df_contagem.columns:
        print(f"{col}: {df_contagem[col].iloc[0]}")
