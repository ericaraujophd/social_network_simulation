# Espalhamento de Fakenews - Um modelo de simulação do impacto do uso de WhatsApp na propagação de informações

Este repositório contém o código e resultados de um modelo para demonstrar como o espalhamento de informação se dá em vários contextos diferentes de países distintos. O código foi criado por Eric Araújo, e quaisquer dúvidas podem ser enviadas para eric@ufla.br.

O modelo considera que um grupo de 1.000 (mil) pessoas está conectado por meio de uma rede social que simula o uso do WhatsApp. Esta rede considera que a distribuição das conexões das pessoas segue um modelo [Small-world](https://pt.wikipedia.org/wiki/Redes_de_pequeno_mundo). Este modelo é utilizado para descrever redes de influência social, motivo pelo qual utilizaremos este modelo aqui.

Este código serve única e exclusivamente para fins didáticos. Dados reais não foram utilizados para validar o modelo.

Cada pessoa em nossa rede apresenta uma opinião política, que varia de -1 a 1. O valor de -1 indica uma opinião mais à esquerda, e 1 seria uma opinião mais à direita. valores próximos de 0 indicam centristas. 

Quando uma postagem é gerada por um indivíduo na rede, seus vizinhos terão acesso à informação, e decidirão se compartilharão ou não baseado em um método estocástico, onde a probabilidade de compartilhamento é maior caso a informação esteja mais alinhada com o seu posicionamento, simulando assim o viés de confirmação.

Serão 3 cenários testados.

1. O cenário brasileiro.
2. O cenário britânico.
3. Um cenário onde não existem grupos públicos, e as pessoas só têm acesso à informação de seus vizinhos.

Segundo pesquisa da [Reuters 2019](https://reutersinstitute.politics.ox.ac.uk/sites/default/files/inline-files/DNR_2019_FINAL.pdf):

* 53\% da população usa WhatsApp como rede principal para discutir e compartilhar notícias. 
* 58\% dos usuários de WhatsApp fazem parte de grupos com pessoas que eles não conhecem (12\% no Reino Unido)
* 18\% dos usuários brasileiros de WhatsApp discutem notícias e política em grupos públicos (2\% no Reino Unido)
* 22\% dos usuários de Facebook se apoiam em informações de grupos públicos e privados com desconhecidos para se informar sobre política e das notícias (8\% no Reino Unido).

Desta forma, para os cenários 1 e 2 consideramos a porcentagem de pessoas que fazem parte de grupos públicos ao conectar indivíduos que não são conhecidos nas mesmas proporções levantadas pela pesquisa da Reuters 2019. Para o cenário 3, não existirão grupos públicos/privados para compartilhamento de informação.

## Criando grupos públicos

Grupos públicos são criados a partir da afinidade entre os agentes. Dessa forma, 3 grupos públicos serão criados, considerando a partir do posicionamento político das pessoas. A ideia é que a porcentagem de pessoas em um grupo corresponda ao valor acima, 22\% para os brasileiros, e 8\% para os britânicos.

## Modelo de geração de postagens

Baseado nas estatísticas do Facebook disponíveis pela [OMNICORE](https://www.omnicoreagency.com/facebook-statistics/), o Facebook tem:

* 55 milhões de updates (postagens) por dia.
* 1.59 bilhões de usuários ativos diariamente.

Desta forma, consideramos que a chance de um usuário criar uma nova postagem é de 55 milhões em 1.59 bilhões, ou 0.034\% de chances de fazer uma postagem.

Cada membro da rede poderá gerar uma postagem a cada passo do modelo com probabilidade de 0.034%. Essa postagem conterá um valor referente à carga política (ou viés político) do conteúdo. Para tal, usaremos uma distribuição normal com desvio padrão de 0.1 da posição do agente.

## Modelo de decisão de compartilhamento

O usuário irá verificar a sua concordância com a postagem criada por meio da verificação da diferença entre o conteúdo do post e sua opinião pessoal. Esse cálculo é feito considerando a seguinte fórmula:

$$chance = 1 - |x0 - x1|/2$$

![formula](https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1)


## Medidas de espalhamento

Para mensurar o alcance das mensagens, contabilizaremos quantas vezes cada mensagem foi propagada.
