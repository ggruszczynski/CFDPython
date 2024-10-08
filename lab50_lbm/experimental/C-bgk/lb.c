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

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "lb.h"
#include "assert.h"

/* D2Q9 lattice constants                                        */
/*****************************************************************/

  // lattice weights
static const double t[9] = { 4./9., 1./9., 1./9., 1./9., 1./9.,
                             1./36., 1./36., 1./36., 1./36. };
  // lattice velocities
static const int c[9][2] = {
    {0,0},
    {1,0}, {0,1}, {-1,0}, {0,-1},
    {1,1}, {-1,1}, {-1,-1}, {1,-1}
};


/* struct Node, methods                                          */
/*****************************************************************/

  // initialize a node to default value
void constructNode(Node* node) {
    int iPop;
    for (iPop=0; iPop<9; ++iPop) {
        node->fPop[iPop] = 0.;
    }
    node->dynamics = 0;
}

  // initialize a node to its local equilibrium term
void iniEquilibrium(Node* node, double rho, double ux, double uy) {
    int iPop;
    double uSqr = ux*ux + uy*uy;
    for (iPop=0; iPop<9; ++iPop) {
        node->fPop[iPop] =
            computeEquilibrium(iPop, rho, ux, uy, uSqr);
    }
}


/* struct Simulation, methods                                    */
/*****************************************************************/

  // allocate memory for a full simulation ("constructor")
void constructSim(Simulation* sim, int lx, int ly) {
    sim->lx = lx;
    sim->ly = ly;

    sim->memoryChunk    =
        (Node*) calloc((lx+2)*(ly+2), sizeof(Node));
    sim->tmpMemoryChunk =
        (Node*) calloc((lx+2)*(ly+2), sizeof(Node));
    sim->lattice        = (Node**) calloc(lx+2, sizeof(Node*));
    sim->tmpLattice     = (Node**) calloc(lx+2, sizeof(Node*));

    int iX, iY;
    for (iX=0; iX<lx+2; ++iX) {
        sim->lattice[iX] = sim->memoryChunk + iX*(ly+2);
        sim->tmpLattice[iX] = sim->tmpMemoryChunk + iX*(ly+2);
        for (iY=0; iY<ly+2; ++iY) {
            constructNode(&(sim->lattice[iX][iY]));
            constructNode(&(sim->tmpLattice[iX][iY]));
        }
    }
}

  // free the memory for the simulation ("destructor")
void destructSim(Simulation* sim) {
    free(sim->lattice);
    free(sim->memoryChunk);
    free(sim->tmpLattice);
    free(sim->tmpMemoryChunk);
}

  // specify the dynamics for a given lattice site
void setDynamics(Simulation* sim, int iX, int iY, Dynamics *dyn) {
    sim->lattice[iX][iY].dynamics = dyn;
    sim->tmpLattice[iX][iY].dynamics = dyn;
}

  // apply collision step to a lattice node (and simulate
  //   virtual dispatch)
inline static void collideNode(Node* node) {
    node->dynamics->dynamicsFun(node->fPop,
                                node->dynamics->selfData);
}

  // apply collision step to all lattice nodes
void collide(Simulation* sim) {
    int iX, iY;
    for (iX=1; iX<=sim->lx; ++iX) {
        for (iY=1; iY<=sim->ly; ++iY) {
            collideNode(&(sim->lattice[iX][iY]));
        }
    }
}

  // apply propagation step with help of temporary memory
void propagate(Simulation* sim) {
    int iX, iY, iPop;
    int lx = sim->lx;
    int ly = sim->ly;
    for (iX=1; iX<=lx; ++iX) {
        for (iY=1; iY<=ly; ++iY) {
            for (iPop=0; iPop<9; ++iPop) {
                int nextX = iX + c[iPop][0];
                int nextY = iY + c[iPop][1];
                sim->tmpLattice[nextX][nextY].fPop[iPop] =
                    sim->lattice[iX][iY].fPop[iPop];
            }
        }
    }
    Node** swapLattice = sim->lattice;
    sim->lattice = sim->tmpLattice;
    sim->tmpLattice = swapLattice;
}

  // implement periodic boundary conditions (to be called after
  //   the propagation step)
