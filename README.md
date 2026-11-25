# data_challenges_fase_1
Fase 1 (T02) Projeto Integrador: Radar Legislativo - SQUAD 22005

Projeto Integrador v1
Descrição do Desafio


Toda quarta-feira, em Brasília, 513 deputados decidem o rumo de pautas que afetam diretamente o seu bolso, sua empresa, sua cidade.

Tributação, regulação de IA, marco do saneamento, reforma trabalhista.

Cada voto é registrado. Cada proposição é catalogada. Cada centavo da cota parlamentar é declarado.



Tudo isso é dado público, atualizado diariamente, disponível por uma API aberta e gratuita.



E mesmo assim, a maior parte das pessoas, empresas e até da imprensa acompanha esse fluxo no olho, lendo manchete, ouvindo boato, esperando o resumo do âncora da noite.



O problema não é falta de dado.

O problema é falta de engenharia de dados.



Quem consegue capturar, organizar, enriquecer com IA e transformar esse oceano de informação em sinal acionável tem uma vantagem absurda. Consultorias de relações governamentais cobram cinco dígitos por mês por relatórios que dão para automatizar. Empresas reguladas são pegas de surpresa por projetos que tramitavam há meses.



Esse é o pano de fundo do seu Projeto Integrador.



Aqui você vai juntar tudo o que aprendeu na Fase 1: Python, Pandas, SQL, Git, n8n e IA Generativa, em um único pipeline que roda do início ao fim. Não é mais um exercício isolado de aula. É o projeto que vai pro topo do seu GitHub e que você vai mostrar em entrevista.



🎙️ Antes de começar
Reserve uma hora para visitar a documentação da API da Câmara dos Deputados. Não precisa entender tudo. Só dê uma navegada, veja que tipo de informação está disponível, teste alguns endpoints no navegador mesmo.



🔗Datacast: https://drive.google.com/file/d/1c6gNQcKOMbVnh9kLzjkHwT6OPKIVMgey/view?usp=sharing



🔗Documentação: https://dadosabertos.camara.leg.br/swagger/api.html



O Cenário


Você foi contratado como engenheiro de dados de uma consultoria fictícia chamada Bússola Pública, uma empresa que vende inteligência legislativa para clientes corporativos (escritórios de advocacia, áreas de Relações Governamentais de grandes empresas, associações setoriais).



O CEO te chama na primeira semana e diz:

"Hoje a gente tem dois analistas lendo o site da Câmara o dia inteiro para montar um relatório semanal que a gente vende a R$ 15 mil por mês por cliente. Não escala. Quero que você construa um pipeline automatizado que pegue tudo o que importa, classifique por tema usando IA e me entregue isso pronto para virar produto."


Você assume e descobre alguns gargalos:

Não existe base de dados. Os analistas trabalham em planilhas pessoais.
Não há histórico organizado. Tudo o que foi consultado se perdeu.
A classificação por tema é inconsistente. Cada analista chama do que quer.
Os alertas dependem da memória do analista. Se ele esquece, o cliente é pego desprevenido.
Nenhum indicador é medido. Ninguém sabe quantas proposições por tema entram por semana, qual partido vota mais, qual deputado é mais ativo.


É nesse ambiente que você vai operar.



A Missão
Construir um pipeline completo de ETL com IA, em cinco etapas claras.



Etapa 1: Exploração da API
Antes de codar, entenda o terreno.

Navegue pelos endpoints da API: /deputados, /proposicoes, /votacoes, /partidos.
Faça chamadas com o Python para ver o formato de resposta.
Levante hipóteses sobre o que dá pra responder com esse dado.
Decida quais campos você vai usar e quais vai ignorar.


💡 Engenheiro de dados que pula essa etapa retrabalha o pipeline inteiro depois. Curiosidade primeiro, código depois.

Etapa 2: Extração com Python
Construa um notebook ou script Python que:

Faça as chamadas HTTP usando a biblioteca requests.
Trate paginação (a API entrega resposta em páginas — você precisa rodar um while até pegar tudo).
Trate erros simples (try/except) para quando a API der timeout ou retornar erro.
Salve o JSON bruto em arquivos locais antes de qualquer transformação.


💡 Por que salvar o JSON antes? Porque se o seu transform quebrar, você não precisa chamar a API de novo. Salvou uma vez, transforma quantas vezes quiser.

Etapa 3: Transformação com Pandas e carga no PostgreSQL
Aqui entra tudo o que você aprendeu de Pandas e SQL:

Carregue os JSONs em DataFrames com pd.read_json() ou pd.json_normalize().
Faça validações com Pandas: campos obrigatórios não nulos, datas dentro de um range válido, valores monetários positivos, deduplicação de registros.
Organize as tabelas em um modelo simples:
Tabelas fato: votacoes, proposicoes, despesas
Tabelas dimensão: deputados, partidos
Use SQLAlchemy ou psycopg2 para carregar no PostgreSQL.


📌 Onde hospedar seu PostgreSQL:



