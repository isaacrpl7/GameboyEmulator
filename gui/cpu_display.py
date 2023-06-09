import tkinter as tk

class DisplayCPU:

    def __init__(self):
        self.registers_labels = []
        
        self.window = tk.Tk()
        self.window.title("CPU Registers")
        self.window.configure(bg="#c5ccd6")

    def init_gui(self, registers: dict, step):
        label_a = tk.Label(master=self.window, text="Registers:", font='Helvetica 9 bold',background="#c5ccd6")
        label_a.grid(row=0, column=0, padx=5, pady=0, sticky='W')

        registers_frame = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
        )
        registers_frame.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        for i, register in enumerate(['A', 'B', 'C', 'D', 'E']):
            self.registers_labels.append(tk.Label(master=registers_frame, text=f"{register}\nValue: 0x{registers[register][2:].upper()}"))
            self.registers_labels[i].grid(row=0, column=i, padx=5, pady=5)

        for i, register in enumerate(['H', 'L']):
            self.registers_labels.append(tk.Label(master=registers_frame, text=f"{register}\nValue: 0x{registers[register][2:].upper()}"))
            self.registers_labels[5+i].grid(row=1, column=i, padx=5, pady=5)
        
        label_b = tk.Label(master=self.window, text="Flags:", font='Helvetica 9 bold',background="#c5ccd6")
        label_b.grid(row=2, column=0, padx=5, pady=0, sticky='W')

        flags_frame = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
        )
        flags_frame.grid(row=3, column=0, padx=5, pady=5, sticky='W')
        for i, register in enumerate(['Z', 'S', 'H', 'C']):
            self.registers_labels.append(tk.Label(master=flags_frame, text=f"{register}\nValue: 0x{registers[register][2:].upper()}"))
            self.registers_labels[7+i].grid(row=0, column=i, padx=5, pady=5)
        
        PC_label = tk.Label(master=self.window, text="PC and SP:", font='Helvetica 9 bold',background="#c5ccd6")
        PC_label.grid(row=4, column=0, padx=5, pady=0, sticky='W')

        sp_pc_frame = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
        )
        sp_pc_frame.grid(row=5, column=0, padx=5, pady=5, sticky='W')
        self.pc_label = tk.Label(master=sp_pc_frame, text=f"PC\nValue: 0x{registers['PC'][2:].upper()}")
        self.pc_label.grid(row=0, column=0, padx=5, pady=5)

        self.sp_label = tk.Label(master=sp_pc_frame, text=f"SP\nValue: 0x{registers['SP'][2:].upper()}")
        self.sp_label.grid(row=0, column=1,padx=5, pady=5)

        btn_step = tk.Button(master=self.window,text="Step", command=step)
        btn_step.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

        self.window.mainloop()

    def update(self, registers:dict):
        for idx, register in enumerate(['A', 'B', 'C', 'D', 'E']):
            self.registers_labels[idx]['text'] = f"{register}\nValue: 0x{registers[register][2:].upper()}"

        for idx, register in enumerate(['H', 'L']):
            self.registers_labels[5+idx]['text'] = f"{register}\nValue: 0x{registers[register][2:].upper()}"

        for idx, register in enumerate(['Z', 'S', 'H', 'C']):
            self.registers_labels[7+idx]['text'] = f"{register}\nValue: 0x{registers[register][2:].upper()}"
            
        self.pc_label['text'] = f"PC\nValue: 0x{registers['PC'][2:].upper()}"
        self.sp_label['text'] = f"SP\nValue: 0x{registers['SP'][2:].upper()}"