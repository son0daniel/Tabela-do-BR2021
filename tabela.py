#Importação de bibliotecas
from time import sleep #Da bilioteca time importar apenas a função 'sleep'
from bs4 import BeautifulSoup #Importar BeautifulSoup para trabalhar com HTML
#Importação do Selenium
from selenium import webdriver
import pandas as pd

url = 'https://ge.globo.com/futebol/brasileirao-serie-a/'
op = webdriver.ChromeOptions()
op.add_argument('headless') #Argumento que impede que o navegador seja aberto e trabalhe silenciosamente
driver = webdriver.Chrome('./chromedriver.exe', options=op) #Pega o webdriver do Chrome localizado na pasta
driver.get(url) #Acessa a URL
sleep(.5) #Tempo suficiente para renderizar JavaScript da maioria das páginas
pagina = driver.page_source #Pega o HTML da página renderizada
driver.close() #Fecha o navegador

sopa = BeautifulSoup(pagina, 'html.parser') #Transforma o conteúdo renderizado do site em html
times = sopa.find_all('strong', attrs={'class': 'classificacao__equipes classificacao__equipes--nome'}) #Pega os nomes das equipes presentes no HTML
estatistica = sopa.find('table', attrs={'class': 'tabela__pontos'}) #Pega a tabela de classificação
estatisticas = estatistica.find_all('tr', {'class': 'classificacao__tabela--linha'}) #Pega as estatísticas (pontos, vitórias, etc)

equipes = [] #Lista de equipes
for x in times:
    equipes.append(x.text)

desempenho = [] #Lista que armazena o desempenho das equipes
count = 0
for x in estatisticas:
    lista = [] #Lista que armazena o nome da equipe e seu respectivo desempenho
    lista.append(equipes[count])
    count+=1
    for y in x:    
        if y.text != '': #Evita a coleta de conteúdo vazio
            lista.append(y.text)
    desempenho.append(lista)

tabela_df = pd.DataFrame(desempenho, columns=['Time', 'Pts', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', '%']) #Cria uma tabela com as colunas 'Time', 'Pts', etc
print(tabela_df)
#Resultado do print
#              Time Pts   J   V  E   D  GP  GC   SG     %
# 0     Atlético-MG  42  19  13  3   3  29  13   16  73.7
# 1       Palmeiras  35  19  11  2   6  30  23    7  61.4
# 2        Flamengo  34  17  11  1   5  35  17   18  66.7
# 3       Fortaleza  33  20   9  6   5  29  22    7    55
# 4      Bragantino  32  19   8  8   3  30  21    9  56.1
# 5     Corinthians  29  20   7  8   5  19  17    2  48.3
# 6      Fluminense  28  20   7  7   6  20  21   -1  46.7
# 7          Cuiabá  27  20   6  9   5  21  20    1    45
# 8     Atlético-GO  26  19   6  8   5  16  18   -2  45.6
# 9    Athletico-PR  24  19   7  3   9  23  23    0  42.1
# 10          Ceará  24  19   5  9   5  19  21   -2  42.1
# 11  Internacional  23  18   5  8   5  22  22    0  42.6
# 12         Santos  23  20   5  8   7  20  25   -5  38.3
# 13      Juventude  23  20   5  8   7  17  23   -6  38.3
# 14          Bahia  22  20   6  4  10  24  32   -8  36.7
# 15      São Paulo  22  19   5  7   7  16  22   -6  38.6
# 16     América-MG  21  19   5  6   8  17  22   -5  36.8
# 17         Grêmio  19  18   5  4   9  14  18   -4  35.2
# 18          Sport  17  19   3  8   8   8  14   -6  29.8
# 19    Chapecoense  10  20   1  7  12  17  32  -15  16.7
tabela_df.to_excel('tabela_do_br2021.xlsx', index=False) #Transforma a tabela em planilha de excel