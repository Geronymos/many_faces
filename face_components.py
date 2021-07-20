# https://github.com/google/mediapipe/blob/139237092fedef164a17840aceb4e628244f8173/mediapipe/python/solutions/face_mesh.py

components = {
    "lips": {
        (61, 146),
        (146, 91),
        (91, 181),
        (181, 84),
        (84, 17),
        (17, 314),
        (314, 405),
        (405, 321),
        (321, 375),
        (375, 291),
        (61, 185),
        (185, 40),
        (40, 39),
        (39, 37),
        (37, 0),
        (0, 267),
        (267, 269),
        (269, 270),
        (270, 409),
        (409, 291),
        (78, 95),
        (95, 88),
        (88, 178),
        (178, 87),
        (87, 14),
        (14, 317),
        (317, 402),
        (402, 318),
        (318, 324),
        (324, 308),
        (78, 191),
        (191, 80),
        (80, 81),
        (81, 82),
        (82, 13),
        (13, 312),
        (312, 311),
        (311, 310),
        (310, 415),
        (415, 308),
    },
    "left_eye": {
        (263, 249),
        (249, 390),
        (390, 373),
        (373, 374),
        (374, 380),
        (380, 381),
        (381, 382),
        (382, 362),
        (263, 466),
        (466, 388),
        (388, 387),
        (387, 386),
        (386, 385),
        (385, 384),
        (384, 398),
        (398, 362),
    }, 
    "left_eyebrow": {
        (276, 283),
        (283, 282),
        (282, 295),
        (295, 285),
        (300, 293),
        (293, 334),
        (334, 296),
        (296, 336),
    },
    "right_eye": {
        (33, 7),
        (7, 163),
        (163, 144),
        (144, 145),
        (145, 153),
        (153, 154),
        (154, 155),
        (155, 133),
        (33, 246),
        (246, 161),
        (161, 160),
        (160, 159),
        (159, 158),
        (158, 157),
        (157, 173),
        (173, 133),
    },
    "right_eyebrow": {
        (46, 53),
        (53, 52),
        (52, 65),
        (65, 55),
        (70, 63),
        (63, 105),
        (105, 66),
        (66, 107),
    },
    "face_oval": {
        (10, 338),
        (338, 297),
        (297, 332),
        (332, 284),
        (284, 251),
        (251, 389),
        (389, 356),
        (356, 454),
        (454, 323),
        (323, 361),
        (361, 288),
        (288, 397),
        (397, 365),
        (10, 338),
        (338, 297),
        (297, 332),
        (332, 284),
        (284, 251),
        (251, 389),
        (389, 356),
        (356, 454),
        (454, 323),
        (323, 361),
        (361, 288),
        (288, 397),
        (397, 365),
        (365, 379),
        (379, 378),
        (378, 400),
        (400, 377),
        (377, 152),
        (152, 148),
        (148, 176),
        (176, 149),
        (149, 150),
        (150, 136),
        (136, 172),
        (172, 58),
        (58, 132),
        (132, 93),
        (93, 234),
        (234, 127),
        (127, 162),
        (162, 21),
        (21, 54),
        (54, 103),
        (103, 67),
        (67, 109),
        (365, 379),
        (379, 378),
        (378, 400),
        (400, 377),
        (377, 152),
        (152, 148),
        (148, 176),
        (176, 149),
        (149, 150),
        (150, 136),
        (136, 172),
        (172, 58),
        (58, 132),
        (132, 93),
        (93, 234),
        (234, 127),
        (127, 162),
        (162, 21),
        (21, 54),
        (54, 103),
        (103, 67),
        (67, 109),
        (109, 10)
    }
}

class ConnectionsSwitcher:
  def __init__(self):
    self.states = {
    "every": True,
    "face": True,
    "face_oval": True,
    "lips": True,
    "right_eye": True,
    "left_eye": True,
    "right_eyebrow": True,
    "left_eyebrow": True
    }

    self.face_component_keys = ["face_oval", "lips", "right_eye", "left_eye", "right_eyebrow", "left_eyebrow"]
    self.range_list = [(i, i) for i in range(468)]

  def set_state(self, name, value):
    self.states[name] = value
    if name == "every" or name == "face":
      for key in self.face_component_keys:
        self.states[key] = value

  def switch_state(self, name):
    self.set_state(name, not self.states[name])
    
  def get_combined(self):
    face_component_list = []
    for key in self.face_component_keys:
      if self.states[key]:
        for landmark in [*components[key]]:
          face_component_list.append(landmark)

    return {
      "match": face_component_list,
      "show": self.states["every"] and self.range_list or face_component_list
    }

class LandmarkConverter:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.z = 0
  def from_landmark(self, landmark):
    self.x = landmark.x
    self.y = landmark.y
    self.z = landmark.z
  def from_vertex(self, vertex):
    x,y,z = vertex
    self.x = x
    self.y = y
    self.z = z
  def to_landmark(self):
    normalized_landmark = mp.framework.formats.landmark_pb2.NormalizedLandmark()
    normalized_landmark.x = self.x
    normalized_landmark.y = self.y
    normalized_landmark.z = self.z
    return normalized_landmark
  def to_vertex(self):
    return [self.x, self.y, self.z]

class FaceConverter:
  def __init__(self):
    self.face = []
  def from_face(self, face):
    for landmark in face.landmark:
      landmark_converter = LandmarkConverter()
      landmark_converter.from_landmark(landmark)
      self.face.append(landmark_converter)
  def from_vertices_list(self, vertices_list):
    for vertex in zip(*(iter(vertices_list),) * 3):
      landmark_converter = LandmarkConverter()
      landmark_converter.from_vertex(vertex)
      self.face.append(landmark_converter)
  def to_face(self):
    normalized_landmark_list = mp.framework.formats.landmark_pb2.NormalizedLandmarkList()
    for landmark in self.face:
      normalized_landmark_list.landmark.append(landmark.to_landmark())
    return normalized_landmark_list
  def to_vertices_list(self):
    vertices_list = []
    for landmark in self.face:
      vertices_list.extend(landmark.to_vertex())
    
    return vertices_list
    
class DatasetController:
  def __init__(self):
    self.faces = []

  def important(self, important_components_list):
    pass
    # important_landmarks_dataset = []
    # important_landmarks_webcam = []
    # for important in self.connectionsSwitcher.get_combined()["match"]:
    #   important_landmarks_dataset.append(face_landmarks_list[ important[0] ])
    #   important_landmarks_webcam.extend(self.data[ important[0]*3 : important[0]*3+2 ])
