import prover as p
import interpret as i
import customtkinter as ctk
from PIL import Image, ImageTk
import math
from tkinter import font, CENTER
is_animating= False
end_player=0
current_player = "Blue"
players = ["Blue", "Green", "Yellow", "Red"]
images = {
    "Blue": "blue_impasta.png",
    "Green": "green_impasta.png",
    "Yellow": "yellow_impasta.png",
    "Red": "red_impasta.png"
}

# Sentences stored in a dictionary
player_sentences = {
    "Blue": "",
    "Green": "",
    "Yellow": "",
    "Red": ""
}
def display_sentence(selection):
    """
    Dynamically display the selected sentence.
    :param selection: The sentence option selected from the dropdown.
    """
    # Clear the canvas from previous sentence components
    my_canvas.delete("sentence_widgets")
    load_and_display_sentence_outline()
    # Map sentence options to their respective functions
    sentence_functions = {
        "Sentence 1: I saw <Player> doing <Task> at <Place>": (sentence_option_1, get_values_sentence1),
        "Sentence 2: I was doing <Task> at <Place>": (sentence_option_2, get_values_sentence2),
        "Sentence 3: <Player1> killed <Player2>": (sentence_option_3, get_values_sentence3),
        "Sentence 4: I can't believe <Player> is dead!": (sentence_option_4, get_values_sentence4),
    }

    # Get the corresponding function for the selected sentence
    if selection in sentence_functions:
        sentence_function, submit_function = sentence_functions[selection]

        # Display the sentence components
        sentence_function()

        # Add a Submit button for the selected sentence
        submit_button = ctk.CTkButton(root, text="Submit", command=submit_function,
                                      corner_radius=10, fg_color="#A9A9A9", text_color="white")
        my_canvas.create_window(720, 280, window=submit_button, tags="sentence_widgets")


# Function to animate the first image
def animate_first_image(impasta_image, canvas_impasta_image, first_image_phase=0):
    global is_animating

    if not is_animating:
        return  # Stop animation if the flag is cleared

    # Animation logic
    squish_factor = math.sin(first_image_phase) * 9
    new_width = 270 + squish_factor
    new_height = 300 - squish_factor

    resized_image = impasta_image.resize((int(new_width), int(new_height)), Image.Resampling.LANCZOS)
    tk_image1 = ImageTk.PhotoImage(resized_image)

    # Update the canvas image
    my_canvas.itemconfig(canvas_impasta_image, image=tk_image1)
    my_canvas.image1 = tk_image1

    # Continue to the next frame
    next_phase = first_image_phase + 0.5
    root.after(45, lambda: animate_first_image(impasta_image, canvas_impasta_image, next_phase))





options1 = ["Blue", "Yellow", "Green","Red"]
options2 = ["scan", "swipe card", "flushing leaves", "fix meltdown", "insert code"]
options3 = ["Medbay", "Admin", "Cafeteria", "Reactor", "O2"]
options4 = ["Pink", "Violet", "Brown"]  # victims

combo1 = None
combo2 = None
combo3 = None

font_style = ("Arial", 20)
font_style_combobox = ("Arial", 14)
dropdown_style = {"corner_radius": 10, "fg_color": "#E8E8E8", "text_color": "#4D4D4D"}

# Function to retrieve and print selected values from the dropdowns
def get_values_sentence1():
    print(f"I saw {combo1.get()} doing {combo2.get()} at {combo3.get()}.")
    player_sentences[current_player] = f"I saw {combo1.get()} doing {combo2.get()} at {combo3.get()}"
    switch_player()

def get_values_sentence2():
    print(f"I was doing {combo2.get()} at {combo3.get()}.")
    player_sentences[current_player] = f"I was doing {combo2.get()} at {combo3.get()}"
    switch_player()

def get_values_sentence3():
    print(f"{combo2.get()} killed {combo3.get()}.")
    player_sentences[current_player] = f"{combo2.get()} killed {combo3.get()}"
    switch_player()

def get_values_sentence4():
    print(f"Guys, I can't believe {combo3.get()} is dead!")
    player_sentences[current_player] = f"Guys, I can't believe {combo3.get()} is dead!"
    switch_player()

'''
GLOBAL ROOT AND CANVAS  
'''
root = None
my_canvas = None

def init_ctk():
    global root, my_canvas
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("When impostor is SUS")
    root.geometry("1200x500")

    my_canvas = ctk.CTkCanvas(root, width=1200, height=500, bg="white")
    my_canvas.pack(pady=20)

# Function to load and display the impasta image
def load_and_display_image_impasta(impasta_image_path):
    original_image = Image.open(impasta_image_path)
    resized_image = original_image.resize((270, 300), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_image)

    # Persist image reference
    my_canvas.image1 = tk_image
    canvas_impasta_image = my_canvas.create_image(230, 250, anchor="center", image=tk_image)
    return original_image, canvas_impasta_image

