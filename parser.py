import xml.etree.ElementTree as ET
import csv
import datetime
import sys

anosDeProducao = 4

def extrairTrabalhosEmEventos(xmlMember) :
 rows = []
 for child in xmlMember :
 	row = ['','','','']
 	dados = child.find('DADOS-BASICOS-DO-TRABALHO')
 	ano = int(dados.get('ANO-DO-TRABALHO')) 
 	if datetime.datetime.now().year - ano <= anosDeProducao :
 	 row.append(ano)
 	 row.append('Evento')
 	 row.append(dados.get('NATUREZA'))
 	 dados = child.find('DETALHAMENTO-DO-TRABALHO')
 	 row.append(dados.get('NOME-DO-EVENTO'))
 	 row.append('')
 	 row.append('')
 	 dados = child.findall('AUTORES')
 	 row.append(len(dados))
 	 row.append('')
 	 row.append(child.find('DADOS-BASICOS-DO-TRABALHO').get('DOI'))
 	 rows.append(row)
  
 return rows
	
def extrairArtigos(xmlMember) : 
 rows = []
 for child in xmlMember :
 	row = ['','','','']
 	dados = child.find('DADOS-BASICOS-DO-ARTIGO')
 	ano = int(dados.get('ANO-DO-ARTIGO')) 
 	if datetime.datetime.now().year - ano <= anosDeProducao :
 	 row.append(ano)
 	 row.append('Journal')
 	 row.append(dados.get('NATUREZA'))
 	 dados = child.find('DETALHAMENTO-DO-ARTIGO')
 	 row.append(dados.get('TITULO-DO-PERIODICO-OU-REVISTA'))
 	 row.append('')
 	 row.append('')
 	 dados = child.findall('AUTORES')
 	 row.append(len(dados))
 	 row.append('')
 	 row.append(child.find('DADOS-BASICOS-DO-ARTIGO').get('DOI'))
 	 rows.append(row)
  
 return rows
	
def extrairLivrosECapitulos(xmlMember) :
 rows = []
 for child in xmlMember :
 	if child.tag == 'LIVROS-PUBLICADOS-OU-ORGANIZADOS' :
 		rows = rows + extrairLivros(child)
 	elif child.tag == 'CAPITULOS-DE-LIVROS-PUBLICADOS' : 
 		rows = rows + extrairCapitulos(child)
 
 return rows

def extrairLivros(xmlMember): 
 rows = []
 for child in xmlMember :
 	row = ['','','','']
 	dados = child.find('DADOS-BASICOS-DO-LIVRO')
 	ano = int(dados.get('ANO')) 
 	if datetime.datetime.now().year - ano <= anosDeProducao :
 	 row.append(ano)
 	 row.append('Livro')
 	 row.append(dados.get('NATUREZA'))
 	 row.append(dados.get('TITULO-DO-LIVRO'))
 	 #dados = child.find('DETALHAMENTO-DO-LIVRO')
 	 row.append('')
 	 row.append('')
 	 dados = child.findall('AUTORES')
 	 row.append(len(dados))
 	 row.append('')
 	 row.append(child.find('DETALHAMENTO-DO-LIVRO').get('ISBN'))
 	 
 	 rows.append(row)
  
 return rows

def extrairCapitulos(xmlMember) :
 rows = []
 for child in xmlMember :
 	row = ['','','','']
 	dados = child.find('DADOS-BASICOS-DO-CAPITULO')
 	ano = int(dados.get('ANO')) 
 	if datetime.datetime.now().year - ano <= anosDeProducao :
 	 row.append(ano)
 	 row.append('Capitulo')
 	 row.append('Capitulo')
 	 row.append(dados.get('TITULO-DO-CAPITULO-DO-LIVRO'))
 	 row.append('')
 	 row.append('')
 	 dados = child.findall('AUTORES')
 	 row.append(len(dados))
 	 row.append('')
 	 row.append(child.find('DETALHAMENTO-DO-CAPITULO').get('ISBN'))
 	 rows.append(row)
  
 return rows

def main() : 
 
 if len(sys.argv) != 2 :
  print('Sintaxe: python3 parser <arquivo lattes em formato xml>')
  exit(-1)

 tree = ET.parse(sys.argv[1])
 root = tree.getroot()
 

 # create the csv writer object

 #csvwriter = csv.writer(csvfile)
 resident_head = []

 root = tree.getroot()
 rows = [['Professor', 'Depto Grad',	'Pos-grad',	'Efetivo / Substituto / Visitante (E/S/V)',	'Ano Publicação','Journal, Evento, Livro, Capitulo', 'Completo/Resumo Expandido/Resumo', 'Nome Journal/Evento', 'Qualis Sucupira (Mais recente)', 'Impact Factor (p/ Journal)',	'Número Autores', 'Número Instituições Envolvidas',	'DOI/ISBN']]
 rows.append([root.find('DADOS-GERAIS').get('NOME-COMPLETO'),'','','','','','','','','','','',''])
 trabalhos = root.find('PRODUCAO-BIBLIOGRAFICA')
 for tipoTrabalho in trabalhos :
   if tipoTrabalho.tag == 'TRABALHOS-EM-EVENTOS' :
    rows = rows + extrairTrabalhosEmEventos(tipoTrabalho)
   elif tipoTrabalho.tag == 'ARTIGOS-PUBLICADOS' :
    rows = rows + extrairArtigos(tipoTrabalho)
   elif tipoTrabalho.tag == 'LIVROS-E-CAPITULOS' :
    rows = rows + extrairLivrosECapitulos(tipoTrabalho)

 #print(rows)
 csvfilename = root.find('DADOS-GERAIS').get('NOME-COMPLETO').replace(' ','') + '.csv'
 csvfile = open(csvfilename, 'w',encoding='utf-8')
 csvwriter = csv.writer(csvfile)
 csvwriter.writerows(rows)

if __name__== "__main__":
  main()