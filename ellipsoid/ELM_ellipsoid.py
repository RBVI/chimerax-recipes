# Draw a rotated ellipsoid, given the values of center of mass, semiaxes, and eigenvectors 
# written by Matthew Casertano and David Fushman, University of Maryland, June 2019
from pymol.cgo import BEGIN, COLOR, TRIANGLES, VERTEX, NORMAL, END
from pymol import cmd

def sin (theta): return math.sin(math.radians(theta)) # sine of an angle in degree form
def cos (theta): return math.cos(math.radians(theta)) # cosine of an angle in degree form


def ellipsoid(cmx, cmy, cmz, a1, a2, a3, u, v, R11, R12, R13, R21, R22, R23, R31, R32, R33):
 
    #coordinates of ellipsoid points and the normals in the ellipsoid coordinate frame 
        x0 = a1 * cos(u) * cos(v)
        y0 = a2 * cos(u) * sin(v)
        z0 = a3 * sin(u)
        
        nx0 = x0 / (a1 ** 2)
        ny0 = y0 / (a2 ** 2)
        nz0 = z0 / (a3 ** 2)

    #rotate the coordinates of ellipsoid points and the normals into the protein coordinate frame 
    #and shift the center of ellipsoid to coincide with the COM of the protein molecule 

        x = x0 * R11 + y0 * R12 + z0 * R13 + cmx
        y = x0 * R21 + y0 * R22 + z0 * R23 + cmy
        z = x0 * R31 + y0 * R32 + z0 * R33 + cmz

        nx = nx0 * R11 + ny0 * R12 + nz0 * R13
        ny = nx0 * R21 + ny0 * R22 + nz0 * R23 
        nz = nx0 * R31 + ny0 * R32 + nz0 * R33 

        return x, y, z, nx, ny, nz

def makeEllipsoid(color, cmx, cmy, cmz, a1, a2, a3, u1, u2, v1, v2, u_segs, v_segs, R11, R12, R13, R21, R22, R23, R31, R32, R33):

        r, g, b = color

        # Calculate delta variables 
        dU = (u2 - u1) / u_segs
        dV = (v2 - v1) / v_segs

        o = [BEGIN, TRIANGLES]

        U = u1
        for Y in range(0, u_segs):
                # Initialize variables for loop 
                V = v1
                for X in range(0, v_segs):
                    x, y, z, nx, ny, nz = [0] * 5, [0] * 5, [0] * 5, [0] * 5, [0] * 5, [0] * 5 # this allows the array to be filled
                    for i in range(1, 5): # creates four sets of ellipsoid points and normals, indexed from 1 through 4
                        x[i], y[i], z[i], nx[i], ny[i], nz[i] = ellipsoid(cmx, cmy, cmz, a1, a2, a3, U + dU * (i == 2 or i == 3), V + dV * (i == 3 or i == 4), R11, R12, R13, R21, R22, R23, R31, R32, R33)
                    for i in (1, 2, 4, 2, 3, 4): # extends the output list with the new points
                        o.extend([COLOR, r, g, b, NORMAL, nx[i], ny[i], nz[i], VERTEX, x[i], y[i], z[i]])

                    # Update variables for next loop 
                    V += dV
                # Update variables for next loop 
                U += dU 
        o.append(END)
        return o

def drawEllipsoid(color, cmx, cmy, cmz, a1, a2, a3, R11, R12, R13, R21, R22, R23, R31, R32, R33):
                return makeEllipsoid(color, cmx, cmy, cmz, a1, a2, a3, -90, 90, -180, 180, 10, 10, 
				R11, R12, R13, R21, R22, R23, R31, R32, R33) 

def rotationMatrix(rotationInput): #Elements of the rotation matrix R = transpose of the rotation matrix defined in Arfken's book
    if (len (rotationInput)) == 9: return rotationInput # simply return input if it is already a matrix
    a, b, g = rotationInput[0], rotationInput[1], rotationInput[2]
    R11, R12, R13 = cos(g) * cos(b) * cos(a) - sin(g) * sin(a), -sin(g) * cos(b) * cos(a) - cos(g) * sin(a), sin(b) * cos(a)
    R21, R22, R23 = cos(g) * cos(b) * sin(a) + sin(g) * cos(a), -sin(g) * cos(b) * sin(a) + cos(g) * cos(a), sin(b) * sin(a)
    R31, R32, R33 = -cos(g) * sin(b), sin(g) * sin(b), cos(b)
    return R11, R12, R13, R21, R22, R23, R31, R32, R33
 
#1. Center of Mass of the molecule
cmx, cmy, cmz = 20.051, 6.333, -0.915
#2. Ellipsoid semiaxes length (in Angstrom)
a1,a2,a3 = 21.700, 24.645, 16.567
#3. Color: see https://pymolwiki.org/index.php/Color_Values for more options
color = [0.85, 0.85, 1.00]
#4. Rotation Input: three Euler angles: alpha, beta, gamma (in degrees)
rotationInput = [83.790, 114.370, 179.850]
tmp = drawEllipsoid(color, cmx, cmy, cmz, a1, a2, a3, *rotationMatrix(rotationInput))
cmd.load_cgo(tmp, 'ellipsoid-cgo')
cmd.set('cgo_transparency', 0.5, 'ellipsoid-cgo')