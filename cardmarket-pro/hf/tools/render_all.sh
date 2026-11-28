set -e
cd /home/user/kyomania/cardmarket-pro/hf
R="npx --yes hyperframes@0.9.104 render -f 24 -q delivery -w 2"
D=../videos/Final4_5
E="-c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2"
cd seller
for L in DE EN ES FR IT NL; do python3 gen.py $L >/dev/null; $R -o out/SELLER_${L}_3x4.mp4 >/dev/null 2>&1; I=out/SELLER_${L}_3x4.mp4
 ffmpeg -v error -y -i $I -vf "crop=834:1042:0:35,scale=1080:1350:flags=lanczos" $E $D/$L/SELLER_CENTER_1_${L}_4x5.mp4
 ffmpeg -v error -y -i $I -filter_complex "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];[0]scale=1080:1440:flags=lanczos[fg];[bg][fg]overlay=0:240" $E $D/$L/SELLER_CENTER_1_${L}_9x16.mp4
 rm -f $D/$L/SELLER_CENTER_1_$L.mp4; echo "SELLER $L"; done
cd ../app
for L in DE EN ES FR IT NL; do for F in 9x16 4x5; do python3 gen.py $L $F >/dev/null; $R -o out/APP_${L}_${F}.mp4 >/dev/null 2>&1; cp out/APP_${L}_${F}.mp4 $D/$L/APP_LAUNCH_1_${L}_${F}.mp4; echo "APP $L $F"; done; done
