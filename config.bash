#/bin/bash



mv macroMaker/utils/C/* .
mv src/makeMLC_statique.c .
mv src/makeMLC_dynamique.c .

g++ -c *.c

mv makeMLC_statique.c src/
mv makeMLC_dynamique.c src/

g++ makeMLC_statique.o -o makeMLC
g++ makeMLC_dynamique.o -o makeDynaMLC
rm *.o
mv makeMLC makeDynaMLC bin/

mv bin src macroMaker/utils/C/

echo CONGRATULATIONS...configuration ok!