void makePeriodic(Simulation* sim) {
    int lx = sim->lx;
    int ly = sim->ly;
    Node** lat = sim->lattice;

    int iX, iY;
    for (iX=1; iX<=lx; ++iX) {
        lat[iX][ly].fPop[4] = lat[iX][0].fPop[4];
        lat[iX][ly].fPop[7] = lat[iX][0].fPop[7];
        lat[iX][ly].fPop[8] = lat[iX][0].fPop[8];

        lat[iX][1].fPop[2] = lat[iX][ly+1].fPop[2];
        lat[iX][1].fPop[5] = lat[iX][ly+1].fPop[5];
        lat[iX][1].fPop[6] = lat[iX][ly+1].fPop[6];
    }

    for (iY=1; iY<=ly; ++iY) {
        lat[1][iY].fPop[1] = lat[lx+1][iY].fPop[1];
        lat[1][iY].fPop[5] = lat[lx+1][iY].fPop[5];
        lat[1][iY].fPop[8] = lat[lx+1][iY].fPop[8];

        lat[lx][iY].fPop[3] = lat[0][iY].fPop[3];
        lat[lx][iY].fPop[6] = lat[0][iY].fPop[6];
        lat[lx][iY].fPop[7] = lat[0][iY].fPop[7];
    }

    lat[1][1].fPop[5]   = lat[lx+1][ly+1].fPop[5];
    lat[lx][1].fPop[6]  = lat[0][ly+1].fPop[6];
    lat[lx][ly].fPop[7] = lat[0][0].fPop[7];
    lat[1][ly].fPop[8]  = lat[lx+1][0].fPop[8];
}

  // save the velocity field (norm) to disk
void saveVel(Simulation* sim, char fName[]) {
    FILE* oFile = fopen(fName, "w");
    int iX, iY;
    double ux, uy, uNorm, rho;
    for (iY=1; iY<=sim->ly; ++iY) {
       for (iX=1; iX<=sim->lx; ++iX) {
           computeMacros(sim->lattice[iX][iY].fPop, &rho, &ux, &uy);
           uNorm = sqrt(ux*ux+uy*uy);
           fprintf(oFile, "%f ", uNorm);
       }
       fprintf(oFile, "\n");
    }
    fclose(oFile);
}

  // save one lattice population to disk
void saveF(Simulation* sim, int iPop, char fName[]) {
    FILE* oFile = fopen(fName, "w");
    int iX, iY;
    double ux, uy, uNorm, rho;
    for (iY=1; iY<=sim->ly; ++iY) {
       for (iX=1; iX<=sim->lx; ++iX) {
           double f = sim->lattice[iX][iY].fPop[iPop];
           fprintf(oFile, "%f ", f);
       }
       fprintf(oFile, "\n");
    }
    fclose(oFile);
}


/* some free helper functions                                    */
/*****************************************************************/

  // compute density and velocity from the f's 
void computeMacros(double* f, double* rho, double* ux, double* uy) {
    double upperLine  = f[2] + f[5] + f[6];
    double mediumLine = f[0] + f[1] + f[3];
    double lowerLine  = f[4] + f[7] + f[8];
    *rho = upperLine + mediumLine + lowerLine;
    *ux  = (f[1] + f[5] + f[8] - (f[3] + f[6] + f[7]))/(*rho);
    *uy  = (upperLine - lowerLine)/(*rho);
}

  // compute local equilibrium from rho and u
double computeEquilibrium(int iPop, double rho,
                          double ux, double uy, double uSqr)
{
    double c_u = c[iPop][0]*ux + c[iPop][1]*uy;
    return rho * t[iPop] * (
               1. + 3.*c_u + 4.5*c_u*c_u - 1.5*uSqr
           );
}

  // bgk collision term
void bgk(double* fPop, void* selfData) {
    double omega = *((double*)selfData);
    double rho, ux, uy;
    computeMacros(fPop, &rho, &ux, &uy);
    double uSqr = ux*ux+uy*uy;
    int iPop;
    for(iPop=0; iPop<9; ++iPop) {
        fPop[iPop] *= (1-omega);
        fPop[iPop] += omega * computeEquilibrium (
                                  iPop, rho, ux, uy, uSqr );
    }
}

