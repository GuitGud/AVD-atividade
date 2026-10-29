# Publicação no Streamlit Community Cloud

A publicação ainda está pendente: a automação do navegador foi interrompida por não conseguir identificar a URL com segurança. O repositório e o app estão preparados para esta etapa. Não foi criado um endereço fictício de aplicação.

## Configuração

1. Abra https://share.streamlit.io e entre na sua conta.
2. Clique em **Create app** e escolha **Yup, I have an app**.
3. Informe:
   - Repository: `GuitGud/AVD-atividade`
   - Branch: `codex/aula21`
   - Main file path: `app.py`
4. Em **Advanced settings**, use Python **3.12**. O projeto não precisa de secrets.
5. Se quiser, escolha um subdomínio disponível. Clique em **Deploy** e aguarde o carregamento dos dois painéis.
6. Copie o link efetivamente atribuído pelo Streamlit. Só então registre a URL no README.

Alternativa: use **Paste GitHub URL** com:
https://github.com/GuitGud/AVD-atividade/blob/codex/aula21/app.py

## Registrar o link real

Após publicar, execute na raiz do projeto, substituindo o endereço pelo link real:

```powershell
.venv\Scripts\python.exe scripts/registrar_publicacao.py --url https://SEU-APP.streamlit.app
```

O script exige HTTPS e domínio streamlit.app, confere resposta HTTP e troca apenas o bloco de publicação do README. Não declara que widgets ou navegação em janela anônima foram testados. Revise e envie as alterações com Git.

## Conferência em janela anônima

Abra uma janela **InPrivate** no Edge (Ctrl+Shift+N), cole a URL pública e siga `entregas/teste-app-publicado.md`. Acesso HTTP 200 ou teste local não comprova o funcionamento dos widgets no app publicado.

Referência oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
