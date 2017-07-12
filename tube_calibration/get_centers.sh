for file in *.peaks;
do
    echo -n $file\  | sed 's/.peaks//' | sed 's/COR_//' | sed 's/_/ /'g
    cut -f2 $file | head -17 | tail -16 | sort -n | tr '\n' ' '
    echo
done
