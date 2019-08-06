import led_matrix_interface as Jworld


def run_text_scroller(text="hello world"):
    pen = Jworld.Pen(canvas=None)
    matrix = pen.matrix
    font = Jworld.graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = Jworld.graphics.Color(255, 255, 0)
    pos = matrix.width
    my_text = text

    while True:
        matrix.Clear()
        len = Jworld.graphics.DrawText(matrix, font, pos, 10, textColor, my_text)
        pos -= 1
        if pos + len < 0:
            pos = matrix.width

        Jworld.time.sleep(0.05)


# Main function
if __name__ == "__main__":
    run_text_scroller()
