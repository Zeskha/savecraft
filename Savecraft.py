import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, ttk, font
import pyshortcuts as ps
from ctypes import windll
from PIL import Image
import datetime
import webbrowser

class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("900x450")
        self.pack()
        self.create_widgets(font)
        self.load_saved_paths()
        
        self.file_type = 'file'
        self.date = False
        self.shortcut = False

    def create_widgets(self, letter_font):
        # Creates the GUI
        self.top_menu = tk.Menu(root)
        root.config(menu=self.top_menu)

        self.options_menu = tk.Menu(self.top_menu, tearoff=0)
        self.options_menu.add_command(label="Settings        ",
                                      command=lambda: self.settings_floating_window(letter_font),
                                      font=(letter_font, 13))

        self.options_menu.add_separator()
        self.options_menu.add_command(label="Exit           ",
                                      command=root.quit, font=(letter_font, 13))

        self.info_menu = tk.Menu(self.top_menu, tearoff=0)
        self.info_menu.add_command(label="Info          ",
                                   command=lambda: webbrowser.open_new("https://github.com/Zeskha/savecraft/blob/main/README.md"),
                                   font=(letter_font, 13))
        self.info_menu.add_command(label="More           ",
                                   command=lambda: webbrowser.open_new("https:/github.com/Zeskha?tab=repositories"),
                                   font=(letter_font, 13))

        self.top_menu.add_cascade(label="Settings", menu=self.options_menu)
        self.top_menu.add_cascade(label='Info', menu=self.info_menu)

        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=(75, 0))

        self.group1_frame = tk.Frame(self.top_frame)
        self.group1_frame.pack()

        self.browse_label_frame = tk.Frame(self.group1_frame)
        self.browse_label_frame.pack()

        self.browse_button_frame = tk.Frame(self.group1_frame)
        self.browse_button_frame.pack(side="left")

        self.browse_label = tk.Label(self.browse_label_frame, text="Select world", anchor='w', font=(letter_font, 15))
        self.browse_label.pack(side="left")

        self.browse_button = tk.Button(self.browse_button_frame, text="Browse", command=self.browse_world_path,
                                       font=(letter_font, 14), borderwidth=3)
        self.browse_button.pack(side="left")

        self.path_entry_frame = tk.Frame(self.group1_frame)
        self.path_entry_frame.pack(side="left")

        self.path_entry = tk.Entry(self.path_entry_frame, width=50, state='readonly',
                                   font=(letter_font, 14), borderwidth=2)
        self.path_entry.pack()

        self.group2_frame = tk.Frame(self.top_frame)
        self.group2_frame.pack(pady=(75, 15))  # Aumentamos la distancia entre los grupos

        self.browse_label_frame2 = tk.Frame(self.group2_frame)
        self.browse_label_frame2.pack()

        self.browse_button_frame2 = tk.Frame(self.group2_frame)
        self.browse_button_frame2.pack(side="left")

        self.browse_label2 = tk.Label(self.browse_label_frame2, text="Select location", anchor='w',
                                      font=(letter_font, 15))
        self.browse_label2.pack(side="left")

        self.browse_button2 = tk.Button(self.browse_button_frame2, text="Browse", command=self.browse_target_path,
                                        font=(letter_font, 14), borderwidth=3)
        self.browse_button2.pack(side="left")

        self.path_entry_frame2 = tk.Frame(self.group2_frame)
        self.path_entry_frame2.pack(side="left")

        self.path_entry2 = tk.Entry(self.path_entry_frame2, width=50, state='readonly',
                                    font=(letter_font, 14), borderwidth=2)
        self.path_entry2.pack()

        self.accept_button_frame = tk.Frame(self.master, padx=7.5, pady=7.5)
        self.accept_button_frame.pack(side="bottom", fill="x")

        self.progress_bar = tk.ttk.Progressbar(self.accept_button_frame, orient="horizontal", length=300,
                                               mode="determinate")
        self.progress_bar.pack(side="left", fill='x', expand=True, padx=(0, 7.5))

        self.accept_button = tk.Button(self.accept_button_frame, text="Run",
                                       command=lambda: self.copy_world_start(self.path_entry.get(),
                                                                             self.path_entry2.get()),
                                       width=15, font=(letter_font, 15), borderwidth=3)
        self.accept_button.pack(side="right")

    def settings_floating_window(self, letter_font):
        def display_information_text(event):
            if event.type == '7':
                if event.widget == date_cb:
                    info_label.place(x=date_cb.winfo_x(), y=date_cb.winfo_y()+37)
                    upper_canva.place(x=date_cb.winfo_x()-4, y=date_cb.winfo_y() + 30)
                    info_label.config(text='If the checkbox is selected, this will add the date to the name '
                                           'of the world file (This will cause longer copying time if folder selected)'
                                           '(dd-mm-yyyy).')

                elif event.widget == shortcut_cb:
                    info_label.place(x=shortcut_cb.winfo_x(), y=shortcut_cb.winfo_y() + 37)
                    upper_canva.place(x=shortcut_cb.winfo_x()-4, y=shortcut_cb.winfo_y() + 30)
                    info_label.config(text='If the checkbox is selected, this will create a shortcut in the desktop '
                                           'for saving the world automatically with selected settings.')
            elif event.type == '8':
                actual = floating_window.after(1000, display_information_text, event)
                num = int(actual[6:]) - 1
                floating_window.after_cancel(actual)
                floating_window.after_cancel(f'after#{num}')
                info_label.place_forget()
                upper_canva.place_forget()

        def save_variables():
            if combo.get() == 'Folder':
                self.file_type = 'folder'
            elif combo.get() == 'Zipped folder':
                self.file_type = 'zfolder'
            if date.get() is False:
                self.date = False
            elif date.get() is True:
                self.date = True
            if shortcut.get() is False:
                self.shortcut = False
            elif shortcut.get() is True:
                self.shortcut = True

            floating_window.unbind('<Destroy>')

        floating_window = tk.Toplevel(root)
        floating_window.title("Settings")
        floating_window.grab_set()
        floating_window.transient(root)
        floating_window.protocol("WM_DELETE_WINDOW", floating_window.destroy)
        floating_window.geometry('500x300')
        floating_window.update()

        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # Calculate the x and y coordinates to center the floating window
        x_coordinate = root.winfo_x() + (root_width - 500) // 2
        y_coordinate = root.winfo_y() + (root_height - 250) // 2

        # Set the geometry of the floating window
        floating_window.geometry(f"+{x_coordinate}+{y_coordinate}")

        title = ttk.Label(floating_window, text='Saving format:          ', padding=(0, 45, 165, 5),
                          font=(letter_font, 16))
        title.pack()

        save_options = ["Folder", "Zipped folder"]
        combo = ttk.Combobox(floating_window, state='readonly', values=save_options, font=(letter_font, 14),
                             width=30, height=10)
        combo.set(save_options[0])
        combo.pack()
        floating_window.option_add('*TCombobox*Listbox.font', (letter_font, 13))

        spacing1 = ttk.Label(floating_window, text='')
        spacing1.pack()

        date = tk.BooleanVar()
        date.set(False)
        date_cb = tk.Checkbutton(floating_window, text="Add date to the name of the file              ",
                                 variable=date, font=(letter_font, 14))
        date_cb.pack()

        spacing2 = ttk.Label(floating_window, text='', padding=(0, 0, 0, -6))
        spacing2.pack()

        shortcut = tk.BooleanVar()
        shortcut.set(False)
        shortcut_cb = tk.Checkbutton(floating_window, text="Create a desktop shortcut for this world ",
                                     variable=shortcut, font=(letter_font, 14))
        shortcut_cb.pack()

        date_cb.bind('<Enter>', lambda e: floating_window.after(1100, display_information_text, e))
        shortcut_cb.bind('<Enter>', lambda e: floating_window.after(800, display_information_text, e))
        date_cb.bind('<Leave>', display_information_text)
        shortcut_cb.bind('<Leave>', display_information_text)

        floating_window.update()
        upper_canva = tk.Canvas(floating_window, bd=0, highlightthickness=0, width=date_cb.winfo_width()+5, height=70)

        info_label = tk.Message(floating_window, text='', background="white", font=(letter_font, 11), width=350)

        upper_canva.create_polygon([0, 5, 10, 5, 15, 0, 20, 5, date_cb.winfo_width()+4,
                                    5, date_cb.winfo_width()+4, 69, 0, 69],
                                   fill='white', outline='gray')

        floating_window.bind('<Destroy>', lambda e: save_variables())

    def browse_world_path(self):
        # Opens a navigation tab on the .minecraft\saves path for selecting the world to save
        path = filedialog.askdirectory(initialdir=os.path.join(os.getenv('APPDATA'), r'.minecraft\saves'))
        world_name = os.path.basename(path)
        self.path_entry.configure(state='normal')
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, world_name)
        self.path_entry.configure(state='readonly')
        self.save_world_name(world_name)

    def browse_target_path(self):
        # Opens a navigation tab for selecting the destiny to save the world
        path = filedialog.askdirectory()
        self.path_entry2.configure(state='normal')
        self.path_entry2.delete(0, tk.END)
        self.path_entry2.insert(0, path)
        self.path_entry2.configure(state='readonly')
        self.save_target_path(path)

    def save_world_name(self, world_name):
        # Saves the world name in a file on temp dir, for recover it when app has been closed
        with open(os.path.join(os.environ['TEMP'], 'last_directory.txt'), 'w') as file:
            file.write(f'{world_name}\n')

    def save_target_path(self, path):
        # Saves the destiny path in a file on temp dir, for recover it when app has been closed
        with open(os.path.join(os.environ['TEMP'], 'last_directory.txt'), 'a') as file:
            file.write(path)

    def load_saved_paths(self):
        # Opens the file with the last world and destiny path selected, and sets it to be displayed on the entries
        last_directory = os.path.join(os.environ["TEMP"], 'last_directory.txt')
        if os.path.exists(last_directory):
            with open(last_directory, 'r') as file:
                data = file.read()
                paths = data.splitlines()
                self.path_entry.configure(state='normal')
                self.path_entry.delete(0, tk.END)
                try:
                    self.path_entry.insert(0, paths[0])
                except IndexError:
                    pass
                self.path_entry.configure(state='readonly')

                self.path_entry2.configure(state='normal')
                self.path_entry2.delete(0, tk.END)
                try:
                    self.path_entry2.insert(0, paths[1])
                except IndexError:
                    pass
                self.path_entry2.configure(state='readonly')

    def load_sw_file(self, sw):
        # Opens and reads the sw file specified depending on the quick acces that has been opened
        swfile = os.path.join(os.environ["TEMP"], 'savecraft', sw)
        with open(swfile, 'r') as file:
            data = file.read()
        info = data.splitlines()
        world, target, file_type, date = info
        return world, target, file_type, date


    def create_shortcut_icon(self, world_name, i):
        # Creates the shortcut icon based on the orignal world icon
        img1 = Image.open(os.path.join(application_path, 'icon2.png'))
        img2 = Image.open(os.path.join(os.getenv('APPDATA'), fr'.minecraft\saves\{world_name}\icon.png'))

        result = Image.alpha_composite(img2.convert('RGBA'), img1)
        result.save(os.path.join(os.environ['TEMP'], 'savecraft', f'icon{i}.ico'))

    def create_shortcut(self, i, world_name):
        # Creates a quick acces with an argument starting from 0
        path_to_exe = sys.argv[0]
        argument = f"--sw{i}"

        self.create_shortcut_icon(world_name, i)

        shortcut_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', f'{world_name} SaveCraft')
        shortcut_destiny = f'{path_to_exe} {argument}'

        ps.make_shortcut(name=shortcut_path, script=shortcut_destiny,
                         icon=os.path.join(os.environ['TEMP'], 'savecraft', f'icon{i}.ico'))

    def save_as_dir(self, world_name, target, date):
        # copies files to the destiny if the modification time is different
        minecraft = os.path.join(os.environ['appdata'], fr'.minecraft\saves\{world_name}')

        if date is None:
            # check if the worlds exists in the target
            if os.path.exists(os.path.join(target, world_name)):
                hello = True
                bye = False
                list_with_dirs = [""]
                while hello:
                    try:
                        actual_dir = list_with_dirs[0]
                        list_with_dirs.remove(list_with_dirs[0])

                        for directory in os.listdir(os.path.join(minecraft, actual_dir)):
                            # Check if directory is a file

                            if os.path.isfile(os.path.join(minecraft, actual_dir, directory)):
                                # If the directory is a file, check if file exists on target

                                if os.path.exists(os.path.join(target, world_name, actual_dir, directory)):
                                    # If exists, check if the modification date of source and the target is the same

                                    if (os.path.getmtime(os.path.join(minecraft, actual_dir, directory)) is not
                                            os.path.getmtime(os.path.join(target, world_name, actual_dir, directory))):
                                        # If it's not the same copy the source file to the target

                                        shutil.copyfile(os.path.join(minecraft, actual_dir, directory),
                                                        os.path.join(target, world_name, actual_dir, directory))

                                else:
                                    # If it doesn't exist, copy the source file to the target
                                    shutil.copyfile(os.path.join(minecraft, actual_dir, directory),
                                                    os.path.join(target, world_name, actual_dir, directory))

                            else:
                                list_with_dirs.append(os.path.join(actual_dir, directory))

                                if os.path.exists(os.path.join(target, world_name, actual_dir, directory)):
                                    pass
                                else:
                                    os.mkdir(os.path.join(target, world_name, actual_dir, directory))

                    except IndexError:
                        hello = bye
            else:
                shutil.copytree(os.path.join(minecraft), os.path.join(target, world_name))

        elif date is not None:
            shutil.copytree(os.path.join(minecraft), os.path.join(target, world_name + date))

    def save_as_zip(self, world_name, target, date):
        minecraft = os.path.join(os.environ['appdata'], fr'.minecraft\saves\{world_name}')
        if date is None:
            shutil.make_archive(os.path.join(target, world_name), 'zip', os.path.join(minecraft))
        elif date is not None:
            shutil.make_archive(os.path.join(target, world_name + date), 'zip', os.path.join(minecraft))

    def copy_world_process(self, world_name, target, file_type, date):
        if file_type == 'folder':
            if date is False:
                self.save_as_dir(world_name, target, None)
            elif date is True:
                today_date = datetime.date.today().strftime(' %d-%m-%Y')
                self.save_as_dir(world_name, target, today_date)

        elif file_type == 'zfolder':
            if date is False:
                self.save_as_zip(world_name, target, None)
            elif date is True:
                today_date = datetime.date.today().strftime(' %d-%m-%Y')
                self.save_as_zip(world_name, target, today_date)

    def copy_world_start(self, world_name, target):
        # starts the process of copying the world to the destiny, calling necesary methods
        self.accept_button["state"] = 'disabled'
        self.progress_bar['maximum'] = 19
        self.progress_bar["value"] = 0
        self.progress_bar.update()

        if world_name != '' and target != '':
            if self.shortcut:
                tempdir = os.path.join(os.environ["TEMP"], 'savecraft')
                if os.path.exists(tempdir):
                    pass
                else:
                    os.mkdir(tempdir)

                worlds = [item for item in os.listdir(tempdir) if item.endswith('.txt')]

                for i, world in enumerate(worlds):
                    if world == f"sw{i}.txt":
                        pass
                    else:
                        break

                try:
                    i += 1
                except NameError:
                    i = 0

                with open(os.path.join(tempdir, f'sw{i}.txt'), 'w') as sf:
                    sf.write(f'{world_name}\n{target}\n{self.file_type}\n{self.date}')
                self.create_shortcut(i, world_name)

            self.copy_world_process(world_name, target, self.file_type, self.date)

        self.accept_button["state"] = 'active'

    def startup(self):
        # Loads saved world name and destiny path or start saving if has been opened from a shortcut
        if len(sys.argv) > 1:
            tempdir = os.path.join(os.environ["TEMP"], 'savecraft')
            for world in os.listdir(tempdir):
                for arg in sys.argv[1:]:
                    if f'--{world}' == f'{arg}.txt':
                        world_name, target, file_type, date = self.load_sw_file(world)

                        self.copy_world_process(world_name, target, file_type, bool(date))
                        break
        else:
            windll.shcore.SetProcessDpiAwareness(1)
            app.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SaveCraft")

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)

    root.iconbitmap(default=os.path.join(application_path, 'icon.ico'))

    your_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    font = your_font.actual()

    app = MainWindow(root)
    app.startup()
