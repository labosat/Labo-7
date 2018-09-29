CFITSIO = $(FITSIOROOT)
CPP = g++
CC = gcc
CFLAGS = -Wall -I$(CFITSIO) $(shell root-config --cflags) -O3
LIBS = -L$(CFITSIO) -lcfitsio -lm $(shell root-config --glibs) -lTreeViewer
GLIBS =
GLIBS +=
OBJECTS = vbr.o 
HEADERS =

ALL : vbr.exe
	echo "Done!"

vbr.exe : $(OBJECTS)
	$(CPP) $(OBJECTS) -o vbr.exe $(LIBS) $(GLIBS) $(CFLAGS)

vbr.o : vbr.cc $(HEADERS)
	$(CPP) -c vbr.cc -o vbr.o $(CFLAGS)

clean:
	rm -f *~ *.o *.exe
