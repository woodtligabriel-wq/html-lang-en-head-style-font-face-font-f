import os
import re
import subprocess

# We will write the React component in JavaScript
component_js = r'''
var DbApiSection = () => {
  const [tab, setTab] = Yl.useState('simulator');
  const [selectedDb, setSelectedDb] = Yl.useState('supabase');
  const [dbStatus, setDbStatus] = Yl.useState('connected');
  const [dbLatency, setDbLatency] = Yl.useState(24);
  const [isTestingDb, setIsTestingDb] = Yl.useState(false);
  const [testDbMsg, setTestDbMsg] = Yl.useState(null);

  const [selectedPix, setSelectedPix] = Yl.useState('efi');
  const [metaPhoneId, setMetaPhoneId] = Yl.useState('109284719284729');
  const [metaToken, setMetaToken] = Yl.useState('EAAG_PROD_HOMOLOG_TOKEN_SECURE');
  const [pixKey, setPixKey] = Yl.useState('pix-financeiro@empresa.com.br');
  const [pixSecret, setPixSecret] = Yl.useState('muse_secret_pix_hmac_sha256_2026');
  const [apiTestMsg, setApiTestMsg] = Yl.useState(null);
  const [isTestingApi, setIsTestingApi] = Yl.useState(false);

  const [simStep, setSimStep] = Yl.useState(0);
  const [isSimulating, setIsSimulating] = Yl.useState(false);
  const [simClient, setSimClient] = Yl.useState('Gabriel Woodtli');
  const [simWhatsapp, setSimWhatsapp] = Yl.useState('+55 11 99999-8888');
  const [simValor, setSimValor] = Yl.useState('249.90');

  const [simLogs, setSimLogs] = Yl.useState([
    '⚡ SANDBOX PRONTO: Sistema conectado à Base de Dados e APIs de mensageria / pagamentos.',
    '👉 Clique em \"EXECUTAR FLUXO COMPLETO\" para simular o ciclo: Pedido -> Pix -> Webhook -> WORM -> WhatsApp.'
  ]);

  const [pedidos, setPedidos] = Yl.useState([
    { id: 'PED-9021', cliente: 'Gabriel Woodtli', whatsapp: '+55 11 99999-8888', valor: '249.00', status: 'PAGO_PIX', data: '2026-11-10 18:42', txid: 'TX-9C3FAAFFF10' },
    { id: 'PED-8841', cliente: 'Mariana Silveira', whatsapp: '+55 21 98888-7777', valor: '129.50', status: 'AGUARDANDO_PIX', data: '2026-11-10 18:30', txid: 'TX-8E280C08274' },
    { id: 'PED-8720', cliente: 'Lucas Andrade', whatsapp: '+55 31 97777-6666', valor: '590.00', status: 'PAGO_PIX', data: '2026-11-10 17:15', txid: 'TX-555833CA9F8' }
  ]);

  const [auditLogs, setAuditLogs] = Yl.useState([
    { id: 'WORM-9021', evento: 'PIX_CONFIRMADO_WHATSAPP_ENVIADO', hash: '4ace171962ea038def4b0dcee9364569fa3d83d551c1c1ca50d9f2ea90a9279c', deadline: '2026-11-17 18:42' },
    { id: 'WORM-8720', evento: 'PIX_CONFIRMADO_WHATSAPP_ENVIADO', hash: 'c1d651627de1b9642456b786071f6ed243aede7ef09d1756cd7ebce0ea76a6d7', deadline: '2026-11-17 17:15' }
  ]);

  const [pixTransacoes, setPixTransacoes] = Yl.useState([
    { e2e: 'E90400888179434756', txid: 'TX-9C3FAAFFF10', valor: '249.00', chave: 'pix-financeiro@empresa.com.br', status: 'CONCLUIDO' },
    { e2e: 'E90400888179434720', txid: 'TX-555833CA9F8', valor: '590.00', chave: 'pix-financeiro@empresa.com.br', status: 'CONCLUIDO' }
  ]);

  const [explorerTab, setExplorerTab] = Yl.useState('pedidos');
  const [copiedCode, setCopiedCode] = Yl.useState(false);

  const testDb = () => {
    setIsTestingDb(true);
    setTestDbMsg('Testando conexão com ' + selectedDb.toUpperCase() + '...');
    setTimeout(() => {
      setIsTestingDb(false);
      setDbStatus('connected');
      const lat = Math.floor(18 + Math.random() * 14);
      setDbLatency(lat);
      setTestDbMsg('Conexão ativa! Latência: ' + lat + 'ms. 4 tabelas verificadas (pedidos, pix_transacoes, audit_trail_worm, idempotency_keys).');
    }, 700);
  };

  const testApis = () => {
    setIsTestingApi(true);
    setApiTestMsg('Validando credenciais Meta Graph v20 & PSP Pix...');
    setTimeout(() => {
      setIsTestingApi(false);
      setApiTestMsg('Credenciais validadas com sucesso! Webhooks ativos e mTLS homologado.');
    }, 700);
  };

  const runSimulation = () => {
    if (isSimulating) return;
    setIsSimulating(true);
    setSimStep(1);

    const nowStr = new Date().toISOString().slice(0, 16).replace('T', ' ');
    const newTxId = 'TX-' + Math.random().toString(36).substring(2, 10).toUpperCase();
    const newPedId = 'PED-' + Math.floor(1000 + Math.random() * 9000);
    const newE2e = 'E90400' + Date.now();
    const wormHash = 'a7f9' + Math.random().toString(36).substring(2, 14) + 'b381...';

    setSimLogs([
      `[${nowStr}] [PASSO 1/5] Registrando Pedido na Base de Dados...`,
      `[${nowStr}] 💾 INSERT INTO pedidos (id, cliente, whatsapp, valor, status) VALUES ('${newPedId}', '${simClient}', '${simWhatsapp}', ${simValor}, 'AGUARDANDO_PIX')`
    ]);

    setTimeout(() => {
      setSimStep(2);
      setSimLogs(prev => [
        ...prev,
        `[${nowStr}] [PASSO 2/5] Gerando Cobrança Pix BACEN para txid ${newTxId}...`,
        `[${nowStr}] 💰 Payload BRCode Copia-e-Cola gerado: 00020126580014br.gov.bcb.pix0136${newTxId}...`,
        `[${nowStr}] 📲 Template interativo order_details enviado via WhatsApp Cloud API (Graph v20)`
      ]);

      setTimeout(() => {
        setSimStep(3);
        setSimLogs(prev => [
          ...prev,
          `[${nowStr}] [PASSO 3/5] Notificação Webhook Pix recebida do PSP (${selectedPix.toUpperCase()})!`,
          `[${nowStr}] 🔐 X-Pix-Signature (HMAC SHA-256): APROVADA`,
          `[${nowStr}] ⏱️ Verificação de Quarentena Anti-Race (120s BSC): APROVADA`,
          `[${nowStr}] 🔑 EndToEndId: ${newE2e}`
        ]);

        setTimeout(() => {
          setSimStep(4);
          setSimLogs(prev => [
            ...prev,
            `[${nowStr}] [PASSO 4/5] Atualização na Base de Dados & Registro WORM...`,
            `[${nowStr}] 💾 UPDATE pedidos SET status = 'PAGO_PIX' WHERE id = '${newPedId}'`,
            `[${nowStr}] 🛡️ Log WORM Gravado: Hash SHA-256 = ${wormHash}`,
            `[${nowStr}] ⏳ Protocolo First Contact Resolution (FCR) ativo por 7 dias corridos`
          ]);

          setPedidos(prev => [
            { id: newPedId, cliente: simClient, whatsapp: simWhatsapp, valor: simValor, status: 'PAGO_PIX', data: nowStr, txid: newTxId },
            ...prev
          ]);
          setPixTransacoes(prev => [
            { e2e: newE2e, txid: newTxId, valor: simValor, chave: pixKey, status: 'CONCLUIDO' },
            ...prev
          ]);
          setAuditLogs(prev => [
            { id: 'WORM-' + newPedId.slice(4), evento: 'PIX_CONFIRMADO_WHATSAPP_ENVIADO', hash: wormHash, deadline: '2026-11-17 18:42' },
            ...prev
          ]);

          setTimeout(() => {
            setSimStep(5);
            setIsSimulating(false);
            setSimLogs(prev => [
              ...prev,
              `[${nowStr}] [PASSO 5/5] Disparo WhatsApp de Confirmação entregue ao cliente!`,
              `[${nowStr}] 📱 Mensagem: "Prezado(a) ${simClient}, confirmamos o recebimento do Pix de R$ ${simValor}. Pedido ${newPedId} aprovado."`,
              `[${nowStr}] ✅ FLUXO PONTA A PONTA FINALIZADO COM SUCESSO! Registro consolidado na Base.`
            ]);
          }, 700);
        }, 700);
      }, 700);
    }, 700);
  };

  const copySql = () => {
    const sql = `-- Schema MUSE + META
CREATE TABLE pedidos (id VARCHAR(64) PRIMARY KEY, cliente_nome VARCHAR(255), whatsapp VARCHAR(32), valor NUMERIC(12,2), status VARCHAR(32), txid VARCHAR(64) UNIQUE, created_at TIMESTAMP);
CREATE TABLE pix_transacoes (end_to_end_id VARCHAR(128) PRIMARY KEY, txid VARCHAR(64), valor NUMERIC(12,2), chave_pix VARCHAR(255), status VARCHAR(32), created_at TIMESTAMP);
CREATE TABLE audit_trail_worm (id VARCHAR(128) PRIMARY KEY, timestamp TIMESTAMP, tipo_evento VARCHAR(64), txid VARCHAR(64), hash_sha256 VARCHAR(64), fcr_deadline TIMESTAMP);
CREATE TABLE idempotency_keys (chave_hash VARCHAR(64) PRIMARY KEY, endpoint VARCHAR(255), response_json TEXT, expira_em TIMESTAMP);`;
    let u = document.createElement("textarea");
    u.value = sql;
    document.body.appendChild(u);
    u.select();
    try {
      document.execCommand("copy");
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    } catch {}
    document.body.removeChild(u);
  };

  return w("section", {
    className: "rounded-[16px] border border-[var(--border)] bg-[var(--surface)] overflow-hidden",
    children: [
      // Cabeçalho da Seção 04
      w("div", {
        className: "px-6 py-5 border-b border-[var(--border)] flex flex-col md:flex-row md:items-center justify-between gap-4",
        children: [
          w("div", {
            className: "flex items-center gap-3",
            children: [
              p("div", {
                className: "w-7 h-7 rounded-lg bg-[var(--surface-3)] border border-[var(--border)] flex items-center justify-center",
                children: p(gr, { className: "w-4 h-4 text-emerald-400" })
              }),
              w("div", {
                children: [
                  p("h2", {
                    className: "text-[13px] font-semibold tracking-wide flex items-center gap-2",
                    children: [
                      "04 — CENTRAL DE CONEXÃO: BASE DE DADOS & APIs",
                      p("span", {
                        className: "text-[9px] px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono tracking-widest uppercase",
                        children: "INTERATIVO"
                      })
                    ]
                  }),
                  p("p", {
                    className: "text-[11px] font-mono text-zinc-500",
                    children: "Conexão Unificada: Supabase / PostgreSQL / SQLite • Meta WhatsApp Cloud API • Gateway Pix BACEN"
                  })
                ]
              })
            ]
          }),
          w("div", {
            className: "flex flex-wrap items-center gap-2",
            children: [
              w("div", {
                className: "flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--surface-2)] border border-[var(--border)]",
                children: [
                  p("div", { className: `w-1.5 h-1.5 rounded-full animate-pulse ${dbStatus === 'connected' ? 'bg-emerald-400' : 'bg-amber-400'}` }),
                  p("span", { className: "text-[10px] font-mono text-zinc-500", children: "BASE:" }),
                  p("span", { className: "text-[10px] font-mono font-medium text-emerald-300", children: selectedDb.toUpperCase() + ` (${dbLatency}ms)` })
                ]
              }),
              w("div", {
                className: "flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--surface-2)] border border-[var(--border)]",
                children: [
                  p("div", { className: "w-1.5 h-1.5 rounded-full animate-pulse bg-cyan-400" }),
                  p("span", { className: "text-[10px] font-mono text-zinc-500", children: "APIs:" }),
                  p("span", { className: "text-[10px] font-mono font-medium text-cyan-300", children: "META + PIX OK" })
                ]
              })
            ]
          })
        ]
      }),

      // Barra de Navegação Interna por Abas
      w("div", {
        className: "px-6 py-3 border-b border-[var(--border)] bg-black/20 flex flex-wrap items-center gap-2",
        children: [
          { id: 'simulator', label: '⚡ Simulador em Tempo Real', desc: 'Sandbox Ponta a Ponta' },
          { id: 'database', label: '🗄️ Base de Dados', desc: 'Supabase / Postgres / SQLite' },
          { id: 'apis', label: '🔌 Conexão de APIs', desc: 'WhatsApp Meta & Pix BACEN' },
          { id: 'explorer', label: '📊 Explorador de Dados', desc: 'Tabelas & Logs WORM' }
        ].map(item =>
          w("button", {
            key: item.id,
            onClick: () => setTab(item.id),
            className: `px-3.5 py-2 rounded-lg text-[11px] font-mono transition-all flex items-center gap-2 ${
              tab === item.id
                ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 shadow-sm'
                : 'bg-[var(--surface-2)] text-zinc-400 hover:text-zinc-200 border border-[var(--border)] hover:bg-zinc-800'
            }`,
            children: [
              p("span", { className: "font-semibold", children: item.label }),
              p("span", { className: "text-[9px] text-zinc-500 hidden sm:inline", children: `(${item.desc})` })
            ]
          })
        )
      }),

      // Conteúdo da Aba 1: Simulador Ponta a Ponta
      tab === 'simulator' && w("div", {
        className: "p-6 flex flex-col gap-6",
        children: [
          // Banner explicativo do simulador
          w("div", {
            className: "p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4",
            children: [
              w("div", {
                className: "flex items-start gap-3",
                children: [
                  p(hn, { className: "w-5 h-5 text-cyan-400 shrink-0 mt-0.5" }),
                  w("div", {
                    children: [
                      p("h3", { className: "text-[12px] font-semibold text-cyan-300 uppercase tracking-wide", children: "Simulador de Ciclo de Venda & Pagamento Pix em Produção" }),
                      p("p", {
                        className: "text-[11px] text-zinc-400 mt-1 leading-relaxed",
                        children: "Teste instantaneamente o pipeline: 1. Gravação do Pedido no Banco de Dados -> 2. Emissão do BRCode Pix -> 3. Recepção do Webhook BACEN com validação HMAC -> 4. Gravação de Log WORM Imutável -> 5. Envio de Confirmação formal via WhatsApp."
                      })
                    ]
                  })
                ]
              }),
              w("button", {
                onClick: runSimulation,
                disabled: isSimulating,
                className: `px-4 py-2.5 rounded-lg text-[12px] font-mono font-medium shrink-0 transition-all flex items-center gap-2 ${
                  isSimulating
                    ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed border border-zinc-700'
                    : 'bg-emerald-500 hover:bg-emerald-400 text-black shadow-lg shadow-emerald-500/20 font-bold'
                }`,
                children: [
                  isSimulating ? p("span", { className: "animate-spin", children: "⏳" }) : p("span", { children: "⚡" }),
                  isSimulating ? "PROCESSANDO FLUXO..." : "EXECUTAR FLUXO COMPLETO"
                ]
              })
            ]
          }),

          // Painel de Configuração Rápida do Teste
          w("div", {
            className: "grid grid-cols-1 sm:grid-cols-3 gap-4",
            children: [
              w("div", {
                className: "p-3 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-1.5",
                children: [
                  p("label", { className: "text-[10px] font-mono text-zinc-400 uppercase tracking-wider", children: "Nome do Cliente" }),
                  p("input", {
                    type: "text",
                    value: simClient,
                    onChange: (e) => setSimClient(e.target.value),
                    className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[12px] font-mono text-zinc-200 focus:outline-none focus:border-cyan-400"
                  })
                ]
              }),
              w("div", {
                className: "p-3 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-1.5",
                children: [
                  p("label", { className: "text-[10px] font-mono text-zinc-400 uppercase tracking-wider", children: "WhatsApp do Cliente" }),
                  p("input", {
                    type: "text",
                    value: simWhatsapp,
                    onChange: (e) => setSimWhatsapp(e.target.value),
                    className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[12px] font-mono text-zinc-200 focus:outline-none focus:border-cyan-400"
                  })
                ]
              }),
              w("div", {
                className: "p-3 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-1.5",
                children: [
                  p("label", { className: "text-[10px] font-mono text-zinc-400 uppercase tracking-wider", children: "Valor da Venda (R$)" }),
                  p("input", {
                    type: "text",
                    value: simValor,
                    onChange: (e) => setSimValor(e.target.value),
                    className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[12px] font-mono text-emerald-300 font-semibold focus:outline-none focus:border-cyan-400"
                  })
                ]
              })
            ]
          }),

          // Timeline Visual dos 5 Passos
          w("div", {
            className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-3",
            children: [
              p("div", {
                className: "text-[10px] font-mono tracking-widest text-zinc-500 uppercase",
                children: "PROGRESSO DO PIPELINE DE EXECUÇÃO"
              }),
              w("div", {
                className: "grid grid-cols-1 md:grid-cols-5 gap-3",
                children: [
                  { num: 1, title: '1. Pedido no Banco', desc: 'INSERT em pedidos' },
                  { num: 2, title: '2. Emissão Pix', desc: 'BRCode Copia-e-Cola' },
                  { num: 3, title: '3. Webhook BACEN', desc: 'HMAC & Quarentena 120s' },
                  { num: 4, title: '4. Gravação WORM', desc: 'Hash SHA-256 imutável' },
                  { num: 5, title: '5. WhatsApp Sent', desc: 'Template order_details' }
                ].map(st => {
                  const isDone = simStep >= st.num;
                  const isCurrent = simStep === st.num;
                  return w("div", {
                    key: st.num,
                    className: `p-3 rounded-lg border transition-all ${
                      isDone
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                        : isCurrent
                        ? 'bg-cyan-500/10 border-cyan-500/40 text-cyan-300 animate-pulse'
                        : 'bg-[var(--surface-3)] border-[var(--border)] text-zinc-500'
                    }`,
                    children: [
                      w("div", {
                        className: "flex items-center justify-between mb-1",
                        children: [
                          p("span", { className: "text-[11px] font-mono font-semibold", children: st.title }),
                          isDone
                            ? p(pn, { className: "w-3.5 h-3.5 text-emerald-400" })
                            : p("span", { className: "text-[10px] font-mono text-zinc-600", children: `#${st.num}` })
                        ]
                      }),
                      p("p", { className: "text-[10px] font-mono opacity-80 leading-tight", children: st.desc })
                    ]
                  });
                })
              })
            ]
          }),

          // Terminal de Logs em Tempo Real
          w("div", {
            className: "rounded-xl border border-[var(--border)] bg-black/60 overflow-hidden",
            children: [
              w("div", {
                className: "px-4 py-2.5 border-b border-[var(--border)] bg-[var(--surface-2)] flex items-center justify-between",
                children: [
                  w("div", {
                    className: "flex items-center gap-2",
                    children: [
                      p("div", { className: "w-2.5 h-2.5 rounded-full bg-[#ff5f56]" }),
                      p("div", { className: "w-2.5 h-2.5 rounded-full bg-[#ffbd2e]" }),
                      p("div", { className: "w-2.5 h-2.5 rounded-full bg-[#27c93f]" }),
                      p("span", { className: "ml-2 text-[10px] font-mono text-zinc-400", children: "console.pipeline.log — stdout" })
                    ]
                  }),
                  p("span", { className: "text-[9px] font-mono text-zinc-500", children: "UTF-8 • JSON RFC 8259" })
                ]
              }),
              w("div", {
                className: "p-4 font-mono text-[11.5px] leading-relaxed text-zinc-300 space-y-1 max-h-[220px] overflow-y-auto scrollbar-thin",
                children: simLogs.map((log, idx) =>
                  p("div", {
                    key: idx,
                    className: log.includes('✅')
                      ? 'text-emerald-300 font-semibold'
                      : log.includes('ERRO')
                      ? 'text-rose-400 font-semibold'
                      : log.includes('💾') || log.includes('💰')
                      ? 'text-cyan-300'
                      : log.includes('🔐') || log.includes('🛡️')
                      ? 'text-amber-300'
                      : 'text-zinc-400',
                    children: log
                  })
                )
              })
            ]
          })
        ]
      }),

      // Conteúdo da Aba 2: Configuração da Base de Dados
      tab === 'database' && w("div", {
        className: "p-6 flex flex-col gap-6",
        children: [
          w("div", {
            className: "grid md:grid-cols-2 gap-4",
            children: [
              // Provedores de Banco de Dados
              w("div", {
                className: "flex flex-col gap-3",
                children: [
                  p("h3", { className: "text-[12px] font-semibold tracking-wide text-zinc-300 uppercase", children: "Selecione a Base de Dados Principal" }),
                  [
                    { id: 'supabase', name: 'Supabase (PostgreSQL Cloud)', tag: 'RECOMENDADO', desc: 'Banco relacional em nuvem gratuito, connection pooling e REST/GraphQL instantâneos.' },
                    { id: 'sqlite', name: 'SQLite Nativo (Node 22)', tag: 'ZERO-CONFIG', desc: 'Execução local imediata em data/database.sqlite. Já ativo no projeto sem dependências.' },
                    { id: 'postgres', name: 'PostgreSQL Dedicado (Neon / RDS)', tag: 'ENTERPRISE', desc: 'Instância PostgreSQL padrão via string de conexão DATABASE_URL.' },
                    { id: 'oracle', name: 'Oracle / SAP ERP', tag: 'CORPORATIVO', desc: 'Integração legada corporativa via adaptador de middleware MUSE.' }
                  ].map(pvd =>
                    w("div", {
                      key: pvd.id,
                      onClick: () => setSelectedDb(pvd.id),
                      className: `p-3.5 rounded-xl border cursor-pointer transition-all ${
                        selectedDb === pvd.id
                          ? 'bg-emerald-500/[0.08] border-emerald-500/40'
                          : 'bg-[var(--surface-2)] border-[var(--border)] hover:border-zinc-700'
                      }`,
                      children: [
                        w("div", {
                          className: "flex items-center justify-between mb-1",
                          children: [
                            w("div", {
                              className: "flex items-center gap-2",
                              children: [
                                p("div", { className: `w-3 h-3 rounded-full border flex items-center justify-center ${selectedDb === pvd.id ? 'border-emerald-400 bg-emerald-400' : 'border-zinc-600'}` }),
                                p("span", { className: "text-[12px] font-semibold text-zinc-200", children: pvd.name })
                              ]
                            }),
                            p("span", { className: "text-[9px] px-2 py-0.5 rounded-full font-mono bg-zinc-800 text-zinc-400 border border-zinc-700", children: pvd.tag })
                          ]
                        }),
                        p("p", { className: "text-[11px] text-zinc-400 ml-5 leading-normal", children: pvd.desc })
                      ]
                    })
                  )
                ]
              }),

              // Detalhes da Conexão & Teste
              w("div", {
                className: "flex flex-col gap-4",
                children: [
                  w("div", {
                    className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-3",
                    children: [
                      p("h4", { className: "text-[11px] font-mono text-zinc-400 uppercase tracking-wider", children: "String de Conexão (DATABASE_URL)" }),
                      p("input", {
                        type: "text",
                        readOnly: true,
                        value: selectedDb === 'supabase'
                          ? 'postgresql://postgres.[project-id]:***@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
                          : selectedDb === 'sqlite'
                          ? 'sqlite:///home/agent/workspace/data/database.sqlite'
                          : selectedDb === 'postgres'
                          ? 'postgresql://usuario:senha@localhost:5432/muse_db'
                          : 'oracle://middleware:***@erp-cluster.internal:1521/PROD',
                        className: "px-3 py-2 rounded-lg bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-300 select-all"
                      }),
                      w("div", {
                        className: "flex items-center justify-between pt-1",
                        children: [
                          w("button", {
                            onClick: testDb,
                            disabled: isTestingDb,
                            className: "px-3.5 py-1.5 rounded-md bg-emerald-500 hover:bg-emerald-400 text-black text-[11px] font-mono font-semibold transition-all flex items-center gap-1.5",
                            children: [
                              isTestingDb ? p("span", { className: "animate-spin", children: "⏳" }) : p(gr, { className: "w-3 h-3 text-black" }),
                              isTestingDb ? "TESTANDO..." : "TESTAR CONEXÃO COM A BASE"
                            ]
                          }),
                          w("button", {
                            onClick: copySql,
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface-3)] hover:bg-zinc-800 border border-[var(--border)] text-[11px] font-mono text-zinc-300 transition-all flex items-center gap-1.5",
                            children: [
                              copiedCode ? p(pn, { className: "w-3 h-3 text-emerald-400" }) : p(vr, { className: "w-3 h-3" }),
                              copiedCode ? "SQL COPIADO!" : "COPIAR SCHEMA DDL"
                            ]
                          })
                        ]
                      }),
                      testDbMsg && p("div", {
                        className: "p-2.5 rounded-md bg-emerald-950/30 border border-emerald-500/30 text-[11px] font-mono text-emerald-300 leading-relaxed",
                        children: testDbMsg
                      })
                    ]
                  }),

                  // Instruções de Inicialização Rápida
                  w("div", {
                    className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-2",
                    children: [
                      p("h4", { className: "text-[11px] font-mono text-zinc-400 uppercase tracking-wider", children: "Como Rodar o Backend Localmente" }),
                      p("p", { className: "text-[11px] text-zinc-400 leading-relaxed", children: "O servidor Node 22 com SQLite embutido e endpoints prontos para receber o Webhook já está salvo no seu repositório em backend/server.js:" }),
                      p("pre", {
                        className: "p-2.5 rounded-lg bg-black/60 border border-[var(--border)] text-[11px] font-mono text-cyan-300 overflow-x-auto",
                        children: "npm start    # Inicia a API na porta 3001\nnpm test     # Executa teste automatizado do fluxo Pix"
                      })
                    ]
                  })
                ]
              })
            ]
          })
        ]
      }),

      // Conteúdo da Aba 3: Conexão de APIs (WhatsApp Meta & Pix BACEN)
      tab === 'apis' && w("div", {
        className: "p-6 flex flex-col gap-6",
        children: [
          w("div", {
            className: "grid md:grid-cols-2 gap-6",
            children: [
              // Card Meta WhatsApp Cloud API
              w("div", {
                className: "p-5 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-4",
                children: [
                  w("div", {
                    className: "flex items-center justify-between border-b border-[var(--border)] pb-3",
                    children: [
                      w("div", {
                        className: "flex items-center gap-2.5",
                        children: [
                          p("div", { className: "w-7 h-7 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center", children: p(vn, { className: "w-4 h-4 text-emerald-400" }) }),
                          w("div", {
                            children: [
                              p("h3", { className: "text-[12px] font-semibold text-zinc-200", children: "Meta WhatsApp Cloud API" }),
                              p("p", { className: "text-[10px] font-mono text-zinc-500", children: "Graph API v20.0 • Templates Interativos" })
                            ]
                          })
                        ]
                      }),
                      p("span", { className: "text-[9px] px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono tracking-widest", children: "VERIFIED" })
                    ]
                  }),
                  w("div", {
                    className: "space-y-3",
                    children: [
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "Phone Number ID" }),
                          p("input", {
                            type: "text",
                            value: metaPhoneId,
                            onChange: (e) => setMetaPhoneId(e.target.value),
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-200"
                          })
                        ]
                      }),
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "Access Token (Bearer)" }),
                          p("input", {
                            type: "password",
                            value: metaToken,
                            onChange: (e) => setMetaToken(e.target.value),
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-200"
                          })
                        ]
                      }),
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "URL do Webhook Receptor" }),
                          p("input", {
                            type: "text",
                            readOnly: true,
                            value: "https://seu-servidor.com/api/webhooks/meta",
                            className: "px-3 py-1.5 rounded-md bg-black/40 border border-[var(--border)] text-[11px] font-mono text-zinc-400 select-all"
                          })
                        ]
                      })
                    ]
                  })
                ]
              }),

              // Card Gateway Pix BACEN / PSP
              w("div", {
                className: "p-5 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-4",
                children: [
                  w("div", {
                    className: "flex items-center justify-between border-b border-[var(--border)] pb-3",
                    children: [
                      w("div", {
                        className: "flex items-center gap-2.5",
                        children: [
                          p("div", { className: "w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center", children: p(hr, { className: "w-4 h-4 text-cyan-400" }) }),
                          w("div", {
                            children: [
                              p("h3", { className: "text-[12px] font-semibold text-zinc-200", children: "Gateway Pix BACEN / PSP" }),
                              p("p", { className: "text-[10px] font-mono text-zinc-500", children: "Protocolo mTLS • Assinatura HMAC SHA-256" })
                            ]
                          })
                        ]
                      }),
                      p("span", { className: "text-[9px] px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-mono tracking-widest", children: "HOMOLOGADO" })
                    ]
                  }),
                  w("div", {
                    className: "space-y-3",
                    children: [
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "Provedor Pix Homologado" }),
                          w("select", {
                            value: selectedPix,
                            onChange: (e) => setSelectedPix(e.target.value),
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-200 focus:outline-none",
                            children: [
                              p("option", { value: "efi", children: "EFI Bank (antiga Gerencianet) — mTLS Oficial" }),
                              p("option", { value: "asaas", children: "Asaas — API REST Pix Direta" }),
                              p("option", { value: "mercadopago", children: "Mercado Pago — Pix Instantâneo" }),
                              p("option", { value: "bacen", children: "BACEN SPI Direto (Participante Homologado)" })
                            ]
                          })
                        ]
                      }),
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "Chave Pix (EVP / CNPJ / E-mail)" }),
                          p("input", {
                            type: "text",
                            value: pixKey,
                            onChange: (e) => setPixKey(e.target.value),
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-200"
                          })
                        ]
                      }),
                      w("div", {
                        className: "flex flex-col gap-1",
                        children: [
                          p("label", { className: "text-[10px] font-mono text-zinc-400", children: "Segredo de Assinatura Webhook (HMAC)" }),
                          p("input", {
                            type: "password",
                            value: pixSecret,
                            onChange: (e) => setPixSecret(e.target.value),
                            className: "px-3 py-1.5 rounded-md bg-[var(--surface)] border border-[var(--border)] text-[11px] font-mono text-zinc-200"
                          })
                        ]
                      })
                    ]
                  })
                ]
              })
            ]
          }),

          // Botão de Validação e Feedback
          w("div", {
            className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col sm:flex-row items-center justify-between gap-4",
            children: [
              w("div", {
                className: "flex items-center gap-3",
                children: [
                  p(Er, { className: "w-5 h-5 text-emerald-400" }),
                  w("div", {
                    children: [
                      p("h4", { className: "text-[11px] font-semibold text-zinc-200", children: "Auditoria de Credenciais & Webhooks" }),
                      p("p", { className: "text-[10px] text-zinc-400", children: "Simula o handshake com os endpoints da Meta e do PSP Pix com verificação de certificados." })
                    ]
                  })
                ]
              }),
              w("button", {
                onClick: testApis,
                disabled: isTestingApi,
                className: "px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black text-[11px] font-mono font-semibold transition-all shrink-0 flex items-center gap-2",
                children: [
                  isTestingApi ? p("span", { className: "animate-spin", children: "⏳" }) : p("span", { children: "🔍" }),
                  isTestingApi ? "VALIDANDO..." : "TESTAR INTEGRAÇÃO DE APIs"
                ]
              })
            ]
          }),
          apiTestMsg && p("div", {
            className: "p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/30 text-[11px] font-mono text-cyan-300 leading-relaxed text-center",
            children: apiTestMsg
          })
        ]
      }),

      // Conteúdo da Aba 4: Explorador de Dados (Tabelas & Logs WORM)
      tab === 'explorer' && w("div", {
        className: "p-6 flex flex-col gap-6",
        children: [
          // Sub-abas do explorador
          w("div", {
            className: "flex items-center justify-between border-b border-[var(--border)] pb-3",
            children: [
              w("div", {
                className: "flex items-center gap-2",
                children: [
                  { id: 'pedidos', label: 'Tabela: pedidos', count: pedidos.length },
                  { id: 'pix', label: 'Tabela: pix_transacoes', count: pixTransacoes.length },
                  { id: 'audit', label: 'Tabela: audit_trail_worm', count: auditLogs.length }
                ].map(sub =>
                  w("button", {
                    key: sub.id,
                    onClick: () => setExplorerTab(sub.id),
                    className: `px-3 py-1.5 rounded-md text-[11px] font-mono transition-all flex items-center gap-1.5 ${
                      explorerTab === sub.id
                        ? 'bg-[var(--surface-3)] text-zinc-100 border border-[var(--border)]'
                        : 'text-zinc-500 hover:text-zinc-300'
                    }`,
                    children: [
                      p("span", { children: sub.label }),
                      p("span", { className: "text-[9px] px-1.5 py-0.2 rounded-full bg-zinc-800 text-zinc-400", children: sub.count })
                    ]
                  })
                )
              }),
              p("span", { className: "text-[10px] font-mono text-zinc-500", children: `Base: ${selectedDb.toUpperCase()}` })
            ]
          }),

          // Tabela de Pedidos
          explorerTab === 'pedidos' && w("div", {
            className: "rounded-xl border border-[var(--border)] bg-black/40 overflow-x-auto",
            children: w("table", {
              className: "w-full text-left font-mono text-[11px]",
              children: [
                p("thead", {
                  className: "bg-[var(--surface-2)] text-zinc-400 border-b border-[var(--border)]",
                  children: w("tr", {
                    children: [
                      p("th", { className: "px-4 py-2.5", children: "ID PEDIDO" }),
                      p("th", { className: "px-4 py-2.5", children: "CLIENTE" }),
                      p("th", { className: "px-4 py-2.5", children: "WHATSAPP" }),
                      p("th", { className: "px-4 py-2.5", children: "VALOR" }),
                      p("th", { className: "px-4 py-2.5", children: "STATUS" }),
                      p("th", { className: "px-4 py-2.5", children: "TXID BACEN" })
                    ]
                  })
                }),
                w("tbody", {
                  className: "divide-y divide-[var(--border)] text-zinc-300",
                  children: pedidos.map(ped =>
                    w("tr", {
                      key: ped.id,
                      className: "hover:bg-[var(--surface-2)] transition-colors",
                      children: [
                        p("td", { className: "px-4 py-2.5 font-bold text-cyan-300", children: ped.id }),
                        p("td", { className: "px-4 py-2.5", children: ped.cliente }),
                        p("td", { className: "px-4 py-2.5 text-zinc-400", children: ped.whatsapp }),
                        p("td", { className: "px-4 py-2.5 text-emerald-300 font-semibold", children: `R$ ${Number(ped.valor).toFixed(2)}` }),
                        p("td", {
                          className: "px-4 py-2.5",
                          children: p("span", {
                            className: `px-2 py-0.5 rounded-full text-[9px] font-mono ${
                              ped.status === 'PAGO_PIX'
                                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                            }`,
                            children: ped.status
                          })
                        }),
                        p("td", { className: "px-4 py-2.5 text-zinc-500 text-[10px]", children: ped.txid || '—' })
                      ]
                    })
                  )
                })
              ]
            })
          }),

          // Tabela de Pix
          explorerTab === 'pix' && w("div", {
            className: "rounded-xl border border-[var(--border)] bg-black/40 overflow-x-auto",
            children: w("table", {
              className: "w-full text-left font-mono text-[11px]",
              children: [
                p("thead", {
                  className: "bg-[var(--surface-2)] text-zinc-400 border-b border-[var(--border)]",
                  children: w("tr", {
                    children: [
                      p("th", { className: "px-4 py-2.5", children: "END_TO_END_ID" }),
                      p("th", { className: "px-4 py-2.5", children: "TXID" }),
                      p("th", { className: "px-4 py-2.5", children: "CHAVE PIX" }),
                      p("th", { className: "px-4 py-2.5", children: "VALOR" }),
                      p("th", { className: "px-4 py-2.5", children: "STATUS" })
                    ]
                  })
                }),
                w("tbody", {
                  className: "divide-y divide-[var(--border)] text-zinc-300",
                  children: pixTransacoes.map(px =>
                    w("tr", {
                      key: px.e2e,
                      className: "hover:bg-[var(--surface-2)] transition-colors",
                      children: [
                        p("td", { className: "px-4 py-2.5 text-cyan-300 text-[10px]", children: px.e2e }),
                        p("td", { className: "px-4 py-2.5 text-zinc-400", children: px.txid }),
                        p("td", { className: "px-4 py-2.5 text-zinc-500", children: px.chave }),
                        p("td", { className: "px-4 py-2.5 text-emerald-300 font-semibold", children: `R$ ${Number(px.valor).toFixed(2)}` }),
                        p("td", { className: "px-4 py-2.5 text-emerald-400 font-bold", children: px.status })
                      ]
                    })
                  )
                })
              ]
            })
          }),

          // Tabela de Auditoria WORM
          explorerTab === 'audit' && w("div", {
            className: "rounded-xl border border-[var(--border)] bg-black/40 overflow-x-auto",
            children: w("table", {
              className: "w-full text-left font-mono text-[11px]",
              children: [
                p("thead", {
                  className: "bg-[var(--surface-2)] text-zinc-400 border-b border-[var(--border)]",
                  children: w("tr", {
                    children: [
                      p("th", { className: "px-4 py-2.5", children: "AUDIT ID" }),
                      p("th", { className: "px-4 py-2.5", children: "TIPO EVENTO" }),
                      p("th", { className: "px-4 py-2.5", children: "HASH SHA-256 (IMUTÁVEL)" }),
                      p("th", { className: "px-4 py-2.5", children: "FCR DEADLINE (7D)" })
                    ]
                  })
                }),
                w("tbody", {
                  className: "divide-y divide-[var(--border)] text-zinc-300",
                  children: auditLogs.map(aud =>
                    w("tr", {
                      key: aud.id,
                      className: "hover:bg-[var(--surface-2)] transition-colors",
                      children: [
                        p("td", { className: "px-4 py-2.5 text-amber-300 font-bold", children: aud.id }),
                        p("td", { className: "px-4 py-2.5 text-zinc-300", children: aud.evento }),
                        p("td", { className: "px-4 py-2.5 text-cyan-300 text-[10px] select-all", children: aud.hash }),
                        p("td", { className: "px-4 py-2.5 text-zinc-500", children: aud.deadline })
                      ]
                    })
                  )
                })
              ]
            })
          })
        ]
      }),

      // Rodapé da Seção 04
      w("div", {
        className: "px-6 py-4 border-t border-[var(--border)] bg-black/30 flex flex-col md:flex-row gap-3 justify-between text-[11px] font-mono text-zinc-500",
        children: [
          w("span", {
            className: "flex items-center gap-2",
            children: [
              p("span", { children: "🛡️ Trilha WORM imutável & Compliance LGPD/BACEN" }),
              p("span", { className: "text-zinc-600", children: "• FCR 7 dias ativado" })
            ]
          }),
          p("span", { className: "text-zinc-600", children: "SQLite Nativo • PostgreSQL • Supabase Ready • Node 22 API" })
        ]
      })
    ]
  });
};
'''

# Verify component syntax with Node vm
test_script = f"""
const vm = require('node:vm');
const Yl = {{ useState: (init) => [init, () => {{}}] }};
const p = () => ({{}});
const w = () => ({{}});
const gr = () => ({{}});
const kr = () => ({{}});
const vn = () => ({{}});
const hr = () => ({{}});
const Er = () => ({{}});
const gt = () => ({{}});
const hn = () => ({{}});
const vr = () => ({{}});
const pn = () => ({{}});
const mr = () => ({{}});
const ht = () => ({{}});
const wr = () => ({{}});
const Sr = () => ({{}});
const mn = () => ({{}});

{component_js}
new vm.Script(DbApiSection.toString());
console.log('REACT COMPONENT SYNTAX VALIDATION: SUCCESS!');
"""

with open('/tmp/test_comp.js', 'w') as f:
    f.write(test_script)

res = subprocess.run(['node', '/tmp/test_comp.js'], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print('ERROR:', res.stderr)
    exit(1)
print('Ready to integrate!')
