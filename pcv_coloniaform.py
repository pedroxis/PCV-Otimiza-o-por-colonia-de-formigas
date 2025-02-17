import random

class VariaveisGlobais:
    def __init__(self):
        self.matriz_distancias = []
        self.matriz_feromonio = []
        self.num_vertices = 0
        self.num_formigas = 0
        self.caminho_formiga = []
        self.alfa = 1
        self.beta = 5
        self.p = 0.5
        self.q = 100
        self.t0 = 1e-16
        self.melhor_caminho_global = []
        self.melhor_fitness_global = float('inf')
        
class Formiga:
    def __init__(self, num_vertices):  # era: (self,numvertices,alfa,beta) - modificado 21:35
        self.caminho = []  # lista para armazenar o caminho da formiga
        self.fitness = 0  # distancia percorrida 'Lk' (inicializada com 0) seria o custo do caminho
        self.posicao_atual = None  # posicao em que a formiga esta
        self.num_vertices = num_vertices        

def ler_matriz_distancia(arquivo, variaveis):
    with open(arquivo, 'r') as file:
        lines = file.readlines()
        for linha in lines:
            if linha.startswith('#'):
                continue  # Ignorar comentários no arquivo
            variaveis.matriz_distancias.append(list(map(int, linha.split())))
        
        variaveis.num_vertices = len(variaveis.matriz_distancias)  # Número de vertices (tamanho da matriz)
        
def inicializar_feromonios(variaveis):
    variaveis.matriz_feromonio = [[variaveis.t0 for _ in range(variaveis.num_vertices)] for _ in range(variaveis.num_vertices)]
    #ATUALIZA TODA A MATRIZ DE FEROMONIOS COM 10^-16
    
def inicializar_formigas(variaveis):
    for i in range(variaveis.num_formigas):
        caminho = list(range(variaveis.num_vertices)) # cria uma lista de vertices
        random.shuffle(caminho) # aleatoriza o caminho de vertices 
        variaveis.caminho_formiga.append(caminho) #atualiza a matriz de caminho da formiga com o caminho aleatorio

def escolher_proxima_cidade(formiga,variaveis):
    probabilidades = []
    soma_probabilidades = 0
    for j in range(variaveis.num_vertices):
        if j not in formiga.caminho:
            visibilidade_ij = 1 / variaveis.matriz_distancias[formiga.posicao_atual][j]
            feromonio_ij = variaveis.matriz_feromonio[formiga.posicao_atual][j]
            probabilidade_ij = (feromonio_ij**variaveis.alfa) * ( visibilidade_ij**variaveis.beta) 
            # equacao descrita para calculo da probabilidade de acordo com α e β (EQUAÇÃO 2 DO SLIDE)
            
            probabilidades.append(probabilidade_ij) #atualiza a lista de probabilidades
            soma_probabilidades += probabilidade_ij
            
        else:
            probabilidades.append(0) # se a cidade ja foi visitada entao nao podemos ir a ela.
            
    # Normaliza as probabilidades (soma = 1)
    probabilidades = [p / soma_probabilidades for p in probabilidades]
    
    # A formiga escolhe uma cidade com base nas probabilidades
    cidade_escolhida = random.choices(range(variaveis.num_vertices), probabilidades)[0]
    return cidade_escolhida

def atualizar_feromonios(variaveis, formigas):
    # evaporar feromonio
    for i in range(variaveis.num_vertices):
        for j in range(variaveis.num_vertices):
            variaveis.matriz_feromonio[i][j] *= (1 - variaveis.p)  # Evaporação usando variaveis.p
    
    # depositar feromônio 
    for formiga in formigas:
        for i in range(len(formiga.caminho)-1):
            vertice_atual = formiga.caminho[i]
            vertice_proximo = formiga.caminho[i+1]
            variaveis.matriz_feromonio[vertice_atual][vertice_proximo] += (variaveis.q / formiga.fitness)
            variaveis.matriz_feromonio[vertice_proximo][vertice_atual] += (variaveis.q / formiga.fitness)                 

def movimento_formiga(variaveis, formiga):
    formiga.posicao_atual = random.randint(0, variaveis.num_vertices - 1) #escolhe uma cidade aleatoria entre as
                                                                         #as vertices disponiveis
    formiga.caminho = [formiga.posicao_atual] #começa o caminho com o 'vertice' atual
    
    while len(formiga.caminho) < variaveis.num_vertices:
        proxima_cidade = escolher_proxima_cidade(formiga, variaveis) # escolhe a proxima cidade
        formiga.caminho.append(proxima_cidade) # coloca a proxima cidade escolhida no caminho escolhido
        formiga.posicao_atual = proxima_cidade # atualiza a posicao atual da formiga para a cidade escolhida
        
def calcular_fitness(formiga, variaveis):  # calcular o custo do caminho da formiga.
    distancia = 0
    for i in range(len(formiga.caminho) - 1):
        cidade_atual = formiga.caminho[i]
        cidade_proxima = formiga.caminho[i + 1]
        distancia += variaveis.matriz_distancias[cidade_atual][cidade_proxima]
    return distancia


    
            
        
def main():
    arquivo = 'sgb128_dist.txt'
    variaveis = VariaveisGlobais()
    
    ler_matriz_distancia(arquivo,variaveis)
    
    inicializar_feromonios(variaveis)
    
    variaveis.num_formigas = variaveis.num_vertices
    
    inicializar_formigas(variaveis)
    
    #print("Matriz de dist: ")
    #for linha in variaveis.matriz_distancias:
    #    print(linha)
        
    #print("matriz de feromonios:")
    #for linha in variaveis.matriz_feromonio:
    #    print(linha)
        
    #print("caminhos das formigas:")
    #for caminho in variaveis.caminho_formiga:
    #    print(caminho)
        
    for iteracao in range(variaveis.q):
        formigas = [Formiga(variaveis.num_vertices) for _ in range(variaveis.num_formigas) ] 
        melhor_caminho_iteracao = []
        melhor_fitness_iteracao = float('inf')
        
        for formiga in formigas:
            movimento_formiga(variaveis, formiga)
            formiga.fitness = calcular_fitness(formiga, variaveis)
            
            if formiga.fitness < melhor_fitness_iteracao:
                melhor_fitness_iteracao = formiga.fitness
                melhor_caminho_iteracao = formiga.caminho[:]
                
        if melhor_fitness_iteracao < variaveis.melhor_fitness_global:
                variaveis.melhor_fitness_global = melhor_fitness_iteracao
                variaveis.melhor_caminho_global = melhor_caminho_iteracao
                
        
        atualizar_feromonios(variaveis,formigas)
        
        print(f"Iteracao {iteracao +1}: Melhor Distancia = {melhor_fitness_iteracao}")
        
    print("\n Melhor caminho global: ",variaveis.melhor_caminho_global)
    print("\n Melhor fitness global: ", variaveis.melhor_fitness_global)
    
    #print("matriz de feromonios atualizada:")
    #for linha in variaveis.matriz_feromonio:
    #    print(linha)
            
main()