import os
import subprocess

with open('/home/agent/workspace/generate_section.py', 'r') as f:
    gen_code = f.read()

# Extract component_js
start_marker = "component_js = r'''"
end_marker = "'''\n\n# Verify component syntax"
component_js = gen_code[gen_code.find(start_marker) + len(start_marker):gen_code.find(end_marker)].strip()

with open('/home/agent/workspace/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Static HTML for Section 04
static_html = '''<section class="rounded-[16px] border border-[var(--border)] bg-[var(--surface)] overflow-hidden"><div class="px-6 py-5 border-b border-[var(--border)] flex flex-col md:flex-row md:items-center justify-between gap-4"><div class="flex items-center gap-3"><div class="w-7 h-7 rounded-lg bg-[var(--surface-3)] border border-[var(--border)] flex items-center justify-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-database w-4 h-4 text-emerald-400"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5V19A9 3 0 0 0 21 19V5"></path><path d="M3 12A9 3 0 0 0 21 12"></path></svg></div><div><h2 class="text-[13px] font-semibold tracking-wide flex items-center gap-2">04 — CENTRAL DE CONEXÃO: BASE DE DADOS &amp; APIs<span class="text-[9px] px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono tracking-widest uppercase">INTERATIVO</span></h2><p class="text-[11px] font-mono text-zinc-500">Conexão Unificada: Supabase / PostgreSQL / SQLite • Meta WhatsApp Cloud API • Gateway Pix BACEN</p></div></div><div class="flex flex-wrap items-center gap-2"><div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--surface-2)] border border-[var(--border)]"><div class="w-1.5 h-1.5 rounded-full animate-pulse bg-emerald-400"></div><span class="text-[10px] font-mono text-zinc-500">BASE:</span><span class="text-[10px] font-mono font-medium text-emerald-300">SUPABASE (24ms)</span></div><div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--surface-2)] border border-[var(--border)]"><div class="w-1.5 h-1.5 rounded-full animate-pulse bg-cyan-400"></div><span class="text-[10px] font-mono text-zinc-500">APIs:</span><span class="text-[10px] font-mono font-medium text-cyan-300">META + PIX OK</span></div></div></div><div class="p-6 flex flex-col gap-6"><div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"><div class="flex items-start gap-3"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-terminal w-5 h-5 text-cyan-400 shrink-0 mt-0.5"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" x2="20" y1="19" y2="19"></line></svg><div><h3 class="text-[12px] font-semibold text-cyan-300 uppercase tracking-wide">Simulador de Ciclo de Venda &amp; Pagamento Pix em Produção</h3><p class="text-[11px] text-zinc-400 mt-1 leading-relaxed">Pipeline completo: 1. Gravação do Pedido no Banco de Dados -&gt; 2. Emissão do BRCode Pix -&gt; 3. Recepção do Webhook BACEN com validação HMAC -&gt; 4. Gravação de Log WORM Imutável -&gt; 5. Envio de Confirmação formal via WhatsApp.</p></div></div><button class="px-4 py-2.5 rounded-lg text-[12px] font-mono font-medium shrink-0 transition-all flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 text-black shadow-lg shadow-emerald-500/20 font-bold"><span>⚡</span>EXECUTAR FLUXO COMPLETO</button></div></div><div class="px-6 py-4 border-t border-[var(--border)] bg-black/30 flex flex-col md:flex-row gap-3 justify-between text-[11px] font-mono text-zinc-500"><span class="flex items-center gap-2"><span>🛡️ Trilha WORM imutável &amp; Compliance LGPD/BACEN</span><span class="text-zinc-600">• FCR 7 dias ativado</span></span><span class="text-zinc-600">SQLite Nativo • PostgreSQL • Supabase Ready • Node 22 API</span></div></section>'''

# 2. Insert static HTML before <footer
html_footer_target = '<footer class="rounded-[14px] border border-[var(--border)] bg-[var(--surface)] px-6 py-5 grid md:grid-cols-3 gap-6">'
assert html_footer_target in html_content, "Could not find HTML footer"
new_html_content = html_content.replace(html_footer_target, static_html + html_footer_target, 1)

# 3. Insert DbApiSection component before function yu()
yu_func_target = 'function yu(){'
assert yu_func_target in new_html_content, "Could not find function yu()"
new_html_content = new_html_content.replace(yu_func_target, component_js + '\n' + yu_func_target, 1)

# 4. Insert p(DbApiSection,{}) into yu() main children array right before w("footer"
yu_footer_target = ',w("footer",{className:"rounded-[14px] border border-[var(--border)] bg-[var(--surface)] px-6 py-5 grid md:grid-cols-3 gap-6"'
assert yu_footer_target in new_html_content, "Could not find yu footer"
new_html_content = new_html_content.replace(yu_footer_target, ',p(DbApiSection,{})' + yu_footer_target, 1)

# Save to index.html
with open('/home/agent/workspace/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print("Successfully updated index.html!")
