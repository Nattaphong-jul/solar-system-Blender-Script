import bpy
import os
from math import radians
import math 

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def printout(text_content, name = 'text'):
    text_content = str(text_content)
    bpy.ops.object.text_add(location=(0,0,0))
    text = bpy.context.object
    text.data.body = text_content
    text.rotation_euler[0] = radians(90)
    return text


def create_material(name):
    #Create a new material
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    #Clear nodes
    for node in nodes:
        nodes.remove(node)
    
    #Add Principle BSDF
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')


def create_sphere(name, location, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(location=location)
    
    sphere = bpy.context.object
    sphere.name = name
    sphere.scale = (scale, scale, scale)
    
    # Shade smooth
    for poly in sphere.data.polygons:
            poly.use_smooth = True
    return sphere


def apply_img_texture(target_obj, mat_name, img_path, metallic=0.0, roughness=0.5, emit_strength=1.0):
    
    # Create New Material
    myMat = bpy.data.materials.new(name=str(mat_name))
    myMat.use_nodes = True
    nodes = myMat.node_tree.nodes
    links = myMat.node_tree.links
    
    #Clear nodes
    for node in nodes:
        nodes.remove(node)
    
    # Important Texture Node
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    
    # Set Nodes Location
    principled_node.location = (-300, 0)
    texture_node.location = (-600, 0)
    
    # Image Texture
    abs_img_path = bpy.path.abspath(img_path)
    loaded_image = bpy.data.images.load(abs_img_path)
    texture_node.image = loaded_image
    
    target_obj.data.materials.clear() # Clear Texture
    target_obj.data.materials.append(myMat) # Add Texture
    
    # Node Link
    links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    links.new(texture_node.outputs['Color'], principled_node.inputs['Emission Color'])
    
    # BSDF Values Setting
    principled_node.inputs['Metallic'].default_value = metallic
    principled_node.inputs['Roughness'].default_value = roughness
    principled_node.inputs['Emission Strength'].default_value = emit_strength
    
    return myMat

def reset_cursor():
    bpy.context.scene.cursor.location = (0, 0, 0)

# Animation =================================================================
def add_orbit_animation(obj, degrees):
    # Hardcoded frame limit as requested
    end_frame = 140
    
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = end_frame
    
    # Start Frame: Rotation 0
    bpy.context.scene.frame_set(1)
    obj.rotation_euler.z = 0
    obj.keyframe_insert(data_path="rotation_euler", index=2)
    
    # End Frame: Rotation in degrees (converted to radians)
    bpy.context.scene.frame_set(end_frame)
    obj.rotation_euler.z = math.radians(degrees)
    obj.keyframe_insert(data_path="rotation_euler", index=2)

# Stars ============================================================================================================================================
def sun(location, size):
    reset_cursor()
    planet = create_sphere("Sun", location, size)
    apply_img_texture(target_obj=planet, mat_name="Sun", img_path="//texture\\sun\\8k_sun.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # Sun usually rotates too, but if you want it static, remove this line:


def mercury(location, size):
    reset_cursor()
    planet = create_sphere("Mercury", location, size)
    apply_img_texture(target_obj=planet, mat_name="Mercury", img_path="//texture\\mercury\\2k_mercury.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def venus(location, size):
    reset_cursor()
    planet = create_sphere("Venus", location, size)
    apply_img_texture(target_obj=planet, mat_name="Venus", img_path="//texture\\venus\\2k_venus_atmosphere.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def earth(location, size):
    reset_cursor()
    planet = create_sphere("Earth", location, size)
    apply_img_texture(target_obj=planet, mat_name="Earth", img_path="//texture\\earth\\2k_earth_daymap.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def mars(location, size):
    reset_cursor()
    planet = create_sphere("Mars", location, size)
    apply_img_texture(target_obj=planet, mat_name="Mars", img_path="//texture\\mars\\2k_mars.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def jupiter(location, size):
    reset_cursor()
    planet = create_sphere("Jupiter", location, size)
    apply_img_texture(target_obj=planet, mat_name="Jupiter", img_path="//texture\\jupiter\\2k_jupiter.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def saturn(location, size):
    reset_cursor()
    planet = create_sphere("Saturn", location, size)
    apply_img_texture(planet, "Saturn_Mat", "//texture\\saturn\\2k_saturn.jpg")

    outer_radius = size * 2.3
    # Use the passed location, not (0,0,0) so it matches the planet initially
    bpy.ops.mesh.primitive_circle_add(radius=outer_radius, fill_type='NGON', location=location) 
    ring = bpy.context.object
    ring.name = "Saturn_Ring"
    
    bpy.ops.object.mode_set(mode='EDIT')
    inner_radius = size * 1.2 
    inset_amount = outer_radius - inner_radius
    bpy.ops.mesh.inset(thickness=inset_amount)
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    apply_img_texture(ring, "Saturn_Ring_Mat", "//texture\\saturn\\2k_saturn.jpg", emit_strength=0)
    
    bpy.ops.object.select_all(action='DESELECT')
    planet.select_set(True)
    ring.select_set(True)
    bpy.context.view_layer.objects.active = planet
    bpy.ops.object.join()
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)
    return planet

def uranus(location, size):
    reset_cursor()
    planet = create_sphere("Uranus", location, size)
    apply_img_texture(target_obj=planet, mat_name="Uranus", img_path="//texture\\uranus\\2k_uranus.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

def neptune(location, size):
    reset_cursor()
    planet = create_sphere("Neptune", location, size)
    apply_img_texture(target_obj=planet, mat_name="Neptune", img_path="//texture\\neptune\\2k_neptune.jpg", emit_strength=1)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    add_orbit_animation(planet, 360)

# Sun
sun((0, 0, 0), 1392.0)

# Planets
mercury((1500, 0, 0), 4.8)
venus((0, 1550, 0), 12.1)
earth((-1600, 0, 0), 12.7)
mars((0, -1650, 0), 6.8)
jupiter((1400, 1400, 0), 139.8)
saturn((-1800, 1800, 0), 116.5)
uranus((-2100, -2100, 0), 50.7)
neptune((2300, -2300, 0), 49.2)


def apply_hdri(img_path):
    # Get the current world background
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    # Clear nodes
    for node in nodes:
        nodes.remove(node)
    
    # Important Texture Node
    output_node = nodes.new(type='ShaderNodeOutputWorld')
    bg_node = nodes.new(type='ShaderNodeBackground')
    env_tex_node = nodes.new(type='ShaderNodeTexEnvironment')
    
    # Set Nodes Location
    bg_node.location = (0, 0)
    env_tex_node.location = (-300, 0)
    
    # Image Texture
    abs_img_path = bpy.path.abspath(img_path)
    loaded_image = bpy.data.images.load(abs_img_path)
    env_tex_node.image = loaded_image
    
    # Node Link
    links.new(env_tex_node.outputs['Color'], bg_node.inputs['Color'])
    links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])
    
    return world

apply_hdri("//texture\\HDRI\\8k_stars_milky_way.jpg")

# Add the camera
bpy.ops.object.camera_add(location=(8000, -8000, 7500))
cam = bpy.context.object
cam.name = "Camera"

cam.rotation_euler[0] = math.radians(55)
cam.rotation_euler[1] = math.radians(0)
cam.rotation_euler[2] = math.radians(45)

cam.data.clip_end = 400000

# Set as the Active Camera
bpy.context.scene.camera = cam