CFITSIO = $(FITSIOROOT)
CPP = g++
CC = gcc
CFLAGS = -Wall -I$(CFITSIO) $(shell root-config --cflags) -O3
LIBS = -L$(CFITSIO) -lcfitsio -lm $(shell root-config --glibs) -lTreeViewer
GLIBS =
GLIBS +=
OBJECTS = grapher.o 
HEADERS =

ALL : grapher.exe
	echo "Done!"

grapher.exe : $(OBJECTS)
	$(CPP) $(OBJECTS) -o grapher.exe $(LIBS) $(GLIBS) $(CFLAGS)

grapher.o : grapher.cc $(HEADERS)
	$(CPP) -c grapher.cc -o grapher.o $(CFLAGS)

clean:
	rm -f *~ *.o *.exe
