import tkinter as tk
from Model import PatientModel
from View import PatientView
from Controller import PatientController

if __name__ == "__main__":
    root = tk.Tk()
    
    model = PatientModel()
    view = PatientView(root)
    controller = PatientController(model, view)
    
    root.mainloop()