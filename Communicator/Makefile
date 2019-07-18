CC=gcc
CFLAGS=-g -W -Wall #$(shell pkg-config --cflags gtk+-3.0)
LDFLAGS= # $(shell pkg-config --libs gtk+-3.0)
OBJ = communicator.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

communicator: $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

.PHONY: clean

clean:
	rm -f ./*.o