import spacy

# Carregar o modelo de língua portuguesa
nlp = spacy.load("pt_core_news_sm")

def gerarRespostaLogica(user_input: str) -> str:
    doc = nlp(user_input)
    
    verbos_encontrados = []
    resposta_principal = None

    for token in doc:
        #print(f"Token: {token.text}, Dep: {token.dep_}, Lemma: {token.lemma_}")  # Depuração
        
        # Identificar o verbo principal (ROOT)
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            resposta_principal = token.lemma_
        
        # Identificar outros verbos
        if token.pos_ == "VERB" and token.lemma_ not in verbos_encontrados:
            verbos_encontrados.append(token.lemma_)
    
    if not verbos_encontrados:
        return "Pode me explicar melhor?"

    # Se encontrar um verbo principal, priorize-o na resposta
    if resposta_principal:
        if resposta_principal == "ajudar":
            return "Como posso ajudar você? O que precisa ser feito?"
        elif resposta_principal == "fazer":
            return "O que você gostaria de fazer? Me diga!"
        elif resposta_principal == "falar":
            return "Sobre o que você quer conversar?"
        elif resposta_principal == "pedir":
            return "Qual é o seu pedido? Como posso ajudar?"
        elif resposta_principal == "jogar":
            return "Você quer jogar algo? Qual é o jogo?"
        elif resposta_principal == "ver":
            return "Eu não tenho olhos, mas posso verificar isso para você!"
        elif resposta_principal == "começar":
            if "desenhar" in verbos_encontrados:
                return "Você quer saber como começar a desenhar? Posso ajudar com dicas específicas!"
            return "Você quer começar algo? Me diga mais detalhes!"
        else:
            return f"Você quer {resposta_principal} algo? Me explique melhor."
    
    # Resposta genérica para múltiplos verbos sem um ROOT claro
    return f"Você mencionou as ações: {', '.join(verbos_encontrados)}. Pode me explicar mais sobre o que quer fazer?"