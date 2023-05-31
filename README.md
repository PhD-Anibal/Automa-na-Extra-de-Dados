# Robô
# Automação na Extração de Dados em Anúncios no Mercado Livre (Versão Beta)

## Resumo
O Mercado Livre é uma das maiores plataformas de comércio eletrônico da América Latina, onde milhões de usuários realizam compras e vendas diariamente. Com a ajuda deste programa, é possível automatizar o processo de extração de dados, economizando tempo e facilitando a análise de grandes quantidades de informações. Este programa Python de automação é capaz dede automatizar a extração de informações de anúncios do Mercado Livre, separados por estado. O programa usa o Selenium para interagir com o site, o WebDriver para controlar o navegador, o Requests para obter dados HTTP e o Pandas para organizar os dados coletados. Com base nos dados extraídos, numa segunda etapa é possível obter insights valiosos sobre os produtos mais populares em cada região, preços médios, preferências dos consumidores e muito mais.

![sequências de etapas do robô](https://github.com/PhD-Anibal/Automa-na-Extra-de-Dados/assets/128927981/1167e394-ef06-4071-a1a0-cfdbece71ead)

## Principais recursos e bibliotecas utilizadas:
- **Selenium**: É uma biblioteca muito popular para automação de testes e scraping. Ele permite interagir com elementos da página da web, preencher formulários, clicar em botões e navegar pelas páginas.

- **WebDriver**: O WebDriver é um componente essencial para o Selenium, permitindo o controle do navegador de forma automatizada. Existem várias opções de WebDriver disponíveis, como o ChromeDriver, o GeckoDriver (para o Firefox) e o Microsoft WebDriver (para o Microsoft Edge).

- **Requests**: A biblioteca Requests é amplamente utilizada para fazer solicitações HTTP em Python. É uma ferramenta poderosa para enviar solicitações a servidores web e receber respostas.

- **Pandas**: O Pandas é uma biblioteca muito popular para manipulação e análise de dados em Python. Ele fornece estruturas de dados flexíveis e eficientes, como o DataFrame, que permite organizar os dados extraídos em uma estrutura tabular adequada para análises posteriores.

## Detalhes
- Também foi acrescentada a funcionalidade de continuar uma busca anterior, caso por algum motivo a busca anterior seja interrompida.
- No final, também há a possibilidade de buscar novamente por links quando a página não carregou corretamente devido a alguma falha na conexão de internet.
