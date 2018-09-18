rm fifo.cu8
mkfifo fifo.cu8
rm FSK.ft
mkfifo FSK.ft


rtl_sdr -g 30 -f 434248000 -s 1300000 fifo.cu8 &
#sudo ../rpitx/rpitx -m IQ -i FSK.ft -f 433916 -s 325000 -c 1 -a 14 &
sudo ../rpitx/rpitx -m IQFLOAT -i FSK.ft -f 433916 -s 325000 -d 1000 -c 1 -a 14  &

./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 14 -p 0 -c 
#./rtlomni -i fifo.cu8 -m tx -a 1f108958 -t 650610 -l 42335 -n 0 -p 0 -c 

#./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 0 -p 0 -c 
#./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 3 -p 3 -c 
#./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 5 -p 8 -c 
#./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 7 -p 11 -c 
#./rtlomni -i fifo.cu8 -m tx -a 1f10895a -t 650610 -l 42335 -n 9 -p 13 -c 
