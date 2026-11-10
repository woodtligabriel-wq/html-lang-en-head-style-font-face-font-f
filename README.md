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

#### B. Gateway Pix BACEN / PSP & Autenticação ICP-Brasil
1. Selecione seu provedor Pix homologado:
   - **EFI Bank (antiga Gerencianet)**: Suporte completo a Pix com certificado mTLS ICP-Brasil e webhooks.
   - **Asaas / Mercado Pago**: Opções ágeis com APIs REST simplificadas.
   - **BACEN Direto (SPI/DICT)**: Para participantes diretos com certificado ICP-Brasil (AC-SPB / Serasa / Certisign).
2. Configure sua chave Pix e credenciais no `.env`.
3. Aponte a URL de notificação Pix do PSP para `https://seu-dominio.com/api/webhooks/pix`.

---

### 4. 🔐 Autenticação ICP-Brasil (mTLS & OAuth 2.0 RFC 8705)

No ecossistema de pagamentos instantâneos do Banco Central do Brasil (Pix), **a autenticação não é feita por senha comum**, mas sim através da **Infraestrutura de Chaves Públicas Brasileira (ICP-Brasil)**, cumprindo a **Resolução BCB nº 1/2020** e o **Manual de Segurança do Pix**:

#### Como nos Autenticamos:
1. **Certificado Digital e-CNPJ (A1 ou A3)**:
   - Emitido por uma Autoridade Certificadora credenciada na ICP-Brasil (Serasa Experian, Certisign, Soluti, etc.) ou AC-SPB.
   - Contém a chave pública X.509 v3 e a chave privada RSA de 2048 bits protegida no servidor.
2. **Handshake mTLS (Mutual TLS 1.2 / 1.3)**:
   - Ambas as pontas comprovam sua identidade criptográfica antes da troca de mensagens HTTP.
   - O servidor do BACEN/PSP valida nossa cadeia ICP-Brasil e nosso servidor valida a raiz do BACEN.
3. **Token OAuth 2.0 Atrelado ao Certificado (RFC 8705)**:
   - Chamada `POST /oauth/token` sob o canal mTLS. O token `access_token` gerado fica travado no hash SHA-256 (fingerprint) do nosso certificado ICP-Brasil, tornando-o inútil se for interceptado fora do túnel TLS.
4. **Endpoint de Status ICP no Servidor**:
   - `GET /api/pix/icp-status`: Retorna as especificações técnicas, status do certificado local e cadeia ICP-Brasil.

#### Conversão do Certificado (.p12 / .pfx para .pem):
```bash
# Extraia o certificado e chave privada sem criptografia para uso no Node.js:
openssl pkcs12 -in certificado_empresa.p12 -out certs/pix_producao.pem -nodes
```

#### Uso no Node.js (mTLS Agent):
```javascript
const https = require('node:https');
const fs = require('node:fs');

const agent = new https.Agent({
  cert: fs.readFileSync('./certs/pix_producao.pem'),
  key: fs.readFileSync('./certs/pix_producao.pem'),
  rejectUnauthorized: true
});
```

> 💡 **Nota sobre a sigla "ICP":**
> - **No projeto financeiro / BACEN**: ICP refere-se à **ICP-Brasil** (Certificação Digital e-CNPJ / mTLS Pix).
> - **No ecossistema Web3 / Cripto**: ICP refere-se ao **Internet Computer Protocol (DFINITY)**, autenticado via *Internet Identity* (WebAuthn / Passkeys com FaceID/TouchID através da lib `@dfinity/auth-client`).

---

## 🛡️ Governança e Regras BSC Implementadas

- **FCR (First Contact Resolution)**: Janela de contestação de 7 dias corridos após confirmação do Pix.
- **Audit Trail WORM**: Logs gravados com hash criptográfico SHA-256 e imutabilidade para auditoria LGPD.
- **Quarentena BSC 120s**: Proteção contra race conditions e ataques de double-spend no Pix.
- **Scan de Linguagem Formal**: Filtro obrigatório de mensagens corporativas antes do disparo via WhatsApp.
