all: omnitx 

CFLAGS	= -std=c99 -Wall -g -O2 -Wno-unused-variable
LDFLAGS	= -lm -lrt -lpthread 
omnitx : omnitx.c
	$(CC) $(CFLAGS) -o omnitx omnitx.c  $(LDFLAGS) 
