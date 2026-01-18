import openpyxl
import os

def carregar_excel(caminho, sheet='Resultados'):
    wb = openpyxl.load_workbook(caminho)
    ws = wb[sheet] 
    return wb, ws

def salvar_excel(wb, caminho):
    wb.save(caminho) 


