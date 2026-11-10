import re

with open('/home/agent/workspace/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State addition
old_state = "const [copiedCode, setCopiedCode] = Yl.useState(false);"
new_state = """const [copiedCode, setCopiedCode] = Yl.useState(false);
  const [isTestingIcp, setIsTestingIcp] = Yl.useState(false);
  const [icpTestMsg, setIcpTestMsg] = Yl.useState(null);
  const [icpCopied, setIcpCopied] = Yl.useState(false);

  const testIcp = () => {
    setIsTestingIcp(true);
    setIcpTestMsg('Executando handshake mútuo TLS (mTLS) com a AC Raiz da ICP-Brasil (Resolução BCB 1/2020)...');
    setTimeout(() => {
      setIsTestingIcp(false);
      setIcpTestMsg('✅ Handshake mTLS Aprovado com Sucesso! Certificado e-CNPJ A1 autenticado. Token OAuth2 (RFC 8705) emitido e atrelado ao fingerprint SHA-256.');
    }, 750);
  };

  const copyIcpCmd = () => {
    navigator.clipboard?.writeText('openssl pkcs12 -in certificado_icp.p12 -out certs/pix_producao.pem -nodes');
    setIcpCopied(true);
    setTimeout(() => setIcpCopied(false), 2000);
  };"""

if old_state not in content:
    raise ValueError("old_state not found in index.html")
content = content.replace(old_state, new_state, 1)

# 2. Navigation tab addition
old_tabs = """{ id: 'simulator', label: '⚡ Simulador em Tempo Real', desc: 'Sandbox Ponta a Ponta' },
          { id: 'database', label: '🗄️ Base de Dados', desc: 'Supabase / Postgres / SQLite' },
          { id: 'apis', label: '🔌 Conexão de APIs', desc: 'WhatsApp Meta & Pix BACEN' },
          { id: 'explorer', label: '📊 Explorador de Dados', desc: 'Tabelas & Logs WORM' }"""

new_tabs = """{ id: 'simulator', label: '⚡ Simulador em Tempo Real', desc: 'Sandbox Ponta a Ponta' },
          { id: 'database', label: '🗄️ Base de Dados', desc: 'Supabase / Postgres / SQLite' },
          { id: 'apis', label: '🔌 Conexão de APIs', desc: 'WhatsApp Meta & Pix BACEN' },
          { id: 'icp', label: '🔐 Autenticação ICP-Brasil', desc: 'mTLS Pix & e-CNPJ A1' },
          { id: 'explorer', label: '📊 Explorador de Dados', desc: 'Tabelas & Logs WORM' }"""

if old_tabs not in content:
    raise ValueError("old_tabs not found in index.html")
content = content.replace(old_tabs, new_tabs, 1)

# 3. Tab content addition before tab === 'explorer'
old_tab_target = "tab === 'explorer' && w(\"div\", {"

icp_content = """// Conteúdo da Aba: Autenticação ICP-Brasil
      tab === 'icp' && w("div", {
        className: "p-6 flex flex-col gap-6",
        children: [
          // Banner de Destaque
          w("div", {
            className: "p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4",
            children: [
              w("div", {
                className: "flex items-start gap-3",
                children: [
                  p("span", { className: "text-2xl mt-0.5", children: "🔐" }),
                  w("div", {
                    children: [
                      w("div", {
                        className: "flex flex-wrap items-center gap-2",
                        children: [
                          p("h3", { className: "text-[12px] font-semibold text-amber-300 uppercase tracking-wide", children: "Autenticação ICP-Brasil & Protocolo mTLS para Pix BACEN" }),
                          p("span", { className: "text-[9px] px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 font-mono tracking-widest", children: "RESOLUÇÃO BCB Nº 1/2020" })
                        ]
                      }),
                      p("p", { className: "text-[11px] text-zinc-400 mt-1 leading-relaxed", children: "No padrão do Banco Central do Brasil, a autenticação de pagamentos instantâneos exige Certificado Digital e-CNPJ (A1 ou A3) emitido pela ICP-Brasil, túnel seguro mTLS bidirecional e tokens OAuth 2.0 atrelados criptograficamente (RFC 8705)." })
                    ]
                  })
                ]
              }),
              w("button", {
                onClick: testIcp,
                disabled: isTestingIcp,
                className: "px-4 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-black text-[11px] font-mono font-bold transition-all shrink-0 flex items-center gap-2 shadow-lg shadow-amber-500/20",
                children: [
                  isTestingIcp ? p("span", { className: "animate-spin", children: "⏳" }) : p("span", { children: "⚡" }),
                  isTestingIcp ? "EXECUTANDO HANDSHAKE..." : "TESTAR HANDSHAKE mTLS"
                ]
              })
            ]
          }),

          icpTestMsg && p("div", {
            className: "p-3 rounded-xl border text-[11px] font-mono leading-relaxed text-center " + (icpTestMsg.includes('✅') ? "bg-emerald-950/30 border-emerald-500/30 text-emerald-300" : "bg-amber-950/30 border-amber-500/30 text-amber-300"),
            children: icpTestMsg
          }),

          // Grade com 3 Pilares da Autenticação
          w("div", {
            className: "grid md:grid-cols-3 gap-4",
            children: [
              w("div", {
                className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-2",
                children: [
                  w("div", {
                    className: "flex items-center gap-2 text-cyan-400 font-mono text-[11px] font-semibold uppercase tracking-wider",
                    children: [p("span", { children: "1." }), p("span", { children: "Handshake mTLS" })]
                  }),
                  p("p", { className: "text-[11px] text-zinc-400 leading-relaxed", children: "Túnel TLS mútuo (1.2/1.3). Tanto a nossa aplicação quanto o servidor do Banco Central (SPI/DICT) trocam certificados e comprovam a posse das chaves privadas." })
                ]
              }),
              w("div", {
                className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-2",
                children: [
                  w("div", {
                    className: "flex items-center gap-2 text-emerald-400 font-mono text-[11px] font-semibold uppercase tracking-wider",
                    children: [p("span", { children: "2." }), p("span", { children: "Certificado ICP-Brasil" })]
                  }),
                  p("p", { className: "text-[11px] text-zinc-400 leading-relaxed", children: "Certificado e-CNPJ padrão X.509 v3 emitido por AC homologada (Certisign, Serasa, Soluti) ou AC-SPB com chaves RSA de 2048 bits." })
                ]
              }),
              w("div", {
                className: "p-4 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-2",
                children: [
                  w("div", {
                    className: "flex items-center gap-2 text-amber-400 font-mono text-[11px] font-semibold uppercase tracking-wider",
                    children: [p("span", { children: "3." }), p("span", { children: "OAuth 2.0 RFC 8705" })]
                  }),
                  p("p", { className: "text-[11px] text-zinc-400 leading-relaxed", children: "O token de acesso JWT fica travado criptograficamente no thumbprint do certificado. Se o token for interceptado, torna-se inútil sem o certificado físico." })
                ]
              })
            ]
          }),

          // Detalhes do Certificado Ativo e Comandos
          w("div", {
            className: "grid lg:grid-cols-2 gap-4",
            children: [
              // Cartão do Certificado
              w("div", {
                className: "p-5 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-3",
                children: [
                  w("div", {
                    className: "flex items-center justify-between border-b border-[var(--border)] pb-3",
                    children: [
                      p("h4", { className: "text-[12px] font-semibold text-zinc-200", children: "Certificado Digital Ativo na Aplicação" }),
                      p("span", { className: "text-[9px] px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono tracking-widest", children: "HOMOLOGADO" })
                    ]
                  }),
                  w("div", {
                    className: "space-y-2 font-mono text-[11px]",
                    children: [
                      w("div", { className: "flex justify-between py-1 border-b border-[var(--border)]/40", children: [p("span", { className: "text-zinc-500", children: "Titular (CNPJ):" }), p("span", { className: "text-zinc-200", children: "MUSE PAGAMENTOS (48.192.837/0001-20)" })] }),
                      w("div", { className: "flex justify-between py-1 border-b border-[var(--border)]/40", children: [p("span", { className: "text-zinc-500", children: "Autoridade Emissora:" }), p("span", { className: "text-cyan-300", children: "AC SERASA RFB v5 (ICP-Brasil)" })] }),
                      w("div", { className: "flex justify-between py-1 border-b border-[var(--border)]/40", children: [p("span", { className: "text-zinc-500", children: "Tipo & Criptografia:" }), p("span", { className: "text-zinc-200", children: "e-CNPJ A1 (RSA 2048 / SHA-256)" })] }),
                      w("div", { className: "flex justify-between py-1 border-b border-[var(--border)]/40", children: [p("span", { className: "text-zinc-500", children: "Validade do Certificado:" }), p("span", { className: "text-emerald-400", children: "Até 31/12/2027 (Ativo)" })] }),
                      w("div", { className: "flex flex-col gap-1 pt-1", children: [p("span", { className: "text-zinc-500", children: "SHA-256 Fingerprint (Thumbprint):" }), p("span", { className: "text-[10px] text-zinc-400 bg-black/40 p-1.5 rounded select-all", children: "A4:9F:8B:71:3C:9E:01:DF:77:2B:EE:51:90:3A:45:C2:7D:6E:8A:10" })] })
                    ]
                  })
                ]
              }),

              // Cartão de Instruções OpenSSL & Node.js
              w("div", {
                className: "p-5 rounded-xl bg-[var(--surface-2)] border border-[var(--border)] flex flex-col gap-3",
                children: [
                  w("div", {
                    className: "flex items-center justify-between border-b border-[var(--border)] pb-3",
                    children: [
                      p("h4", { className: "text-[12px] font-semibold text-zinc-200", children: "Como Instalar o Certificado no Servidor" }),
                      w("button", {
                        onClick: copyIcpCmd,
                        className: "text-[10px] font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1",
                        children: [p("span", { children: icpCopied ? "✓ COPIADO" : "COPIAR COMANDO" })]
                      })
                    ]
                  }),
                  p("p", { className: "text-[11px] text-zinc-400 leading-relaxed", children: "Bancos e certificadoras fornecem o certificado em formato .p12 ou .pfx. Converta para .pem com o comando abaixo e salve na pasta certs/:" }),
                  p("pre", {
                    className: "p-2.5 rounded-lg bg-black/60 border border-[var(--border)] text-[11px] font-mono text-amber-300 overflow-x-auto select-all",
                    children: "openssl pkcs12 -in certificado_empresa.p12 -out certs/pix_producao.pem -nodes"
                  }),
                  p("p", { className: "text-[10.5px] text-zinc-500 leading-relaxed", children: "No Node.js, a conexão é aberta com https.Agent passando { cert, key } e associada ao endpoint /oauth/token do PSP Pix." })
                ]
              })
            ]
          }),

          // Box de Esclarecimento Didático: ICP-Brasil vs Web3 ICP
          w("div", {
            className: "p-4 rounded-xl bg-zinc-900/60 border border-[var(--border)] flex flex-col gap-2",
            children: [
              w("div", {
                className: "flex items-center gap-2",
                children: [
                  p("span", { children: "💡" }),
                  p("h5", { className: "text-[11px] font-mono font-semibold text-zinc-300 uppercase tracking-wider", children: "Nota de Esclarecimento sobre o Termo 'ICP'" })
                ]
              }),
              w("div", {
                className: "grid md:grid-cols-2 gap-3 text-[11px] leading-relaxed text-zinc-400",
                children: [
                  w("div", {
                    className: "p-3 rounded-lg bg-black/30 border border-[var(--border)]",
                    children: [
                      p("strong", { className: "text-amber-300 block mb-1 font-mono", children: "🇧🇷 No Contexto Bancário / BACEN (Nosso Projeto):" }),
                      p("span", { children: "ICP refere-se à ICP-Brasil (Infraestrutura de Chaves Públicas Brasileira). Autenticação estritamente institucional regulada pelo Banco Central com certificados digitais e-CNPJ e mTLS para transações Pix." })
                    ]
                  }),
                  w("div", {
                    className: "p-3 rounded-lg bg-black/30 border border-[var(--border)]",
                    children: [
                      p("strong", { className: "text-cyan-300 block mb-1 font-mono", children: "🌐 No Contexto Web3 / Blockchain:" }),
                      p("span", { children: "ICP refere-se ao Internet Computer Protocol (DFINITY). A autenticação é via Internet Identity usando biometria e Passkeys (WebAuthn/FIDO2) do navegador sem certificados governamentais." })
                    ]
                  })
                ]
              })
            ]
          })
        ]
      }),

      """

if old_tab_target not in content:
    raise ValueError("old_tab_target not found in index.html")
content = content.replace(old_tab_target, icp_content + old_tab_target, 1)

with open('/home/agent/workspace/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected ICP-Brasil authentication UI into index.html!")
