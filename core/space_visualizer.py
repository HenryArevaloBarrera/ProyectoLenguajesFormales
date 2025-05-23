import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_space_graph(graph, route_path=None, planet_coords=None, filename='space_map.png'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar planetas
    for planet, neighbors in graph.items():
        if planet_coords and planet in planet_coords:
            x, y, z = planet_coords[planet]
            ax.scatter(x, y, z, color='blue', s=50)
            ax.text(x, y, z, planet, size=10)

            # Dibujar conexiones
            for neighbor in neighbors:
                if neighbor in planet_coords:
                    nx, ny, nz = planet_coords[neighbor]
                    ax.plot([x, nx], [y, ny], [z, nz], color='gray')

    # Dibujar ruta
    if route_path and planet_coords:
        route_points = [planet_coords[p] for p in route_path if p in planet_coords]
        if len(route_points) >= 2:
            xs, ys, zs = zip(*route_points)
            ax.plot(xs, ys, zs, color='red', linewidth=2, label='Ruta segura')
    
    ax.set_title("Mapa de Planetas y Ruta")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    
    # Guardar la figura en un archivo y cerrar la ventana
    plt.savefig(filename)
    plt.close(fig)
