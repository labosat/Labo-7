CFITSIO = $(FITSIOROOT)
CPP = g++
CC = gcc
CFLAGS = -Wall -I$(CFITSIO) $(shell root-config --cflags) -O3
LIBS = -L$(CFITSIO) -lcfitsio -lm $(shell root-config --glibs) -lTreeViewer
GLIBS =
GLIBS +=
OBJECTS = rq.o 
HEADERS =

ALL : rq.exe
	echo "Done!"

rq.exe : $(OBJECTS)
	$(CPP) $(OBJECTS) -o rq.exe $(LIBS) $(GLIBS) $(CFLAGS)

rq.o : rq.cc $(HEADERS)
	$(CPP) -c rq.cc -o rq.o $(CFLAGS)

clean:
	rm -f *~ *.o *.exe