# Function to load and display the sentence outline
def load_and_display_sentence_outline():
    image_path = "sentences.png"  # Replace with your second image path
    original_image2 = Image.open(image_path)
    resized_image2 = original_image2.resize((1200, 600), Image.Resampling.LANCZOS)
    tk_image2 = ImageTk.PhotoImage(resized_image2)
    my_canvas.image2 = tk_image2
    my_image2 = my_canvas.create_image(710, 250, anchor="center", image=tk_image2,tags="sentence_widgets")

def sentence_option_1():
    global combo1, combo2, combo3
    label1 = ctk.CTkLabel(root, text="I saw", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo1 = ctk.CTkComboBox(root, values=options1, **dropdown_style, dropdown_font=font_style_combobox)
    combo1.set("")

    label2 = ctk.CTkLabel(root, text="doing", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo2 = ctk.CTkComboBox(root, values=options2, **dropdown_style, dropdown_font=font_style_combobox)
    combo2.set("")

    label3 = ctk.CTkLabel(root, text="at", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo3 = ctk.CTkComboBox(root, values=options3, **dropdown_style, dropdown_font=font_style_combobox)
    combo3.set("")

    my_canvas.create_window(400, 230, window=label1, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(460, 230, window=combo1, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(615, 230, window=label2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(680, 230, window=combo2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(840, 230, window=label3, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(880, 230, window=combo3, anchor="w",tags="sentence_widgets")

def sentence_option_2():
    global combo2, combo3
    label2 = ctk.CTkLabel(root, text="I was doing", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo2 = ctk.CTkComboBox(root, values=options2, **dropdown_style, dropdown_font=font_style_combobox)
    combo2.set("")

    label3 = ctk.CTkLabel(root, text="at", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo3 = ctk.CTkComboBox(root, values=options3, **dropdown_style, dropdown_font=font_style_combobox)
    combo3.set("")

    my_canvas.create_window(400, 230, window=label2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(520, 230, window=combo2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(680, 230, window=label3, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(720, 230, window=combo3, anchor="w",tags="sentence_widgets")

def sentence_option_3():
    global combo2, combo3
    combo2 = ctk.CTkComboBox(root, values=options1, **dropdown_style, dropdown_font=font_style_combobox)
    combo2.set("")

    label3 = ctk.CTkLabel(root, text="killed", font=font_style, text_color="#4D4D4D", fg_color="white")
    combo3 = ctk.CTkComboBox(root, values=options4, **dropdown_style, dropdown_font=font_style_combobox)
    combo3.set("")

    my_canvas.create_window(500, 230, window=combo2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(680, 230, window=label3, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(770, 230, window=combo3, anchor="w",tags="sentence_widgets")

def sentence_option_4():
    global combo3
    label2 = ctk.CTkLabel(root, text="Guys, I can't believe", font=font_style, text_color="#4D4D4D", fg_color="white")
    label3 = ctk.CTkLabel(root, text="is dead!", font=font_style, text_color="#4D4D4D", fg_color="white")

    combo3 = ctk.CTkComboBox(root, values=options4, **dropdown_style, dropdown_font=font_style_combobox)
    combo3.set("")

    my_canvas.create_window(500, 230, window=label2, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(690, 230, window=combo3, anchor="w",tags="sentence_widgets")
    my_canvas.create_window(850, 230, window=label3, anchor="w",tags="sentence_widgets")



# Function to switch to the next player
def switch_player():
    global current_player
    current_index = players.index(current_player)
    if current_index < len(players) - 1:
        current_player = players[current_index + 1]
    else:
        global end_player
        end_player=1
    global is_animating
    is_animating= False
    recurrent_design()




def recurrent_design():
    global is_animating

    my_canvas.delete("sentence_widgets")
    # Load and display the new image
    image_to_be_animated, canvas_image_impasta = load_and_display_image_impasta(images[current_player])
    load_and_display_sentence_outline()

    # Dropdown for sentence selection
    sentence_options = [
        "Sentence 1: I saw <Player> doing <Task> at <Place>",
        "Sentence 2: I was doing <Task> at <Place>",
        "Sentence 3: <Player1> killed <Player2>",
        "Sentence 4: I can't believe <Player> is dead!"
    ]
    sentence_selector = ctk.CTkComboBox(root, values=sentence_options, width=350, **dropdown_style,
                                        dropdown_font=font_style_combobox)
    sentence_selector.set("Select a Sentence")

    select_button = ctk.CTkButton(root, text="Show Sentence", command=lambda: display_sentence(sentence_selector.get()),
                                  corner_radius=10, fg_color="#4CAF50", text_color="white")

    my_canvas.create_window(600, 150, window=sentence_selector, tags="sentence_widgets")
    my_canvas.create_window(950, 150, window=select_button, tags="sentence_widgets")

    # Stop ongoing animation and start a new one
    is_animating = False  # Stop previous animation
    if end_player==0 :
        root.after(200, lambda: start_animation(image_to_be_animated, canvas_image_impasta))

    else: # this is the end of the sentences
          my_canvas.delete("all")
          i.recieve_sentences_as_strings(player_sentences)
          p.identify_impostor()

def start_animation(image, canvas_image):
        global is_animating
        is_animating = True  # Enable animation
        animate_first_image(image, canvas_image)


def build_design():
    init_ctk()
    recurrent_design()
    root.mainloop()

build_design()
