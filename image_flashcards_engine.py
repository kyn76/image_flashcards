from PIL import Image, ImageTk
import tkinter as tk
import sys
import random
import argparse
from typing import List

from lib import from_rgb, get_all_image_paths, get_image_caption, resize_image


def display_caption_or_next_image(
        image_widget: tk.Label, 
        counter_widget: tk.Label, 
        caption_widget: tk.Label, 
        action_button: tk.Button, 
        image_caption: str, 
        image_paths: List[str],
) -> None:
    if caption_widget.cget("text") == "":
        display_caption(caption_widget, image_caption)
        action_button.configure(text="Next")
    else:
        display_next_image(image_widget, counter_widget, caption_widget, image_paths)
        action_button.configure(text="Show")



def display_next_image(
        image_widget: tk.Label, 
        counter_widget: tk.Label, 
        caption_widget: tk.Label, 
        image_paths: List[str],
) -> None:
    global image_index
    global image_caption
    nb_images = len(image_paths)
    if image_index >= nb_images:
        # Display "no more image" in image_widget
        image_widget.configure(text="No more image", image=None, compound="center")
        image_widget.image = None
        image_caption = ""
        hide_caption(caption_widget)
    else:
        image_path = image_paths[image_index]
        image_caption = get_image_caption(image_path)
        image_index += 1
        # Load the first image using Pillow
        image = Image.open(image_path)
        # Resize the image if needed
        image_widget.update_idletasks() # update the widget properties
        image_frame_dimensions = (image_widget.master.winfo_width(), image_widget.master.winfo_height())
        resized_image = resize_image(image, image_frame_dimensions)
        # Convert the image for Tkinter
        image_tk = ImageTk.PhotoImage(resized_image)
        # Update image display
        image_widget.configure(image=image_tk)
        image_widget.image = image_tk
        # Hide caption
        hide_caption(caption_widget)
        # Update counter
        counter_widget.configure(text=f"{image_index} / {nb_images}")


def display_caption(caption_widget: tk.Label, image_caption: str) -> None:
    caption_widget.configure(text=image_caption)


def hide_caption(caption_widget: tk.Label) -> None:
    caption_widget.configure(text="")


def main(images_directory: str) -> None:
    global image_index
    global image_caption
    image_index = 0
    image_caption = ""
    font = ('Helvetica', '16')

    image_paths = get_all_image_paths(images_directory)
    random.shuffle(image_paths)
    nb_images = len(image_paths)
    if nb_images == 0:
        print("No image found in", images_directory)
        sys.exit(1)

    # init the window
    window = tk.Tk()
    window.config(bg=COLOR1)
    # set the size of the window (full screen)
    screen_width = window.winfo_screenwidth()               
    screen_height = window.winfo_screenheight()               
    window.geometry("%dx%d" % (screen_width, screen_height))

    # define the heights of GUI sections
    counter_frame_height = (1/10)*screen_height
    image_frame_height = (5/10)*screen_height
    caption_frame_height = (1/10)*screen_height
    button_frame_height = (3/10)*screen_height

    # set the name of the window
    window.title("Memory Flashcards")

    # Counter widget
    counter_frame = tk.Frame(window, width=screen_width, height=counter_frame_height, bg=COLOR2, relief="raised")
    counter_widget = tk.Label(counter_frame, text=f"0 / {nb_images}", bg=COLOR2, fg=COLOR3, padx=10, pady=2, font=font)
    counter_widget.place(relx=0.5, rely=0.5, anchor="center")
    
    # Label widget to display the image
    image_frame = tk.Frame(window, width=screen_width, height=image_frame_height, bg=COLOR2)
    image_widget = tk.Label(image_frame)
    image_widget.place(relx=0.5, rely=0.5, anchor="center")

    # Caption widget
    caption_frame = tk.Frame(window, width=screen_width, height=caption_frame_height, bg=COLOR2)
    caption_widget = tk.Label(caption_frame, text="", font=font, bg=COLOR2, fg=COLOR3)
    caption_widget.place(relx=0.5, rely=0.5, anchor="center")

    # Action button
    button_frame = tk.Frame(window, width=screen_width, height=button_frame_height, bg=COLOR2)
    action_button = tk.Button(button_frame, text="Show", font=font, width=20, height=5, bg=COLOR1, command=lambda: display_caption_or_next_image(image_widget, counter_widget, caption_widget, action_button, image_caption, image_paths))
    action_button.place(relx=0.5, rely=0.5, anchor="center")

    counter_frame.pack(padx=10, pady=5)
    image_frame.pack(padx=10, pady=5)
    caption_frame.pack(padx=10, pady=5)
    button_frame.pack(padx=10, pady=5)

    display_next_image(image_widget, counter_widget, caption_widget, image_paths) # to display the first image
    window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Graphical memory flashcard engine built from a directory containing images.',
    )

    parser.add_argument("images_directory", help="The directory containing images to learn / recognize")
    parser.add_argument("-l", "--light-mode", action="store_true", help="use light mode in graphical interface (in dark mode by default if not set)")
    args = parser.parse_args()

    # set light/dark mode
    if args.light_mode:
        COLOR1 = "dodgerblue4"
        COLOR2 = from_rgb((234,234,234))
        COLOR3 = "black"
    else: # dark mode, default
        COLOR1 = "darkslategray"
        COLOR2 = "black"
        COLOR3 = "white"

    main(args.images_directory)


