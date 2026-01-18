from .processador_xml import stem_frase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def medir_similaridade(t1, t2):

    doc1 = stem_frase(t1)
    doc2 = stem_frase(t2)

    vetorizador_radical = TfidfVectorizer()
    try:
        matriz_radical = vetorizador_radical.fit_transform([doc1, doc2])

        resultado_radical = cosine_similarity(matriz_radical[0:1], matriz_radical[1:2])[0][0]
    except ValueError:
        resultado_radical = 0.0 

    vetorizador = TfidfVectorizer()
    try:
        tfidf_matrix = vetorizador.fit_transform([t1, t2])
        resultado = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except ValueError:
        resultado = 0.0 

    return max(resultado_radical, resultado)
