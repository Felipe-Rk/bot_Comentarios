Automatização de Respostas para Instagram/Facebook
Este projeto é uma ferramenta de automação para responder a comentários em posts de Instagram e Facebook. 
Utiliza Selenium para interação com o navegador e Tkinter para uma interface gráfica amigável e IA para gerar as repostas.

Funcionalidades
- Automação de Respostas: Responde automaticamente a comentários em posts com base em regras definidas e mensagens personalizadas com a utilização de IA para Obter respostas mais claras e personalizadas apartir de um prompropt.
- Interface Gráfica: Interface fácil de usar desenvolvida com Tkinter para configurar e iniciar o processo de automação.
- Processamento de Comentários: Coleta e processa comentários, verificando se foram respondidos e aplicando respostas apropriadas.
- Geração de Logs: Registra logs detalhados sobre comentários extraidos e respondidos, comentários ofensivos ou que ocorreu algum erro.
- Respostas Automatizadas com IA: Integração com um sistema de IA para criar respostas personalizadas.
- Filtro de Comentários: Aplicação de filtros para gerenciar comentários ofensivos ou irrelevantes.
- Opção de Comentários: Seleção para responder a todos comentários da publicação ou somente os relevantes.

Requisitos
Python 3.x: Versão 3.6 ou superior.
Bibliotecas Python:
tkinter (para a interface gráfica)
selenium (para automação do navegador)
ttkthemes (para temas da interface gráfica)
re (para manipulação de expressões regulares)
ChromeDriver (para automação do código com o google chromer)


Uso
Configuração:

Abra o arquivo interface.pyw para iniciar a interface gráfica.
Na Interface Gráfica:

> Insira a URL do post no campo "Link", Facebook ou Instagram, ele irá reconhecer sozinho.
> Preencha o nome de usuário no campo "Nome do Usuário", para definir se o usuário ja respondeu ao comentário ou não.
>Adicione uma mensagem personalizada se desejar, quanto mais clara a mensagem, melhor a IA irá responder, pode ser a legenda do post ou algo relacionado
>Selecione as opções de filtro e tipo de comentários conforme necessário.
Executar:

Clique em "Executar" para iniciar o processo de automação.
*Na primeira execução vai ser pedido para logar a rede social e tambem na página da IA para uma melhor utilização.

Visualizar Logs:

Use o botão "Abrir Pasta de Logs" para acessar os logs gerados durante o processo.
Logs de execução caso ocorra um erro ou finalize com sucesso.
Logs de bloqueio para respostas consideradas ofensivas ou que não puderam ser respondidas.

Todos os logs possuem o link da publicação, o nome do usuario, e o ID do comentário. 

Caso deseje localizar o mesmo:
>acessar o facebook apartir do link salvo
>Apertar F12 ou botão direito e Inspecionar 
>Apertar Ctrl + F para pesquisa dentro da janela que ira abrir com o código da pagina
>Colar o ID do comentário e pressionar Enter para pesquisar.


Este projeto foi desenvolvido inteiramente por mim, e estou disponibilizando para fins de estudo ou como uma ferramenta de trabalho.

Felipe Roiko Felix da Silva
