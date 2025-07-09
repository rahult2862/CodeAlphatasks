import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

root = tk.Tk()
root.title("Language Translator")
root.geometry("550x450")
root.resizable(False, False)
root.config(bg="#F0F0F0")

try:
    supported_langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    language_names = list(supported_langs_dict.keys())
except Exception as e:
    messagebox.showerror("Error", f"Could not fetch languages. Please check your internet connection.\nDetails: {e}")
    language_names = ["english", "spanish", "french"] 

def translate_text():
    """
    Translates text from the source language to the target language.
    """
    source_lang_name = source_lang_combo.get().lower()
    target_lang_name = target_lang_combo.get().lower()
    text_to_translate = source_text.get("1.0", tk.END).strip()

    if not text_to_translate:
        messagebox.showwarning("Warning", "Please enter text to translate.")
        return

    if not source_lang_name or not target_lang_name:
        messagebox.showwarning("Warning", "Please select both source and target languages.")
        return

    target_text.delete("1.0", tk.END)

    try:
        translator = GoogleTranslator(source='auto', target=supported_langs_dict[target_lang_name])
        translated_text = translator.translate(text_to_translate)
        
        target_text.insert("1.0", translated_text)
    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred during translation.\nDetails: {e}")

def copy_to_clipboard():
    """
    Copies the translated text to the clipboard.
    """
    translated_content = target_text.get("1.0", tk.END).strip()
    if translated_content:
        root.clipboard_clear()
        root.clipboard_append(translated_content)
        messagebox.showinfo("Copied", "Translated text has been copied to the clipboard!")
    else:
        messagebox.showwarning("Warning", "There is no text to copy.")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), background="#F0F0F0")
style.configure("TCombobox", font=("Helvetica", 11))

main_frame = tk.Frame(root, bg="#F0F0F0", padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

lang_frame = tk.Frame(main_frame, bg="#F0F0F0")
lang_frame.pack(fill="x", pady=(0, 15))

source_lang_combo = ttk.Combobox(lang_frame, values=language_names, state="readonly")
source_lang_combo.pack(side="left", expand=True, fill="x", padx=(0, 5))
source_lang_combo.set("english")

ttk.Label(lang_frame, text="to").pack(side="left", padx=10)

target_lang_combo = ttk.Combobox(lang_frame, values=language_names, state="readonly")
target_lang_combo.pack(side="left", expand=True, fill="x", padx=(5, 0))
target_lang_combo.set("spanish")

text_frame = tk.Frame(main_frame, bg="#F0F0F0")
text_frame.pack(expand=True, fill="both")

source_text = tk.Text(text_frame, font=("Helvetica", 11), height=8, wrap="word", relief="solid", borderwidth=1)
source_text.pack(expand=True, fill="both", pady=(0, 10))

target_text = tk.Text(text_frame, font=("Helvetica", 11), height=8, wrap="word", relief="solid", borderwidth=1)
target_text.pack(expand=True, fill="both")

button_frame = tk.Frame(main_frame, bg="#F0F0F0")
button_frame.pack(fill="x", pady=(15, 0))

translate_button = ttk.Button(button_frame, text="Translate", command=translate_text)
translate_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

copy_button = ttk.Button(button_frame, text="Copy Text", command=copy_to_clipboard)
copy_button.pack(side="left", expand=True, fill="x", padx=(5, 0))


root.mainloop()