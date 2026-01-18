from comando_llama.prompt import PROMPT_TEMPLATE 

def dividir_texto_por_prompt_seguro(texto, llm, prompt_template, max_tokens_saida=256):
    
    n_ctx = llm.n_ctx()
    tokens = llm.tokenize(texto.encode())
    blocos = []
    inicio = 0

    while inicio < len(tokens):
        fim = len(tokens)
        while fim > inicio:
            bloco_tokens = tokens[inicio:fim]
            bloco_texto = llm.detokenize(bloco_tokens).decode('utf-8', errors='ignore')
            prompt = prompt_template.format(textoClinico=bloco_texto)
            total_tokens = len(llm.tokenize(prompt.encode())) + max_tokens_saida
            if total_tokens <= n_ctx:
                blocos.append(bloco_texto) 
                inicio = fim
                break
            fim -= 50
        else:

            corte = (n_ctx - max_tokens_saida) // 2
            bloco_tokens = tokens[inicio:inicio + corte]
            bloco_texto = llm.detokenize(bloco_tokens).decode("utf-8", errors="ignore")
            blocos.append(bloco_texto)
            inicio += len(bloco_tokens)

    return blocos

def PesquisaClin_Llama(textoClinico, llm, temperature=0.7):
    
    prompt = PROMPT_TEMPLATE.format(textoClinico=textoClinico)
    try:
        print(f"\nProcessando narrativa completa ({len(llm.tokenize(prompt.encode()))} tokens incluindo prompt)...\n")
        result = llm(prompt=prompt, max_tokens=4096, temperature=temperature)
        return result["choices"][0]["text"].strip()
    except Exception as e:
        print(f"\nErro na chamada LLaMA: {e}")
        return f"Erro na chamada LLaMA: {e}"
