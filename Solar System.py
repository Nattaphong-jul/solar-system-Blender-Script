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


def apply_img_texture(target_obj, mat_name, img_path, metallic_val=0.0, roughness_val=0.5, emit_strength=1.0):
    
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
    principled_node.inputs['Metallic'].default_value = metallic_val
    principled_node.inputs['Roughness'].default_value = roughness_val
    principled_node.inputs['Emission Strength'].default_value = emit_strength
    
    return myMat


def jupiter():
    planet = create_sphere("Jupiter", (110,0,0), (139.8))
    
    apply_img_texture(target_obj=planet, mat_name="Jupiter", img_path="//texture\\jupiter\\2k_jupiter.jpg")


jupiter()


def apply_hdri(hdri_path):
    """
    Applies an HDRI image to the current scene's world background.
    """
    # 1. Get the current world (or create one if none exists)
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    
    # 2. Enable 'Use Nodes'
    world.use_nodes = True
    node_tree = world.node_tree
    nodes = node_tree.nodes
    links = node_tree.links
    
    # 3. Clear existing nodes to start fresh
    nodes.clear()
    
    # 4. Create the necessary nodes
    # Texture Coordinate (for mapping, useful if you want to rotate later)
    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    tex_coord_node.location = (-600, 0)
    
    # Mapping (to rotate the HDRI)
    mapping_node = nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (-400, 0)
    
    # Environment Texture (This holds the HDRI image)
    env_tex_node = nodes.new(type='ShaderNodeTexEnvironment')
    env_tex_node.location = (-200, 0)
    
    # Background Node
    bg_node = nodes.new(type='ShaderNodeBackground')
    bg_node.location = (0, 0)
    
    # World Output Node
    output_node = nodes.new(type='ShaderNodeOutputWorld')
    output_node.location = (200, 0)
    
    # 5. Load the HDRI Image
    if os.path.exists(hdri_path):
        try:
            img = bpy.data.images.load(hdri_path)
            env_tex_node.image = img
        except:
            print(f"Could not load image at {hdri_path}")
    else:
        print(f"File not found: {hdri_path}")
        return

    # 6. Link the nodes together
    # TexCoord -> Mapping
    links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
    # Mapping -> Environment Texture
    links.new(mapping_node.outputs["Vector"], env_tex_node.inputs["Vector"])
    # Environment Texture -> Background
    links.new(env_tex_node.outputs["Color"], bg_node.inputs["Color"])
    # Background -> Output
    links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])

    print("HDRI Setup Complete.")

# --- USAGE ---
# Replace this path with the actual path to your .exr or .hdr file
# Note: On Windows, use r"Path" or double backslashes \\
my_hdri_path = r"S:\Google Drive\3D\Solar System\texture\HDRI\8k_stars_milky_way.jpg"

apply_hdri(my_hdri_path)