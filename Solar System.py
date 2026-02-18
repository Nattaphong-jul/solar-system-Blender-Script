import bpy
import random
import os
from math import radians

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

def jupiter():
    planet = create_sphere("Jupiter", (110,0,0), (139.8))
    
    apply_img_texture(target_obj=planet, mat_name="Jupiter", img_path="//texture\\jupiter\\2k_jupiter.jpg", emit_strength=1)

jupiter()


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