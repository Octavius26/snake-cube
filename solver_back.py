import numpy as np
from typing import Literal






T_direction = Literal['x','-x','y','-y','z','-z']


def sum_valid(snake:list,cube_size=3):
    return sum(snake)-len(snake) + 1 == cube_size ** 3

class T_cube :
    def __init__(self,  M:np.ndarray,
                        end_pointer:tuple[int],
                        prev_dir : T_direction = None,
                        list_dir : list[T_direction] = None,
                        size : int = 3 ) -> None:

        if list_dir is None : list_dir = []

        self.list_dir = list_dir
        self.M = M
        self.end_pointer = end_pointer
        self.prev_dir = prev_dir
        self.size = size

    def copy(self):
        return T_cube(  M=self.M.copy(),
                        end_pointer=self.end_pointer,
                        prev_dir=self.prev_dir,
                        list_dir=self.list_dir.copy())




def dir_possibilities( cube:T_cube,
                        line:int):
    """
    Return the possibilities list for a given line on a cube wich end at end_pointer
    """
    prev_dir = cube.prev_dir
    end = cube.end_pointer
    poss = []                    
    size = cube.size
    if prev_dir not in ['x','-x']:
        if 0 <= end[0] + line - 1 < size : poss.append('x')
        if 0 <= end[0] - line + 1 < size : poss.append('-x')
                        
    if prev_dir not in ['y','-y']:
        if 0 <= end[1] + line - 1 < size : poss.append('y')
        if 0 <= end[1] - line + 1 < size : poss.append('-y')
                        
    if prev_dir not in ['z','-z']:
        if 0 <= end[2] + line - 1 < size : poss.append('z')
        if 0 <= end[2] - line + 1 < size : poss.append('-z')
    
    return poss





def add_to_cube(cube:T_cube,line,dir) -> tuple[bool,T_cube]:
    cube__ = cube.copy()


    M = cube__.M
    x,y,z = cube__.end_pointer
    match dir :
        case 'x':
            for i in range(1,line): M[x+i][y][z] += 1
            cube__.end_pointer = (x+(line-1),y,z)
        case '-x':
            for i in range(1,line): M[x-i][y][z] += 1
            cube__.end_pointer = (x-(line-1),y,z)
        case 'y':
            for i in range(1,line): M[x][y+i][z] += 1
            cube__.end_pointer = (x,y+(line-1),z)
        case '-y':
            for i in range(1,line): M[x][y-i][z] += 1
            cube__.end_pointer = (x,y-(line-1),z)
        case 'z':
            for i in range(1,line): M[x][y][z+i] += 1
            cube__.end_pointer = (x,y,z+(line-1))
        case '-z':
            for i in range(1,line): M[x][y][z-i] += 1
            cube__.end_pointer = (x,y,z-(line-1))
        case _ :
            raise ValueError()
    cube__.list_dir.append(dir)
    return (False, None) if 2 in M else (True, cube__)



class result :
    minimum_len : int
    cube_sol : T_cube

debug = True

def rec_solver( cube : T_cube,
                snake : list[int],
                minimal_len : int) -> bool:
    """
    Return
    ------
    `sol_found` : bool
    `cube_sol` : T_cube | None
    `minimum_len` : int
    """
    
    if snake == [] :
        print("Solution")
        return True,cube,0

    snake = snake.copy()
    line = snake.pop(0)
    l_new_dir = dir_possibilities(cube,line)

    N = len(snake)
    if N < minimal_len :
        print(N)
        minimal_len = N
    # else : print("=>",N)

    cube_sol = None
    for dir in l_new_dir:
        test_ok,new_cube = add_to_cube(cube,line,dir)
        if test_ok: 
            # new_cube.list_dir.append(dir)
            sol_found,cube_sol,minimal_len_2 = rec_solver(new_cube, snake,minimal_len)
            if minimal_len_2 < minimal_len :
                minimal_len = minimal_len_2
            if sol_found :
                return True,cube_sol,0
    if l_new_dir == [] : print(".",end='')
    if cube_sol is None :
        return False,cube,minimal_len
    return False,cube_sol,minimal_len_2


def solve(snake:list[int],size,start_point = (0,0,0))->T_cube:
    cube_init = T_cube( M = np.zeros((size,size,size), dtype=np.int8),
                    end_pointer = start_point,
                    prev_dir=None,
                    size=size)
    x,y,z = start_point
    cube_init.M[x,y,z] = 1
    sol_found,cube_sol,minimum_len = rec_solver(cube_init,snake,len(snake))
    return cube_sol




import plotly.graph_objs as go

def plot_cube(cube:T_cube):

	x,y,z = [],[],[]

	N = cube.size
	for i in range(N):
		for j in range(N):
			for k in range(N):
				x.append(i)
				y.append(j)
				z.append(k)

	data = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=12,opacity=0.8,color="#555"))
	
	x,y,z = [],[],[]

	N = cube.size
	for i in range(N):
		for j in range(N):
			for k in range(N):
				if cube.M[i,j,k] == 1:
					x.append(i)
					y.append(j)
					z.append(k)

	data2 = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=12,opacity=0.5,color="#0a0"))
	
	x,y,z = [],[],[]

	N = cube.size
	for i in range(N):
		for j in range(N):
			for k in range(N):
				if cube.M[i,j,k] == 2 :
					x.append(i)
					y.append(j)
					z.append(k)

	data3 = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=12,opacity=0.5,color="#f00"))
	

		
	x,y,z = [],[],[]

	N = cube.size
	for i in range(N):
		for j in range(N):
			for k in range(N):
				if cube.M[i,j,k] < 0 or cube.M[i,j,k] > 2:
					x.append(i)
					y.append(j)
					z.append(k)

	data4 = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=12,opacity=1,color="#000"))
	
	
	
	layout = go.Layout(margin=dict(l=0,r=0,b=0,t=0))
	fig = go.Figure(data=[data,data2,data3,data4], layout=layout)
	fig.show()