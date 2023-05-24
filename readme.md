# Extração de Dados da CGU no DOU
Utilizando o inlabs. Baixa arquivos xml diariamente, limpa os arquivos, para: 1. controlar designações e dispensas 2. gerar relatório diário em PDF.

## Extração para Tratamento:
Baixa xml via: python -W ignore inlabs-auto-download-xml.py
fetch.py faz o tratamento e extração. baixa_pdf.py baixa o pdf das designações detectadas e faz o highlight das partes alvo, para o upload no AFD.

## Relatório Diário
Relatorio_Diario trata os dados, de forma similar à extração padrão, e então gera um PDF com os destaques do dia que envolvem a Controladoria-Geral da União. Main.py percorre os arquivos xml e chama as demais funções. generate_highlight.py gera o texto de destaque da portaria no PDF.