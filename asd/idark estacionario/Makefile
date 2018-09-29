CFITSIO = $(FITSIOROOT)
CPP = g++
CC = gcc
CFLAGS = -Wall -I$(CFITSIO) $(shell root-config --cflags) -O3
LIBS = -L$(CFITSIO) -lcfitsio -lm $(shell root-config --glibs) -lTreeViewer
GLIBS =
GLIBS +=
OBJECTS = idark.o 
HEADERS =

ALL : idark.exe
	echo "Done!"

idark.exe : $(OBJECTS)
	$(CPP) $(OBJECTS) -o idark.exe $(LIBS) $(GLIBS) $(CFLAGS)

idark.o : idark.cc $(HEADERS)
	$(CPP) -c idark.cc -o idark.o $(CFLAGS)

clean:
	rm -f *~ *.o *.exe
