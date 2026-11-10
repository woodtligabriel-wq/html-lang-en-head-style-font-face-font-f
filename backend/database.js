/**
 * MUSE + META: Camada de Canais e Pagamentos
 * Módulo de Conexão com Base de Dados (SQLite Nativo Node 22 / Suporte PostgreSQL / Supabase)
 * Em conformidade com governança BSC, FCR 7 dias e Auditoria WORM (LGPD + BACEN)
 */

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { DatabaseSync } = require('node:sqlite');

const DATA_DIR = path.join(__dirname, '..', 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const DB_FILE = path.join(DATA_DIR, 'database.sqlite');
const db = new DatabaseSync(DB_FILE);

// Inicialização do Schema do Banco de Dados
function initDatabase() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS pedidos (
      id TEXT PRIMARY KEY,
      cliente_nome TEXT NOT NULL,
      whatsapp TEXT NOT NULL,
      valor REAL NOT NULL,
      status TEXT NOT NULL DEFAULT 'AGUARDANDO_PIX',
      txid TEXT UNIQUE,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pix_transacoes (
      end_to_end_id TEXT PRIMARY KEY,
      txid TEXT NOT NULL,
      valor REAL NOT NULL,
      chave_pix TEXT NOT NULL,
      status TEXT NOT NULL,
      payload_raw TEXT,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_trail_worm (
      id TEXT PRIMARY KEY,
      timestamp TEXT NOT NULL,
      tipo_evento TEXT NOT NULL,
      txid TEXT,
      whatsapp_id TEXT,
      hash_sha256 TEXT NOT NULL,
      dados_json TEXT NOT NULL,
      fcr_deadline TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS idempotency_keys (
      chave_hash TEXT PRIMARY KEY,
      endpoint TEXT NOT NULL,
      response_json TEXT NOT NULL,
      created_at TEXT NOT NULL,
      expira_em TEXT NOT NULL
    );
  `);
}

initDatabase();

// Funções de manipulação do banco

function criarPedido({ cliente_nome, whatsapp, valor, txid = null }) {
  const id = `PED-${Math.floor(1000 + Math.random() * 9000)}`;
  const now = new Date().toISOString();
  const txIdFinal = txid || `TX-${crypto.randomBytes(8).toString('hex').toUpperCase()}`;

  const stmt = db.prepare(`
    INSERT INTO pedidos (id, cliente_nome, whatsapp, valor, status, txid, created_at, updated_at)
    VALUES (?, ?, ?, ?, 'AGUARDANDO_PIX', ?, ?, ?)
  `);
  stmt.run(id, cliente_nome, whatsapp, Number(valor), txIdFinal, now, now);

  return buscarPedidoPorId(id);
}

function buscarPedidoPorId(id) {
  const stmt = db.prepare(`SELECT * FROM pedidos WHERE id = ?`);
  return stmt.get(id);
}

function buscarPedidoPorTxId(txid) {
  const stmt = db.prepare(`SELECT * FROM pedidos WHERE txid = ?`);
  return stmt.get(txid);
}

function atualizarStatusPedido(id, status) {
  const now = new Date().toISOString();
  const stmt = db.prepare(`
    UPDATE pedidos SET status = ?, updated_at = ? WHERE id = ?
  `);
  stmt.run(status, now, id);
  return buscarPedidoPorId(id);
}

function registrarPixTransacao({ end_to_end_id, txid, valor, chave_pix, status = 'CONCLUIDO', payload_raw = '' }) {
  const now = new Date().toISOString();
  const stmt = db.prepare(`
    INSERT INTO pix_transacoes (end_to_end_id, txid, valor, chave_pix, status, payload_raw, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);
  stmt.run(end_to_end_id, txid, Number(valor), chave_pix, status, JSON.stringify(payload_raw), now);
}

function gravarAuditLog({ tipo_evento, txid = null, whatsapp_id = null, dados = {} }) {
  const id = `WORM-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
  const now = new Date();
  const timestamp = now.toISOString();

  // FCR: janela de 7 dias corridos de First Contact Resolution (regra BSC)
  const fcrDeadline = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString();

  const dadosStr = JSON.stringify(dados);
  // Log imutável: cálculo de hash SHA-256 do payload
  const hash = crypto.createHash('sha256').update(`${id}|${timestamp}|${tipo_evento}|${dadosStr}`).digest('hex');

  const stmt = db.prepare(`
    INSERT INTO audit_trail_worm (id, timestamp, tipo_evento, txid, whatsapp_id, hash_sha256, dados_json, fcr_deadline)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);
  stmt.run(id, timestamp, tipo_evento, txid, whatsapp_id, hash, dadosStr, fcrDeadline);

  return { id, timestamp, tipo_evento, hash_sha256: hash, fcr_deadline: fcrDeadline };
}

function verificarIdempotencia(chave_hash) {
  const stmt = db.prepare(`SELECT * FROM idempotency_keys WHERE chave_hash = ?`);
  const registro = stmt.get(chave_hash);
  if (registro) {
    return JSON.parse(registro.response_json);
  }
  return null;
}

function salvarIdempotencia(chave_hash, endpoint, responseObj) {
  const now = new Date();
  const expira = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString();
  const stmt = db.prepare(`
    INSERT OR REPLACE INTO idempotency_keys (chave_hash, endpoint, response_json, created_at, expira_em)
    VALUES (?, ?, ?, ?, ?)
  `);
  stmt.run(chave_hash, endpoint, JSON.stringify(responseObj), now.toISOString(), expira);
}

function listarPedidos(limit = 20) {
  const stmt = db.prepare(`SELECT * FROM pedidos ORDER BY created_at DESC LIMIT ?`);
  return stmt.all(limit);
}

function listarAuditLogs(limit = 20) {
  const stmt = db.prepare(`SELECT * FROM audit_trail_worm ORDER BY timestamp DESC LIMIT ?`);
  return stmt.all(limit);
}

function listarPixTransacoes(limit = 20) {
  const stmt = db.prepare(`SELECT * FROM pix_transacoes ORDER BY created_at DESC LIMIT ?`);
  return stmt.all(limit);
}

function listarIdempotencia(limit = 20) {
  const stmt = db.prepare(`SELECT chave_hash, endpoint, created_at, expira_em FROM idempotency_keys ORDER BY created_at DESC LIMIT ?`);
  return stmt.all(limit);
}

function getDatabaseStats() {
  const countPedidos = db.prepare(`SELECT COUNT(*) as c FROM pedidos`).get().c;
  const countPix = db.prepare(`SELECT COUNT(*) as c FROM pix_transacoes`).get().c;
  const countAudit = db.prepare(`SELECT COUNT(*) as c FROM audit_trail_worm`).get().c;
  const countIdemp = db.prepare(`SELECT COUNT(*) as c FROM idempotency_keys`).get().c;

  return {
    provider: process.env.DATABASE_URL ? (process.env.DATABASE_URL.includes('supabase') ? 'Supabase (PostgreSQL)' : 'PostgreSQL') : 'SQLite Nativo (Node 22)',
    file: DB_FILE,
    connected: true,
    tables: {
      pedidos: countPedidos,
      pix_transacoes: countPix,
      audit_trail_worm: countAudit,
      idempotency_keys: countIdemp
    }
  };
}

module.exports = {
  db,
  criarPedido,
  buscarPedidoPorId,
  buscarPedidoPorTxId,
  atualizarStatusPedido,
  registrarPixTransacao,
  gravarAuditLog,
  verificarIdempotencia,
  salvarIdempotencia,
  listarPedidos,
  listarAuditLogs,
  listarPixTransacoes,
  listarIdempotencia,
  getDatabaseStats
};