A forma mais simples e recomendada é usar o Supabase (https://supabase.com), é um PostgreSQL gerenciado, com plano gratuito generoso, painel web bonito para visualizar suas tabelas (Table Editor) e SQL Editor embutido. Não precisa instalar nada na sua máquina, e você compartilha o link do projeto na hora de apresentar.

Alternativas igualmente válidas: Neon (https://neon.tech) ou Railway (https://railway.app). Postgres local também serve, mas dá mais trabalho de configuração e você não consegue mostrar o banco rodando "na nuvem" no dia da apresentação.



💡 Bônus se usar Supabase: o pgvector já vem habilitado, o que facilita a Etapa 4 caso você escolha o caminho de embeddings.
💡 Validar com Pandas é tão simples quanto df[df['valor'] < 0] para encontrar valores inválidos. Não precisa de biblioteca exótica.

Etapa 4: Camada de IA (a parte que diferencia)
Essa é a parte que faz o seu projeto diferente de todo pipeline genérico de portfólio. Use o que viu no módulo de IA Generativa.

Escolha um dos dois caminhos (ou ambos, se quiser ousar):



Caminho A -> Classificação temática com embeddings

Para cada proposição, gere um embedding da ementa usando a API da OpenAI (text-embedding-3-small, é barato, custa centavos).
Crie embeddings também para uma lista de ~10 temas (Saúde, Tributário, Trabalho, Tecnologia, Meio Ambiente, etc.).
Calcule a similaridade de cosseno entre cada proposição e cada tema. O tema com maior similaridade é a classificação.
Salve essa classificação como uma coluna nova na tabela proposicoes.


Caminho B -> Resumo executivo automatizado

Para cada proposição, mande a ementa (e o texto completo, se disponível) para um LLM via API com um prompt do tipo: "Resuma essa proposição em 3 linhas, em linguagem clara para um executivo."
Salve o resumo como coluna nova.


💡 Controle seu custo. Antes de rodar para 1000 proposições, teste com 10. Veja quanto custou. Multiplique. Decida.

Etapa 5: Automação com n8n e versionamento no GitHub
n8n: monte pelo menos um workflow que execute o pipeline automaticamente. Sugestões:
Workflow diário às 06h que roda a ingestão incremental
OU workflow que envia um email semanal com as 5 proposições mais relevantes da semana
OU workflow que dispara alerta no Telegram quando uma proposição de tema crítico (ex: "Tecnologia") é apresentada
Dica: o n8n tem integração nativa com Supabase e Postgres — você consegue conectar direto no banco e fazer queries pelo workflow.


Git e GitHub: o projeto inteiro versionado, com:
Commits frequentes e descritivos (não vale um único commit "projeto final")
README explicando o que o projeto faz, como rodar, e mostrando prints do resultado
.gitignore correto (não suba sua API key da OpenAI!)
requirements.txt com as bibliotecas usadas


Entregáveis


✅ Repositório no GitHub com o pipeline completo (notebook ou scripts), README bem feito e instruções de como rodar.

✅ Banco PostgreSQL populado (Supabase, Neon ou similar) com pelo menos 30 dias de dados ingeridos. Compartilhe o link do projeto em modo leitura no README.

✅ Workflow n8n exportado (.json) e salvo no repositório, com print mostrando uma execução bem-sucedida.

✅ Documentação técnica curta (pode ser o próprio README) contendo:

Diagrama do pipeline (pode ser feito no Excalidraw)
Modelo das tabelas (pode ser texto mesmo, listando colunas e relacionamentos)
Quais decisões você tomou e por quê (ex: "escolhi classificar por embeddings porque..." )
Prompts usados na camada de IA
✅ Apresentação executiva (até 6 slides) no estilo pitch:

Qual é o problema da Bússola Pública
Como seu pipeline resolve
Demo do resultado (prints do banco, do dashboard se tiver, do n8n)
O que viria como próximo passo


Avaliação
Sua entrega será medida em cinco dimensões:



Funcionamento: O pipeline roda do início ao fim sem quebrar?

Modelagem: As tabelas estão organizadas de forma coerente?

IA aplicada: A camada de IA agrega valor real (não é decoração)?

Automação: O n8n está configurado e funcionando?

Comunicação: O README é claro? A apresentação convence?



⚠️ Erros comuns que você deve evitar
Querer pegar a API inteira de uma vez. Comece com 7 dias. Depois 30. Não tente baixar 4 anos de histórico no primeiro dia.
Usar IA como decoração. Se a classificação por tema não muda nada na saída, é teatro. Mostre que o tema agora aparece no relatório, no alerta, no email.
Deixar o n8n para última semana. Automação é metade do projeto. Comece a montar o workflow assim que tiver a primeira parte do pipeline funcionando.
README ralo. Recrutador olha o README primeiro. Se for ruim, ele nem clica nos arquivos. Coloque print, explique o problema, mostre o resultado.
Subir API key no GitHub. Use .env e .gitignore SEMPRE.
Não medir custo de IA. Antes de rodar embedding para 1000 proposições, rode para 10 e calcule.


📂 Materiais de apoio


🔗 Documentação da API: https://dadosabertos.camara.leg.br/swagger/api.html

🔗 Swagger interativo: https://dadosabertos.camara.leg.br/api/v2

🔗 PostgreSQL gratuito na nuvem (recomendado): https://supabase.com

🔗 Alternativas Postgres: https://neon.tech | https://railway.app

🔗 OpenAI API (para embeddings e resumos): https://platform.openai.com



Recado Final


Esse Projeto Integrador não é mais um trabalho de aula. É a peça central do seu portfólio quando você for buscar a próxima vaga como engenheiro de dados.



Recrutador sério não quer ver mais um pipeline do Titanic ou da Netflix. Quer ver alguém que pegou um problema real, com API real, com dado público de impacto e camada de IA que faz sentido, e entregou um pipeline que roda sozinho às 6 da manhã sem ninguém olhando.



Encare como se a Bússola Pública existisse de verdade e o CEO estivesse esperando o seu commit na sexta-feira.

Porque, no fim, vai estar mesmo.
