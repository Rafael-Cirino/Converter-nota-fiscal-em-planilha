# `Conversor de nota fiscal em planilha`
# `Convert invoice to spreadsheet`

## Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação *EA979A - Introdução a Computação Gráfica e Processamento de Imagens*, 
oferecida no primeiro semestre de 2022, na Unicamp, sob supervisão da Profa. Dra. Paula Dornhofer Paro Costa, do Departamento de Engenharia de Computação e Automação (DCA) da Faculdade de Engenharia Elétrica e de Computação (FEEC).

> |Nome  | RA | Curso|
> |--|--|--|
> | Rafael Cirino  | 223730  | Eng. Elétrica|


## Descrição do Projeto
> Observando o trabalho que meu pai tinha ao chegar do supermercado e ter que adicionar item por item da compra em uma planilha excel, pensei por que não deselvover um algoritmo capaz de a partir de uma imagem extrair as informações contidas na nota fiscal


## Plano de Trabalho
> Nesta primeira entrega, seu grupo deve ser capaz de identificar quais são as etapas necessárias para alcançar o objetivo proposto.
> Nesta seção, identifique claramente essas etapas, estimando o tempo que o seu grupo gastará em cada uma delas.
> Por exemplo:
> * Etapa 1 (1 semana): Estudo de técnicas OCR (Reconhecimento ótico de caracteres)
>    - Pesquisar sobre o funcionamento de algoritmos que indentificam texto em imagem 
> * Etapa 2 (2 semana): Blibliotecas, planilha e padrões
>   - Pesquisar bibliotecas para Python que reconhecem texto em imagem e decidir sobre utilizar uma ou desenvolver uma própria. 
>   - Pensar qual o melhor formato para salvar as informações em .csv, google sheets ou planilha padrão do Excel.
>   - Indentificar padrões contidos em diferentes notas fiscais.
> * Etapa 3 (6 semanas): Codificação.
>   - Desenvolver o conversor de texto em imagem para uma planilha, 
>   - Validar e testar para os mais diferentes dados possíveis
>   - Redigir o relatório a ser entregue no final
> 
> OBS: Ao longo das etapas vou montar um banco de dados com imagens de nota fiscal para validação ao final do projeto

## CNFP
### Sobre o OCR
OCR é um acrónimo para o inglês Optical Character Recognition, é uma tecnologia para reconhecer caracteres a partir de um arquivo de imagem ou mapa de bits sejam eles escaneados, escritos a mão, datilografados ou impressos. Dessa forma, através do OCR é possível obter um arquivo de texto editável.

### Tesseract e Pytesseract
O Tesseract é um mecanismo de recocimento de texto utilizando OCR, suporta uma grande variedade de idiomas. Tendo uma imagem como entrada, ele realiza alguns processamentos a fim de obter menos ruídos, em seguida, utilizando uma RNN chamada LSMT(Muito boa para reconhecer sequências longas) reconhece o texto contigo na imagem retornando uma string.

O Pytesseract, é um wrapper do Tesseract para python que em conjunto com a biblioteca PIL torna possível realizar essa técnica de reconhecimento sobre uma imagem

<figure>
    <img src="Image/tesseract.png"
         alt="Pytesseract"
         height="70%"
         width="70%">
    <figcaption>Loki com o pytesseract</figcaption>
</figure>

## Referências Bibliográficas
> * How to OCR with Tesseract, OpenCV and Python - https://nanonets.com/blog/ocr-with-tesseract/
>
> * OCR a document, form, or invoice with Tesseract, OpenCV, and Python - https://pyimagesearch.com/2020/09/07/ocr-a-document-form-or-invoice-with-tesseract-opencv-and-python/
>
> * “Lendo imagens”! — Uma abordagem a OCR com Google tesseract e Python! - https://blog.codeexpertslearning.com.br/lendo-imagens-uma-abordagem-%C3%A0-ocr-com-google-tesseract-e-python-ee8e8009f2ab
