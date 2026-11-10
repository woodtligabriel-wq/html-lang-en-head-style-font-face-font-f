-- =========================================================================
-- MUSE + META | Camada de Canais e Pagamentos
-- Schema DDL Universal (Compatível com PostgreSQL, Supabase e SQLite)
-- Regras: BSC Quorum Governance, FCR 7 dias e Auditoria WORM (LGPD + BACEN)
-- =========================================================================

-- 1. Tabela de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
  id VARCHAR(64) PRIMARY KEY,
  cliente_nome VARCHAR(255) NOT NULL,
  whatsapp VARCHAR(32) NOT NULL,
  valor NUMERIC(12, 2) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'AGUARDANDO_PIX',
  txid VARCHAR(64) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pedidos_txid ON pedidos(txid);
CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status);

-- 2. Tabela de Transações Pix
CREATE TABLE IF NOT EXISTS pix_transacoes (
  end_to_end_id VARCHAR(128) PRIMARY KEY,
  txid VARCHAR(64) NOT NULL,
  valor NUMERIC(12, 2) NOT NULL,
  chave_pix VARCHAR(255) NOT NULL,
  status VARCHAR(32) NOT NULL,
  payload_raw TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pix_txid ON pix_transacoes(txid);

-- 3. Tabela de Trilha de Auditoria WORM Imutável (LGPD / BACEN)
CREATE TABLE IF NOT EXISTS audit_trail_worm (
  id VARCHAR(128) PRIMARY KEY,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tipo_evento VARCHAR(64) NOT NULL,
  txid VARCHAR(64),
  whatsapp_id VARCHAR(128),
  hash_sha256 VARCHAR(64) NOT NULL,
  dados_json TEXT NOT NULL,
  fcr_deadline TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_tipo ON audit_trail_worm(tipo_evento);
CREATE INDEX IF NOT EXISTS idx_audit_txid ON audit_trail_worm(txid);

-- 4. Tabela de Idempotência (Prevenção de double-charge e replay attack)
CREATE TABLE IF NOT EXISTS idempotency_keys (
  chave_hash VARCHAR(64) PRIMARY KEY,
  endpoint VARCHAR(255) NOT NULL,
  response_json TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expira_em TIMESTAMP WITH TIME ZONE NOT NULL
);
