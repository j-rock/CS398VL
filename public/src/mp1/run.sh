mkdir cleaned

for i in 1 2 3 4;
do
  runhaskell main.hs orig/ofk$i.txt > cleaned/ofk$i.txt
done

python2.7 process_files.py
rm -rf cleaned
