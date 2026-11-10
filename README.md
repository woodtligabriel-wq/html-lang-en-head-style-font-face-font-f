# MUSE + META | Camada de Canais e Pagamentos

Arquitetura de integração com governança BSC, compliance BACEN Pix, LGPD e Meta WhatsApp Cloud API.

---

## 🚀 Conexão de Base de Dados e APIs

Este projeto conta com um servidor backend completo e auto-contido em Node.js (v22+) com suporte a SQLite local (zero dependências externas) e PostgreSQL / Supabase, além de endpoints para webhooks e envio de mensagens.

### 1. Início Rápido (Local com SQLite Embutido)

Para iniciar o servidor backend imediatamente:

```bash
# Executar servidor backend na porta 3001
npm start
# ou:
node backend/server.js
```

Para rodar o teste de fluxo automatizado ponta a ponta:

```bash
npm test
# ou:
node backend/test-flow.js
```

---

### 2. Conectando a uma Base de Dados em Nuvem (Supabase / PostgreSQL)

1. Crie um projeto gratuito no [Supabase](https://supabase.com).
2. No menu **Project Settings -> Database**, copie a `Connection URI` (modo Transaction Pooler ou Direct).
3. Execute o script DDL contido em `backend/schema.sql` no SQL Editor do Supabase para criar as tabelas:
   - `pedidos`
   - `pix_transacoes`
   - `audit_trail_worm`
   - `idempotency_keys`
4. Crie um arquivo `.env` na raiz (baseado em `backend/.env.example`) e configure:
   ```env
   DATABASE_URL=postgresql://postgres.xxx:senha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
   ```

---

### 3. Conectando às APIs

#### A. Meta WhatsApp Cloud API
1. Acesse o [Meta for Developers](https://developers.facebook.com/) e crie um App do tipo **Business**.
2. Adicione o produto **WhatsApp** -> **API Setup**.
3. Obtenha o `Phone Number ID` e gere um `Access Token`.
4. Configure o Webhook apontando para `https://seu-dominio.com/api/webhooks/meta` com o token de verificação configurado em `META_VERIFY_TOKEN`.

#### B. Gateway Pix BACEN / PSP
1. Selecione seu provedor Pix homologado:
   - **EFI Bank (antiga Gerencianet)**: Excelente suporte a Pix com certificado mTLS e webhooks em homologação.
   - **Asaas / Mercado Pago**: Opções ágeis com APIs REST simplificadas.
   - **BACEN Direto**: Para participantes diretos com certificado ICP-Brasil.
2. Configure sua chave Pix e credenciais no `.env`.
3. Aponte a URL de notificação Pix do PSP para `https://seu-dominio.com/api/webhooks/pix`.

---

## 🛡️ Governança e Regras BSC Implementadas

- **FCR (First Contact Resolution)**: Janela de contestação de 7 dias corridos após confirmação do Pix.
- **Audit Trail WORM**: Logs gravados com hash criptográfico SHA-256 e imutabilidade para auditoria LGPD.
- **Quarentena BSC 120s**: Proteção contra race conditions e ataques de double-spend no Pix.
- **Scan de Linguagem Formal**: Filtro obrigatório de mensagens corporativas antes do disparo via WhatsApp.
