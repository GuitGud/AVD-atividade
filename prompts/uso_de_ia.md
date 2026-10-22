# Declaração de uso de IA

**Ferramenta:** Codex / OpenAI. **Data:** 22/10/2026.

**Aplicação:** leitura do material da Aula 21, identificação dos entregáveis, adaptação do notebook já encontrado no computador, inclusão do dataset local, exportação dos CSVs, criação do esqueleto Streamlit, documentação e testes.

**Decisões implementadas:** preservar o tratamento de casos incompletos do notebook; manter outliers; selecionar somente as cinco quantitativas da EDA; usar os containers e widgets nativos do Streamlit; reservar os gráficos para a próxima etapa; corrigir os limites das faixas etárias e uma observação sobre Pearson.

**Verificação automática:** execução completa da EDA e testes dos dados exportados e de interações do app, conforme `docs/VALIDACAO.md`.

**Participação do aluno:** solicitou a atividade e confirmou o uso do notebook Heart Disease encontrado. Esta declaração não afirma que o aluno já revisou todas as células, conferiu os gráficos ou obteve aprovação docente do dataset. A revisão e a apresentação final cabem ao aluno.

**Prompt de implementação:** adaptar o modelo da professora à EDA confirmada, com sidebar para seleção das quantitativas e seus intervalos; área principal em duas colunas para correlação e distribuição; placeholders para os gráficos da Aula 22; arquivos de dados locais e exportação reproduzível pelo notebook; entrega com histórico Git.
