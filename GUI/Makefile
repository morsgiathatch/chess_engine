CC=gcc
CFLAGS=-g -W -Wall $(shell pkg-config --cflags gtk+-3.0)
LDFLAGS=$(shell pkg-config --libs gtk+-3.0)
DEPS = board.h
OBJ = gui_main.o board.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

gui_main: $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

.PHONY: clean

clean:
	rm -f ./*.o