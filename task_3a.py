'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ PB_2931 ]
# Author List:		[ ]
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
known = np.full(36,0,dtype=int)
cost = np.full(36,999,dtype=int)
prev = np.full(36,-1,dtype=int)
que = np.full(36,0,dtype=int)

front,rear,size = 0,0,36

def find_nodes(img):
    node = dict()
    for i in range(7):
        for j in range(7):
            node[chr(65+i)+str(j+1)] = img[94+(j*100):107+(j*100),94+(i*100):107+(i*100)]
    return node

def checkcolor(img,color):
	return all(img[5][5] == color)

def h_roads(img):
    h_r=dict()
    for i in range(5):
        for j in range(6):
            h_r[chr(65+i)+str(j+1)+'-'+chr(65+i+1)+str(j+1)] = img[94+(j*100):107+(j*100),107+(i*100):194+(i*100)]
    return h_r

def v_roads(img):
    v_r=dict()
    for i in range(5):
        for j in range(6):
            v_r[chr(65+j)+str(i+1)+'-'+chr(65+j)+str(i+2)] = img[107+(i*100):194+(i*100),94+(j*100):107+(j*100)]
    return v_r

def nti(n):
	x = int(ord(n[0])-65)
	y = int(n[1])-1

	return (x*6)+y

def itn(n):
	a = str(chr((n//6)+65))
	b = str((n%6)+1)

	return a+b

def am(paths):
    adj = np.zeros([36,36],dtype=int)
    for i in paths.keys():
        for j in paths[i].keys():
            x = nti(i)
            y = nti(j)
            adj[x][y] = 1
            adj[y][x] = 1
    return adj

def dks(x,inp):
	global front,rear,que,cost,known,prev,size
	mini,s = 9999,0
	if known[x]!=1 :
		for i in range(size):
			if inp[x][i] != 0 and (inp[x][i]+cost[x])<cost[i] and i!=x:
				cost[i]=inp[x][i]+cost[x]
				prev[i]=x

		known[x]=1

		for j in range(size):
			if mini>cost[j] and j!=x and known[j] != 1:
				mini = cost[j]
				s = j

		rear += 1
		if rear < size:
			que[rear]=s

	front += 1

	if front<=rear and front<size:
		dks(que[front],inp)

def path(x,y):
	
	patht = []
	patht.append(itn(y))
	global cost,prev
	t = 0
	if cost[y]<9999 and prev[y]>-1 and y!=x:
		t = prev[y]

		while t!=x and prev[t] != -1:
			patht.append(itn(t))
			t = prev[t]
	patht.append(itn(x))
	return patht[::-1]

def get_moves(pathplan,traffic_signal):
    path = pathplan.copy()
    path.insert(0,'00')
    a,b,c='','',''
    d1,d2={},{}
    for i in range(len(path)-2):
        a=str(path[i])
        b=str(path[i+1])
        c=str(path[i+2])
        d1[i] = [a[0],b[0],c[0]]
        d2[i] = [a[1],b[1],c[1]]



    tr=[]
    x=0

    for a in range(len(d1)):
        if a==0:
            if d1[a][1] > d1[a][2]:	
                tr.append('LEFT')
                x=-1
            elif d1[a][1] < d1[a][2]:
                tr.append('RIGHT')
                x=1
            else:
                tr.append('STRAIGHT')

                if d2[a][1]<d2[a][2]:
                    x=-2
                else:
                    x=2

        elif len(set(d1[a])) == 1 or len(set(d2[a])) == 1:
            tr.append('STRAIGHT')

        elif len(set(d1[a][1:])) ==2:
            if(d1[a][1]>d1[a][2]) and x == 2:
                tr.append('LEFT')
                x=-1
            elif(d1[a][1]<d1[a][2]) and x == 2:
                tr.append('RIGHT')
                x=1
            else:
                if(d1[a][1]>d1[a][2]) and x == -2:
                    tr.append('RIGHT')
                    x=-1

                else:
                    tr.append('LEFT')
                    x=1

        else:
            if(d2[a][1]<d2[a][2]) and x == 1:
                tr.append('RIGHT')
                x=-2

            elif(d2[a][1]>d2[a][2]) and x == 1:
                tr.append('LEFT')
                x=2

            else:
                if(d2[a][1]>d2[a][2]) and x == -1:
                    tr.append('RIGHT')
                    x=2

                else:
                    tr.append('LEFT')
                    x=-2

        if (d1[a][2] + d2[a][2]) in traffic_signal:
            tr.append('WAIT_5')

    return tr

##############################################################

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too

	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""
	traffic_signals = []
	start_node = ""
	end_node = ""

	##############	ADD YOUR CODE HERE	##############
	image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	node = find_nodes(image)
	
	traffic_signals = []
	start_node = ""
	end_node = ""
	for key,value in node.items():
		if(checkcolor(value,[255,0,0])):
			traffic_signals.append(key)
		elif(checkcolor(value,[0,255,0])):
			start_node=key
		elif(checkcolor(value,[105,43,189])):
			end_node=key
	##################################################

	return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node
			Eg. : { "D3":{"C3", "E3", "D2", "D4" },
					"D5":{"C5", "D2", "D6" }  }
	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	hra = []
	vra = []
	ra = []

	nodes = find_nodes(image)

	hr = h_roads(image)
	for key,value in hr.items():
		if not (checkcolor(value,[255,255,255])):
			hra.append(key)

	vr = v_roads(image)
	for key,value in vr.items():
		if not (checkcolor(value,[255,255,255])):
			vra.append(key)

	ra = hra + vra
	for i in nodes.keys():
		temp = dict()
		for j in ra:
			if i in j:
				temp[((j.replace(i,"")).replace("-",""))] = 1

		paths[i]=temp

	##################################################

	return paths


def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters

	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[],
	                      "start_node": "E4",
	                      "end_node":"A3",
	                      "paths": {}}
	"""
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters["traffic_signals"],arena_parameters["start_node"],arena_parameters["end_node"] = detect_all_nodes(maze_image)
	arena_parameters["paths"] = detect_paths_to_graph(maze_image)

	##################################################

	return arena_parameters


def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of
	list given below **

	Input Arguments:
	---
	`graph` :	[ numpy array ]
			numpy array of image returned by cv2 library
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']

	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	inp = am(graph)
	n = nti(start)
	e = nti(end)

	cost[n]=0
	prev[n]=-1
	front=rear=0
	que[rear]=n

	dks(n,inp)
	backtrace_path = path(n,e)
	##################################################

	prev
	print(find_nodes(image).keys())
	k=0
	for i in (prev):
		if i == -1:
			k+=1
			continue
		print(itn(k),itn(i),i)
		k+=1
	print(backtrace_path)

	return backtrace_path
  

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']

	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""

	list_moves=[]

	##############	ADD YOUR CODE HERE	##############

	list_moves = (get_moves(paths,traffic_signal))

	##################################################

	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
		

		img_key = 'maze_00' + str(file_num)
		img_file_path = img_dir_path + img_key  + '.png'
		# read image using opencv
		image = cv2.imread(img_file_path)

		# detect the arena parameters from the image
		arena_parameters = detect_arena_parameters(image)
		print('\n============================================')
		print("IMAGE: ", file_num)
		print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

		# path planning and getting the moves
		back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
		moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

		print("PATH PLANNED: ", back_path)
		print("MOVES TO TAKE: ", moves)

		# display the test image
		cv2.imshow("image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
