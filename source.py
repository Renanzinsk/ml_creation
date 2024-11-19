import json
#from difflib import get_close_matches
from typing import List, Dict, Union
import speech_recognition as sr
from tts import textToSpeech
from rapidfuzz import process
from gerarRespostaLogica import gerarRespostaLogica

def exeAction(act: str):
    """Executa uma ação específica baseada no comando fornecido."""
    if act == "ligar_lampada":
        print("Executando: Ligando a lâmpada.")
    elif act == "desligar_lampada":
        print("Executando: Desligando a lâmpada.")
    else:
        print("Ação não reconhecida.")

def carregarConhecimento(file_path: str) -> Dict:
    """Carrega o conhecimento de um arquivo JSON."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def salvarConhecimento(file_path: str, data: Dict) -> None:
    """Salva o conhecimento em um arquivo JSON."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def melhorResposta(user_question: str, questions: List[str]) -> Union[str, None]:
    result = process.extractOne(user_question, questions)
    if result:
        best_match, score, _ = result
        return best_match if score > 90 else None
    return None

def pegaRespostas(question: str, baseConhecimento: Dict) -> Union[str, None]:
    """Obtém a resposta para a pergunta fornecida da base de conhecimento."""
    for q in baseConhecimento["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_with_bot():
    """Interage com o usuário em um chat, utilizando a base de conhecimento."""
    baseConhecimento = carregarConhecimento("database.json")
    
    print("Digite 'sair' para encerrar a conversa.")
    while True:
        #recognizer = sr.Recognizer()
        #with sr.Microphone() as source:
            #print("Fale algo...")
            #audio = recognizer.listen(source)
            #try:
                #texto = recognizer.recognize_google(audio, language="pt-BR")
                #print("Você disse:", texto)
            #except sr.UnknownValueError:
                #print("Não consegui entender.")
            #except sr.RequestError:
                #print("Erro ao conectar com o serviço.")

        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            break
        
        best_match = melhorResposta(user_input, [q["question"] for q in baseConhecimento["questions"]])
        if best_match:
            resposta = next(q for q in baseConhecimento["questions"] if q["question"] == best_match)
            print(f"Bot: {resposta['answer']}")
            textToSpeech(resposta["answer"])
            if "action" in resposta:
                exeAction(resposta["action"])

        else:
            #print("Bot: Não sei a resposta. Você pode me ensinar?")
            #new_answer = input('Digite a resposta ou "pular" para pular: ')
            #if new_answer.lower() != "pular":
                #baseConhecimento["questions"].append({"question": user_input, "answer": new_answer})
                #salvarConhecimento("database.json", baseConhecimento)
                #print("Bot: Obrigado! Aprendi uma nova resposta!")

            resposta_logica = gerarRespostaLogica(user_input)
            print(f"Bot: {resposta_logica}")
            if resposta_logica.lower() != "Pode me explicar melhor?":
                second_input = input("Insira a informacao que falta: ")
                baseConhecimento["questions"].append({"question": user_input, "answer": second_input})
                salvarConhecimento("database.json", baseConhecimento)
            else:
                explicacao = input("Insira a informacao que falta: ")
                if explicacao.strip().lower() != "pular":
                    print("Bot: Obrigado! Agora aprendi algo novo.")
                    baseConhecimento["questions"].append({"question": user_input, "answer": explicacao})
                salvarConhecimento("database.json", baseConhecimento)

if __name__ == "__main__":
    chat_with_bot()