from flask import Flask, render_template, request
import time
import sys


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/min_span_trees', methods=['GET', 'POST'])
def min_span_trees():
    try:
        start_time = time.time()*1000000
        val = request.form['val']
        tree_nodes = list(map(int, list(val.split(","))))
        print(tree_nodes)
        print(sum(tree_nodes))
        if len(tree_nodes) % 3 != 0:
            return render_template("index.html", error='Please Enter Numeric Values for Vertices and Distance.')

        mst1, mst_edges1 = kruskal_algo(tree_nodes)
        rt1 = time.time()*1000000 - start_time

        #start_time = time.time()
        mst2, mst_edges2, graph_array, total_vertices = prims_algo(tree_nodes)
        rt2 = time.time()*1000000 - start_time

        return render_template('min_span_trees.html', data=tree_nodes, mst1=mst1, rt1=rt1/1000000, mst2=mst2, rt2=rt2/1000000, mst_edges1=mst_edges1, mst_edges2=mst_edges2, graph_array=graph_array, total_vertices=total_vertices)

    except Exception as e:
        print(e)
        return render_template("index.html", error="Please Enter Numeric Values for Vertices and Distance.")


def kruskal_algo(inp):
    try:
        vertices = []
        for i in range(int(len(inp) / 3)):
            j = i * 3
            if inp[j] not in vertices:
                vertices.append(inp[i])
            if inp[j + 1] not in vertices:
                vertices.append(inp[j + 1])
        vertices.sort()
        total_vertices = len(vertices)
        graph_array = [[0] * total_vertices for _ in range(total_vertices)]
        g = kruskal_graph(total_vertices)
        for i in range(int(len(inp) / 3)):
            j = i * 3
            g.insert_edges(vertices.index(inp[j]), vertices.index(inp[j + 1]), inp[j + 2])
        mst = g.kruskal_algorithm()
        print(mst)
        return mst

    except Exception as e:
        print(e)
        return render_template("index.html", error=e)


class kruskal_graph:
    def __init__(self, ver):
        self.vertex = ver
        self.kruskalGraph = []

    def insert_edges(self, source, destination, weight):
        self.kruskalGraph.append([source, destination, weight])

    def find_edges(self, parent, t):
        if parent[t] == t:
            return t
        return self.find_edges(parent, parent[t])

    def merge_graph(self, parent, index, a, b):
        r1 = self.find_edges(parent, a)
        r2 = self.find_edges(parent, b)
        if index[r1] > index[r2]:
            parent[r2] = r1
        elif index[r2] > index[r1]:
            parent[r1] = r2
        else:
            index[r1] += 1
            parent[r2] = r1

    def kruskal_algorithm(self):
        ans = []
        i, e = 0, 0
        self.kruskalGraph = sorted(self.kruskalGraph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.vertex):
            parent.append(node)
            rank.append(0)
        while self.vertex - 1 > e:
            u, v, w = self.kruskalGraph[i]
            i = i + 1
            x = self.find_edges(parent, u)
            y = self.find_edges(parent, v)
            if x != y:
                e = e + 1
                ans.append([u, v, w])
                self.merge_graph(parent, rank, x, y)
        mst = 0
        mst_edges = []
        for u, v, weight in ans:
            mst_edges.append(str(u)+'  -  '+str(v) + ' :  ' + str(weight))
            #print("Edge:", u, v, end=" ")
            #print("-", weight)
            mst += weight
        print(mst_edges)
        return mst, mst_edges


def prims_algo(inp):
    try:
        vertices = []
        for i in range(int(len(inp) / 3)):
            j = i * 3
            if inp[j] not in vertices:
                vertices.append(inp[i])
            if inp[j + 1] not in vertices:
                vertices.append(inp[j + 1])
        vertices.sort()
        total_vertices = len(vertices)
        graph_array = [[0] * total_vertices for _ in range(total_vertices)]
        for i in range(int(len(inp) / 3)):
            j = i * 3
            graph_array[vertices.index(inp[j])][vertices.index(inp[j + 1])] = inp[j + 2]
            graph_array[vertices.index(inp[j + 1])][vertices.index(inp[j])] = inp[j + 2]
        select_vertices = [0] * total_vertices
        e = 0
        select_vertices[0] = True
        mst = 0
        mst_edges = []
        while e < total_vertices - 1:
            min_val = sys.maxsize
            a = 0
            b = 0
            for m in range(total_vertices):
                if select_vertices[m]:
                    for n in range(total_vertices):
                        if (not select_vertices[n]) and graph_array[m][n]:
                            if graph_array[m][n] < min_val:
                                min_val = graph_array[m][n]
                                a = m
                                b = n
            #print(str(a) + "-" + str(b) + ":" + str(graph_array[a][b]))
            mst_edges.append(str(a)+'  -  '+str(b) + ' :  ' + str(graph_array[a][b]))
            mst += graph_array[a][b]
            select_vertices[b] = True
            e += 1
        print(mst_edges)
        return mst, mst_edges, graph_array, total_vertices
    except Exception as e:
        print(e)
        return render_template("index.html", error=e)


if __name__ == '__main__':
    app.run()
