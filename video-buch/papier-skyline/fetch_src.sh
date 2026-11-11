#!/usr/bin/env bash
# Lädt die 11 Seedream-4.5-Bilder (Higgsfield, 11.11.2026) nach src/ (nicht im Repo, ~190 MB)
set -e; cd "$(dirname "$0")"; mkdir -p src
B=https://d8j0ntlcm91z4.cloudfront.net/user_3264KFSseuho48GajeCTiMLAiDl/hf_20261111_
i=1
for f in 212640_2834815d-6ecb-42ec-9202-7c54056d8b52 212659_f66f5380-54cc-4873-966f-9882875f34e1 \
         212718_9f9a1766-bcb3-408b-a238-f13df23906c1 212729_462e2343-4907-429b-8cd3-7fb9cfee30da \
         212739_20e033e4-499b-44f1-88dc-da046f591d9b 212747_3b723827-9a85-4877-95ed-9163783d48fa \
         212756_55be9727-2f3d-47da-bed4-6455b97134b4 212801_33ccfd5a-23bf-4060-b553-78f561880406 \
         213643_5ffabb03-8ad9-4054-bdc8-028b0675bf4b 213653_ef0e9c31-6388-47f7-bca9-5576bfcc07eb \
         213717_fdbe12e6-57b6-4df1-b6ff-948418428881; do
  [ -f "src/$(printf g%02d.png $i)" ] || curl -sS -o "src/$(printf g%02d.png $i)" "$B$f.png"; i=$((i+1))
done
