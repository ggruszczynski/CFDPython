# Lattice Boltzmann sample, written in C
#
# Copyright (C) 2006 Jonas Latt
# Address: Rue General Dufour 24,  1211 Geneva 4, Switzerland 
# E-mail: Jonas.Latt@cui.unige.ch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.


CC   = gcc
COPT = -O3 -march=athlon-4
LOPT =

default: unsteady

unsteady: unsteady.o lb.o boundaries.o
	${CC} ${LOPT} -o unsteady -lm unsteady.o lb.o boundaries.o

unsteady.o: lb.h boundaries.h unsteady.c
	${CC} $(COPT) -c unsteady.c

lb.o: lb.h lb.c
	${CC} $(COPT) -c lb.c

boundaries.o: boundaries.h lb.h boundaries.c
	${CC} $(COPT) -c boundaries.c

clean:
	rm -f unsteady vel.dat *.o *~
