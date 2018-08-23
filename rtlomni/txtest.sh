rm fifo.cu8
mkfifo fifo.cu8
rm FSK.ft
mkfifo FSK.ft


rtl_sdr -g 30 -f 434248000 -s 1300000 fifo.cu8 &
sudo ../rpitx/rpitx -m RF -i FSK.ft -f 433916 -c 1 -a 14 &
./rtlomni -i fifo.cu8 -m tx -a 1f108958 -n 10 -p 3 -c 


