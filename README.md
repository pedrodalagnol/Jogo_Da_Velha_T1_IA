## Tic-Tac-Toe IA 
Este projeto consiste em um sistema de IA capaz de classificar estados de um tabuleiro de Jogo da Velha 3x3 em cinco categorias: Tem jogo, Possibilidade de Fim, Empate, O vence e X vence.   

## Membros do Grupo
-Danielle dos Reis Madrid 
-João Pedro Rossatti Dal Agnol
-Renato Souza


# Algoritmos usados :
Árvore de Decisão - Danielle Madrid
Random Forest - Danielle Madrid 
K-NN - João Dal Agnol
SVM - João Dal Agnol
Multi Layer Percepton - Renato Souza
    
    
# Organização do Repositório
/data: Contém o dataset balanceado e processado
/models: Modelos de IA treinados e exportados em formato .joblib.  
/notebooks: Arquivos Jupyter (.ipynb) com todo o processo de limpeza, treinamento e validação dos algoritmos.  
/src: Código do Front onde o usuário pode interagir com a IA.   

# Bibliotecas usasas
Pandas: Utilizada para a manipulação e análise estruturada do dataset, permitindo a limpeza, renomeação de colunas e mapeamento de dados.  
NumPy: Para operações matemáticas e criação de arrays multidimensionais.
Scikit-learn: Usada para implementar os algoritmos e realizar a divisão dos dados entre treino/teste e gerar as métricas de avaliação.  
Joblib: Utilizada para a serialização dos modelos de IA treinados.
Streamlit: Para o desenvolvimento do Front, criando uma interface interativa onde o usuário pode testar as predições da IA em tempo real. 
Google Colab: Tratamento do dataset e treinamento inicial dos modelos.