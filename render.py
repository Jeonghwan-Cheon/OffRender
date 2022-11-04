import open3d as o3d
import numpy as np
import math as m
from PIL import Image

SHAPE = (227, 227)

def offRender(filename, phi, delta, main_viewpoint):
    # Generate mesh object
    mesh = o3d.io.read_triangle_mesh(filename)
    mesh.compute_vertex_normals()

    # Calculate maximum position
    vert_x, vert_y, vert_z = np.swapaxes(np.asarray(mesh.vertices),0,1)
    total_max = 0.5 * (max(vert_x) ** 2 + max(vert_y) ** 2 + max(vert_z) ** 2) ** 0.5

    # Calculate polar position
    x_component = m.cos(m.radians(delta))*m.cos(m.radians(phi + main_viewpoint))
    y_component = m.cos(m.radians(delta))*m.sin(m.radians(phi + main_viewpoint))
    z_component = m.sin(m.radians(delta))

    img_width, img_height = SHAPE

    mat = o3d.visualization.rendering.MaterialRecord()
    # mat.shader = 'defaultUnlit'
    mat.shader = 'defaultLit'

    renderer_pc = o3d.visualization.rendering.OffscreenRenderer(img_width, img_height)
    renderer_pc.scene.set_background(np.array([0, 0, 0, 0]))
    renderer_pc.scene.add_geometry("pcd", mesh, mat)

    # Optionally set the camera field of view (to zoom in a bit)
    vertical_field_of_view = 60  # between 5 and 90 degrees
    aspect_ratio = img_width / img_height  # azimuth over elevation
    near_plane = 0.1
    far_plane = total_max*10
    fov_type = o3d.visualization.rendering.Camera.FovType.Vertical
    renderer_pc.scene.camera.set_projection(vertical_field_of_view, aspect_ratio, near_plane, far_plane, fov_type)

    # Look at the origin from the front (along the -Z direction, into the screen), with Y as Up.
    center = [0, 0, 0]  # look_at target
    mag = 4
    eye = [-total_max*mag*y_component, -total_max*mag*x_component, total_max*mag*z_component]  # camera position
    up = [total_max*y_component, total_max*x_component, total_max*(1-z_component)]  # camera orientation

    renderer_pc.scene.camera.look_at(center, eye, up)
    image = np.asarray(renderer_pc.render_to_image())
    image = Image.fromarray(image).convert("L")
    image = np.asarray(image)

    del mesh, mat, renderer_pc
    return image