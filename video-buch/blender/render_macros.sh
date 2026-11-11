#!/bin/bash
cd "$(dirname "$0")"
PY=${PY:-python3}
SHOT=eye   SHOT_DUR=3.4 $PY book.py anim frames_eye   40 50 24 2>&1 | grep -E "DONE|Traceback|Error"
SHOT=spine SHOT_DUR=3.2 $PY book.py anim frames_spine 40 50 24 2>&1 | grep -E "DONE|Traceback|Error"
SHOT=title SHOT_DUR=3.0 $PY book.py anim frames_title 40 50 24 2>&1 | grep -E "DONE|Traceback|Error"
echo ALL_DONE
