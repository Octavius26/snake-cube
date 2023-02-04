from solver_back import *

def sum_valid(snake:list,cube_size=3):
	# print(sum(snake)-len(snake) + 1 - cube_size**3)
	E_size = cube_size ** 3
	R_size =  sum(snake)-len(snake) + 1

	print(f"Expeted size = {E_size}, Real size = {R_size} 	",end='')
	if E_size == R_size: print("===> OK")
	else: print("===> Warning")
	return E_size == R_size




import plotly.graph_objs as go


def plot_cube(cube:T_cube,start_point:tuple[int]=None):

	x,y,z = [],[],[]

	N = cube.size
	for i in range(N):
		for j in range(N):
			for k in range(N):
				x.append(i)
				y.append(j)
				z.append(k)

	data = go.Scatter3d(    x=x,y=y,z=z,
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

	data2 = go.Scatter3d(   x=x,y=y,z=z,
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

	data3 = go.Scatter3d(   x=x,y=y,z=z,
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

	data4 = go.Scatter3d(   x=x,y=y,z=z,
							mode='markers',
							marker=dict(size=12,opacity=1,color="#000"))



	xx,yy,zz = cube.end_pointer
	x,y,z = [xx],[yy],[zz]

	data5 = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=18,opacity=0.5,color="#0aa"))


	if start_point is not None :
		xx,yy,zz = start_point
		x,y,z = [xx],[yy],[zz]
	else :
		x,y,z = [],[],[]

	data6 = go.Scatter3d(x=x,y=y,z=z,
						mode='markers',
						marker=dict(size=18,opacity=0.5,color="#0f0"))
	



	layout = go.Layout(margin=dict(l=0,r=0,b=0,t=0))
	fig = go.Figure(data=[data,data2,data3,data4,data5,data6], layout=layout)
	fig.show()
	


# end file