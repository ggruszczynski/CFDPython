/*  Lattice Boltzmann sample, written in C
 *
 *  Copyright (C) 2006 Jonas Latt
 *  Address: Rue General Dufour 24,  1211 Geneva 4, Switzerland 
 *  E-mail: Jonas.Latt@cui.unige.ch
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public 
 *  License along with this program; if not, write to the Free 
 *  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 *  Boston, MA  02110-1301, USA.
 */

/* lb.h: Assembly of various functions for simulating a lattice
 *       Boltzmann dynamics with BGK collision term on a two-
 *       dimenional D2Q9 lattice. The code is generic: every
 *       lattice site can have a different dynamics.
 *       Other collision terms than BGK can easily be added.
 */

#ifndef LB_H
#define LB_H

#include "stddef.h"

/* struct Dynamics                                               */
/*****************************************************************/
/*   emulation of a class that defines the dynamics of a lattice
 *   site. The function dynamicsFun contains the algorithm of the
 *   collision, and selfData points to the function arguments
 *   (for example the local viscosity)
 */
typedef struct {
    void   (*dynamicsFun) (double* fPop, void* selfData);
    void* selfData;
} Dynamics;


/* struct Node                                                   */
/*****************************************************************/
/*  a lattice node, containing the data (distribution functions)
 *  for a D2Q9 lattice, and a pointer to the local dynamics, i.e.
 *  the collision term. Two "methods" are added to construct and
 *  initialize a node.
 */
typedef struct {
    double    fPop[9];
    Dynamics* dynamics;
} Node;

void constructNode(Node* node);
void iniEquilibrium(Node* node, double rho, double ux, double uy);


/* struct Simulation                                             */
/*****************************************************************/
/*  a full D2Q9 LB simulation, containing the allocated memory
 *  for the lattice. Some "methods" are added to initiate the
 *  dynamics.
 */
typedef struct {
    int lx, ly;               // lx*ly lattice
    Node*  memoryChunk;       // contiguous raw memory
    Node*  tmpMemoryChunk;    // contiguous raw tmp memory
    Node** lattice;           // lattice, points to raw memory
    Node** tmpLattice;        // tmp lasttice, points to raw memory
} Simulation;

void constructSim(Simulation* sim, int lx, int ly);
void destructSim(Simulation* sim);
void setDynamics(Simulation* sim, int iX, int iY, Dynamics* dyn);
void collide(Simulation* sim);
void propagate(Simulation* sim);
void makePeriodic(Simulation* sim);
void saveVel(Simulation* sim, char fName[]);
void saveF(Simulation* sim, int iPop, char fName[]);


/* some free helper functions                                    */
/*****************************************************************/

  // compute density and velocity from the f's 
void computeMacros(double* f, double* rho, double* ux, double* uy);

  // compute local equilibrium from rho and u
double computeEquilibrium(int iPop, double rho,
                          double ux, double uy, double uSqr);
  // bgk collision term
void bgk(double* fPop, void* selfData);

#endif
