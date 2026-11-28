set -e
cd /home/user/kyomania/cardmarket-pro/hf/buy1
D=/home/user/kyomania/cardmarket-pro/videos/Final4_5
for L in DE EN ES FR IT NL; do for F in 9x16 4x5; do python3 gen.py $L $F >/dev/null; npx --yes hyperframes@0.9.104 render -f 24 -q delivery -w 2 -o out/BUY1_${L}_${F}.mp4 >/dev/null 2>&1; cp out/BUY1_${L}_${F}.mp4 $D/$L/COLLECTOR_BUY_1_${L}_${F}.mp4; echo "BUY1 $L $F"; done; done
