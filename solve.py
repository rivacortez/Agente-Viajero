import tkinter as tk
from tkinter import messagebox
import random
import networkx as nx
import matplotlib.pyplot as plt
asdasdsads

def generar_matriz(n):
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = random.randint(1, 100)
            matriz[j][i] = matriz[i][j]
    return matriz


def calcular_distancia_total(camino, distancias):
    distancia_total = 0
    for i in range(len(camino) - 1):
        distancia_total += distancias[camino[i]][camino[i + 1]]
    return distancia_total


def resolver_tsp():
    n = int(entry_n.get())
    if n < 5 or n > 15:
        messagebox.showerror("Error", "El valor de 'n' debe estar entre 5 y 15.")
        return

    distancias = []
    for i in range(n):
        fila = []
        for j in range(n):
            valor = entry_matrix[i][j].get()
            fila.append(int(valor))
        distancias.append(fila)

    result_label.config(text="solving ...")
    root.update_idletasks()

    ciudad_inicial = 0  
    visitadas = [False] * n
    camino = [ciudad_inicial]
    visitadas[ciudad_inicial] = True

    for _ in range(n - 1):
        ciudad_actual = camino[-1]
        ciudad_mas_cercana = None
        distancia_minima = float("inf")

        for ciudad in range(n):
            if not visitadas[ciudad] and distancias[ciudad_actual][ciudad] < distancia_minima:
                ciudad_mas_cercana = ciudad
                distancia_minima = distancias[ciudad_actual][ciudad]

        camino.append(ciudad_mas_cercana)
        visitadas[ciudad_mas_cercana] = True

    camino.append(ciudad_inicial)
    distancia_total = calcular_distancia_total(camino, distancias)

    result_label.config(text=f"Ciclo hamiltoniano: {camino}\nDistancia total: {distancia_total}")


    
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distancias[i][j])

   
    optimal_hamiltonian_path = camino  

   
    H = G.copy()
    for u, v in G.edges():
        H[u][v]['selected'] = False

    for i in range(len(optimal_hamiltonian_path) - 1):
        u, v = optimal_hamiltonian_path[i], optimal_hamiltonian_path[i + 1]
        H[u][v]['selected'] = True
        H[v][u]['selected'] = True

    pos = nx.spring_layout(G)  

    
    edge_colors = ['red' if H[u][v]['selected'] else 'black' for u, v in H.edges()]
    labels = nx.get_edge_attributes(H, "weight")
    nx.draw(H, pos, with_labels=True, node_size=500, font_size=10, font_color="black", edge_color=edge_colors)
    nx.draw_networkx_edge_labels(H, pos, edge_labels=labels)
    plt.show()

def generar_matriz_y_mostrar():
    n = int(entry_n.get())
    distancias = generar_matriz(n)

    for i in range(n):
        for j in range(n):
            entry_matrix[i][j].delete(0, tk.END)
            entry_matrix[i][j].insert(0, str(distancias[i][j]))


def limpiar_matriz():
    for i in range(len(entry_matrix)):
        for j in range(len(entry_matrix[i])):
            entry_matrix[i][j].delete(0, tk.END)


def cerrar_programa():
    root.destroy()


root = tk.Tk()
root.title("Agente Viajero")

label_n = tk.Label(root, text="Ingrese la cantidad de vertices en el rango (5,15)")
label_n.pack()

entry_n = tk.Entry(root)
entry_n.pack()

matrix_frame = tk.Frame(root)
matrix_frame.pack()

entry_matrix = []
for i in range(15):
    fila_entradas = []
    for j in range(15):
        entrada = tk.Entry(matrix_frame, width=5)
        entrada.grid(row=i, column=j)
        fila_entradas.append(entrada)
    entry_matrix.append(fila_entradas)

generar_button = tk.Button(root, text="Generar Matriz", command=generar_matriz_y_mostrar)
generar_button.pack()

limpiar_button = tk.Button(root, text="Limpiar Matriz", command=limpiar_matriz)
limpiar_button.pack()

resolver_button = tk.Button(root, text="Aplicar algoritmo", command=resolver_tsp)
resolver_button.pack()

result_label = tk.Label(root, text="", wraplength=300)
result_label.pack()

cerrar_button = tk.Button(root, text="Delete", command=cerrar_programa, bg="red", fg="white")
cerrar_button.pack()

root.mainloop()
