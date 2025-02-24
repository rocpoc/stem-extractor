import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Test Tkinter UI")
    root.geometry("400x200")
    root.configure(bg="white")

    label = tk.Label(root, text="Hello, Tkinter!", bg="white", fg="black")
    label.pack(pady=10)

    entry = tk.Entry(root, width=50, bg="white", fg="black")
    entry.pack(pady=5)

    button = tk.Button(root, text="Click Me", bg="white", fg="black", command=lambda: print("Button clicked"))
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
