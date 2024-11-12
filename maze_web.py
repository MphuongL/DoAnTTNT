from PIL import Image, ImageDraw
import math
from simpleai.search import SearchProblem, astar
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Define the map (the maze)
MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

# Convert map to a list
MAP = [list(x) for x in MAP.split("\n") if x]

# Define cost of moving around the map
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
    "up left": cost_diagonal,
    "up right": cost_diagonal,
    "down left": cost_diagonal,
    "down right": cost_diagonal,
}


# Class containing the methods to solve the maze
class MazeSolver(SearchProblem):
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1
        return (x, y)

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


W = 21  # Width of each grid cell
st.title('Tìm đường trong mê cung')
bg_image = Image.open("maze.bmp")  # Load the maze image

# Draw canvas to allow user to select start and goal
canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.2)",
        stroke_width=5,
        stroke_color="black",
        background_image=bg_image,
        height=210,
        width=630,
        drawing_mode="point"
)

if canvas_result.json_data is not None:
    lst_points = canvas_result.json_data["objects"]
    if len(lst_points) == 2:
        px1 = lst_points[0]['left'] + 3
        py1 = lst_points[0]['top'] + 3
        px2 = lst_points[1]['left'] + 3
        py2 = lst_points[1]['top'] + 3

        x1 = int(px1) // W
        y1 = int(py1) // W

        x2 = int(px2) // W
        y2 = int(py2) // W

        MAP[y1][x1] = 'o'
        MAP[y2][x2] = 'x'

        # Solve the maze
        problem = MazeSolver(MAP)
        result = astar(problem, graph_search=True)

        # Extract the path
        path = [x[1] for x in result.path()]

        # Draw the path on the image
        draw = ImageDraw.Draw(bg_image)  # Create an ImageDraw object to draw on the image

        for point in path:
            px, py = point
            # Convert the grid cell position to pixel coordinates
            x_pixel = px * W + W // 2  # Center the point
            y_pixel = py * W + W // 2
            # Draw a small circle at each path point (you can adjust the size and color)
            draw.ellipse((x_pixel - 2, y_pixel - 2, x_pixel + 2, y_pixel + 2), fill="red")

        # Show the updated image in the Streamlit app
        st.image(bg_image, caption="Mê cung với lộ trình giải quyết", use_column_width=True)