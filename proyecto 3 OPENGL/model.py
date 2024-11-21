from obj import Obj
from buffer import Buffer

from pygame import image

from OpenGL.GL import *
import glm  # pip install PyGLM
from OpenGL.GL.shaders import compileProgram, compileShader


class Model(object):
    def __init__(self, filename):
        self.objFile = Obj(filename)

        self.translation = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

        self.textures = []

        self.BuildBuffers()

        self.visible = True
        self.shader_program = None
        self.uniforms = {}  

    def SetShaders(self, vertex_shader_source, fragment_shader_source):
        if vertex_shader_source is not None and fragment_shader_source is not None:
            vertex_shader = compileShader(
                vertex_shader_source, GL_VERTEX_SHADER)
            fragment_shader = compileShader(
                fragment_shader_source, GL_FRAGMENT_SHADER)
            self.shader_program = compileProgram(vertex_shader, fragment_shader)
        else:
            self.shader_program = None

    def SetUniform(self, name, value):
        self.uniforms[name] = value

    def GetModelMatrix(self):
        # M = T * R * S
        # R = pitch * yaw * roll

        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.translation)

        pitchMat = glm.rotate(identity, glm.radians(
            self.rotation.x), glm.vec3(1, 0, 0))
        yawMat = glm.rotate(identity, glm.radians(
            self.rotation.y), glm.vec3(0, 1, 0))
        rollMat = glm.rotate(identity, glm.radians(
            self.rotation.z), glm.vec3(0, 0, 1))

        rotationMat = pitchMat * yawMat * rollMat

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def BuildBuffers(self):

        positions = []
        texCoords = []
        normals = []
        tangents = []

        self.vertexCount = 0

        for face in self.objFile.faces:

            facePositions = []
            faceTexCoords = []
            faceNormals = []

            for i in range(len(face)):
                facePositions.append(
                    self.objFile.vertices[face[i][0] - 1])
                faceTexCoords.append(
                    self.objFile.texCoords[face[i][1] - 1])
                faceNormals.append(
                    self.objFile.normals[face[i][2] - 1])

            # tangent
            deltaPos1 = glm.sub(glm.vec3(
                facePositions[1]), glm.vec3(facePositions[0]))
            deltaPos2 = glm.sub(glm.vec3(
                facePositions[2]), glm.vec3(facePositions[0]))
            deltaUV1 = glm.sub(glm.vec2(
                faceTexCoords[1]), glm.vec2(faceTexCoords[0]))
            deltaUV2 = glm.sub(glm.vec2(
                faceTexCoords[2]), glm.vec2(faceTexCoords[0]))

            try:
                r = 1.0 / (deltaUV1.x * deltaUV2.y -
                           deltaUV1.y * deltaUV2.x)
                tangent = (deltaPos1 * deltaUV2.y -
                           deltaPos2 * deltaUV1.y) * r
            except:
                continue

            for value in facePositions[0]:
                positions.append(value)
            for value in faceTexCoords[0]:
                texCoords.append(value)
            for value in faceNormals[0]:
                normals.append(value)
            for value in tangent:
                tangents.append(value)

            for value in facePositions[1]:
                positions.append(value)
            for value in faceTexCoords[1]:
                texCoords.append(value)
            for value in faceNormals[1]:
                normals.append(value)
            for value in tangent:
                tangents.append(value)

            for value in facePositions[2]:
                positions.append(value)
            for value in faceTexCoords[2]:
                texCoords.append(value)
            for value in faceNormals[2]:
                normals.append(value)
            for value in tangent:
                tangents.append(value)

            self.vertexCount += 3

            if len(face) == 4:
                for value in facePositions[0]:
                    positions.append(value)
                for value in faceTexCoords[0]:
                    texCoords.append(value)
                for value in faceNormals[0]:
                    normals.append(value)
                for value in tangent:
                    tangents.append(value)

                for value in facePositions[2]:
                    positions.append(value)
                for value in faceTexCoords[2]:
                    texCoords.append(value)
                for value in faceNormals[2]:
                    normals.append(value)
                for value in tangent:
                    tangents.append(value)

                for value in facePositions[3]:
                    positions.append(value)
                for value in faceTexCoords[3]:
                    texCoords.append(value)
                for value in faceNormals[3]:
                    normals.append(value)
                for value in tangent:
                    tangents.append(value)

                self.vertexCount += 3

        self.positionBuffer = Buffer(positions)
        self.texCoordsBuffer = Buffer(texCoords)
        self.normalsBuffer = Buffer(normals)
        self.tangentBuffer = Buffer(tangents)

    def AddTexture(self, textureFilename):

        textureSurface = image.load(textureFilename)
        textureData = image.tostring(textureSurface, "RGB", True)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(GL_TEXTURE_2D, 
                     0,  
                     GL_RGB,  
                     textureSurface.get_width(),  
                     textureSurface.get_height(),  
                     0, 
                     GL_RGB,  
                     GL_UNSIGNED_BYTE,  
                     textureData)  

        glGenerateMipmap(GL_TEXTURE_2D)

        self.textures.append(texture)

    def Render(self, camera, time, pointLight, ambientLight):
        if not self.visible:
            return

        if self.shader_program is not None:
            glUseProgram(self.shader_program)

            # Set standard uniforms
            glUniform1f(glGetUniformLocation(
                self.shader_program, "time"), time)
            glUniform1i(glGetUniformLocation(
                self.shader_program, "tex0"), 0)
            glUniform1i(glGetUniformLocation(
                self.shader_program, "tex1"), 1)

            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "modelMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.GetModelMatrix()))
            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(camera.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(camera.projectionMatrix))

            glUniform3fv(glGetUniformLocation(
                self.shader_program, "pointLight"), 1, glm.value_ptr(pointLight))
            glUniform1f(glGetUniformLocation(
                self.shader_program, "ambientLight"), ambientLight)
            glUniform3fv(glGetUniformLocation(
                self.shader_program, "cameraPos"), 1, glm.value_ptr(camera.position))
            glUniform3fv(glGetUniformLocation(
                self.shader_program, "scale"), 1, glm.value_ptr(self.scale))

            # Set custom uniforms
            for name, value in self.uniforms.items():
                location = glGetUniformLocation(self.shader_program, name)
                if location != -1:
                    if isinstance(value, float):
                        glUniform1f(location, value)
                    elif isinstance(value, int):
                        glUniform1i(location, value)
                    elif isinstance(value, glm.vec2):
                        glUniform2fv(location, 1, glm.value_ptr(value))
                    elif isinstance(value, glm.vec3):
                        glUniform3fv(location, 1, glm.value_ptr(value))
                    elif isinstance(value, glm.vec4):
                        glUniform4fv(location, 1, glm.value_ptr(value))
                    elif isinstance(value, glm.mat4):
                        glUniformMatrix4fv(
                            location, 1, GL_FALSE, glm.value_ptr(value))
                    else:
                        print(
                            f"Uniform '{name}' has unsupported type '{type(value)}'")
                else:
                    print(f"Uniform '{name}' not found in shader.")
        else:
            glUseProgram(0)  

        for i in range(len(self.textures)):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, self.textures[i])

        self.positionBuffer.Use(0, 3)
        self.texCoordsBuffer.Use(1, 2)
        self.normalsBuffer.Use(2, 3)
        self.tangentBuffer.Use(3, 3)

        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
