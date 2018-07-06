rm fifo.cu8
mkfifo fifo.cu8
rtl_sdr -g 20 -f 434248000 -s 1300000 fifo.cu8 &
./rtlomni -i fifo.cu8 -c

