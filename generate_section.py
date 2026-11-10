import os
import re

with open('/home/agent/workspace/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect where yu() is defined and where Section 03 ends
target_yu_section3_end = 'children:[p("span",{children:"⚙️ Comentários em PT-BR por padrão — BSC formal language enforced"}),p("span",{className:"text-zinc-600",children:"Muse generated • human reviewed • quorum approved"})]})]}),w("footer"'
assert target_yu_section3_end in content, "Could not find Section 03 end in yu()"

target_html_section3_end = '<span>⚙️ Comentários em PT-BR por padrão — BSC formal language enforced</span><span class="text-zinc-600">Muse generated • human reviewed • quorum approved</span></div></section><footer class="rounded-[14px]'
assert target_html_section3_end in content, "Could not find Section 03 end in HTML"

print("Both insertion points located successfully!")
