#!/bin/bash
# Rendert alle 4 Szenen als PNG-Sequenzen (fortsetzbar: fertige Bilder werden übersprungen)
PY=${PY:-python3}
cd "$(dirname "$0")"
for s in 1 2 3 4; do
  $PY brandfilm.py anim $s frames/s$s 24 50 24 2>&1 | grep -E "FRAME|DONE|Error|Traceback"
done
echo ALL_DONE
