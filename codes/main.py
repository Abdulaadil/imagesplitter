from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageSplitterMerger:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Splitter Merger")

        self.frame_width = 600
        self.frame_height = 500

        self.current_frame = None
        self.image_path = None
        self.split_images = None
        self.unique_ids = None

        self.show_upload_frame()

    def show_upload_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.master, width=self.frame_width, height=self.frame_height)
        self.current_frame.pack_propagate(False)
        self.current_frame.pack()

        upload_button = Button(self.current_frame, text="Upload Image", command=self.load_image)
        upload_button.grid(row=0, column=0, pady=20)

    def show_uploaded_image_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.master, width=self.frame_width, height=self.frame_height)
        self.current_frame.pack_propagate(False)
        self.current_frame.pack()

        input_image = Image.open(self.image_path)
        input_image.thumbnail((self.frame_width // 2, self.frame_height))
        photo = ImageTk.PhotoImage(input_image)

        label = Label(self.current_frame, image=photo)
        label.photo = photo
        label.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

        split_button = Button(self.current_frame, text="Split Image", command=self.split_image)
        split_button.grid(row=0, column=1, pady=10)

        reset_button = Button(self.current_frame, text="Reset", command=self.show_upload_frame)
        reset_button.grid(row=1, column=1, pady=10)

    def show_split_image_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.master, width=self.frame_width, height=self.frame_height)
        self.current_frame.pack_propagate(False)
        self.current_frame.pack()

        self.split_images = []
        self.unique_ids = []

        image = Image.open(self.image_path)
        width, height = image.size
        split_width = width // 2
        split_height = height // 2

        for i in range(4):
            split_img = image.crop((split_width * (i % 2), split_height * (i // 2), split_width * (i % 2 + 1), split_height * (i // 2 + 1)))
            split_img.thumbnail((self.frame_width // 2, self.frame_height // 2))
            photo = ImageTk.PhotoImage(split_img)

            label = Label(self.current_frame, image=photo)
            label.photo = photo
            label.id = f"split_image_{i}"
            label.grid(row=i // 2, column=i % 2, padx=10, pady=10)

            self.split_images.append(split_img)
            self.unique_ids.append(label.id)

        merge_button = Button(self.current_frame, text="Merge Image", command=self.merge_images)
        merge_button.grid(row=2, column=1, pady=10)

    def show_merge_image_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.master, width=self.frame_width, height=self.frame_height)
        self.current_frame.pack_propagate(False)
        self.current_frame.pack()

        merged_image = Image.new('RGB', (self.split_images[0].width * 2, self.split_images[0].height * 2))

        for i in range(2):
            for j in range(2):
                merged_image.paste(self.split_images[i * 2 + j], (j * self.split_images[0].width, i * self.split_images[0].height))

        merged_image.thumbnail((self.frame_width // 2, self.frame_height))
        photo = ImageTk.PhotoImage(merged_image)

        label = Label(self.current_frame, image=photo)
        label.photo = photo
        label.grid(row=0, column=0, padx=10, pady=10)

        reset_button = Button(self.current_frame, text="Reset", command=self.show_upload_frame)
        reset_button.grid(row=1, column=0, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.show_uploaded_image_frame()
        else:
            messagebox.showinfo("Error", "No image selected.")

    def split_image(self):
        self.show_split_image_frame()

    def merge_images(self):
        self.show_merge_image_frame()

if __name__ == "__main__":
    root = Tk()
    app = ImageSplitterMerger(root)
    root.mainloop()
