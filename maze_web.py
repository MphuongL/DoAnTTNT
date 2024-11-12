import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
from simpleai.search import SearchProblem, astar
from streamlit_drawable_canvas import st_canvas

# Định nghĩa kích thước ô lưới
W = 21
st.title('Tìm đường trong mê cung')

# Tải ảnh nền và kiểm tra tính hợp lệ của ảnh
try:
    bg_image = Image.open("maze.png").convert("RGB")  # Chuyển thành RGB để tránh lỗi alpha
    width, height = bg_image.size
    st.write(f"Kích thước ảnh nền: {width} x {height}")
    img_array = np.array(bg_image)

    if img_array is not None and img_array.size > 0:
        # Sử dụng st_canvas với ảnh nền
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.2)",
            stroke_width=5,
            stroke_color="black",
            background_image=img_array,  # Ảnh nền là mảng NumPy
            height=height,  # Kích thước chiều cao ảnh
            width=width,    # Kích thước chiều rộng ảnh
            drawing_mode="point",
            key="canvas1"
        )
    else:
        st.error("Ảnh nền không hợp lệ!")

except Exception as e:
    st.error(f"Không thể tải ảnh nền: {str(e)}")

# Kiểm tra nếu người dùng đã chọn điểm đầu và điểm cuối
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

        # Cập nhật bản đồ với điểm đầu và điểm cuối
        MAP[y1][x1] = 'o'
        MAP[y2][x2] = 'x'

        # Giải quyết mê cung
        problem = MazeSolver(MAP)
        result = astar(problem, graph_search=True)
        path = [x[1] for x in result.path()]

        # Vẽ lộ trình lên ảnh
        draw = ImageDraw.Draw(bg_image)
        for point in path:
            px, py = point
            x_pixel = px * W + W // 2
            y_pixel = py * W + W // 2
            draw.ellipse((x_pixel - 2, y_pixel - 2, x_pixel + 2, y_pixel + 2), fill="red")

        # Hiển thị lại ảnh với lộ trình đã giải
        st.image(bg_image, caption="Mê cung với lộ trình giải quyết", use_column_width=True)
