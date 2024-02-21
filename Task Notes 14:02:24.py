import sqlite3
import tkinter as tk
from tkinter import messagebox

#creating database
conn = sqlite3.connect("data.db") #establishing a connection 
cursor = conn.cursor() #creating cursor to interact with objects

#using execute to run sql statement to create a table named note if it doesn't exist
conn.execute( 'CREATE TABLE IF NOT EXISTS note(id INT, content text) ') 
#storing sql query here, for future use.
query = '''INSERT INTO note (id, content) VALUES(?,?)'''



#function to add tasks and display current tasks
def add():
    #fetching the max id to ensure the new task is added at the next index
    cursor.execute('''Select Max(id) From note''')
    index = cursor.fetchall()
    index = index[0][0]
    if index == None:
        index = 0
    #storing text to add 
    text_to_add = entry.get()
    #setting a flag to run if text to add is empty and then display a warning to the user if text is blank.
    flag = any(char.isalnum() for char in text_to_add)
    if flag == False:
        tk.messagebox.showwarning(title = "Warning", message = "Please enter task to add!")
    else:
        #inserting task into table 
        index +=1
        cursor.execute(query, (index, text_to_add))
        #running query to select all the task from table.
        cursor.execute('''SELECT content FROM note''')
        #storing query result
        result= cursor.fetchall()
        #commiting changes
        conn.commit()
        #creating tasks to store task 
        tasks = ""
        
        #inserting the tasks
        for count, task in enumerate(result):
            tasks += str(task[0]) + "\n"
            if index == 1:
                listbox.insert(0, task[0])
            else:
                if listbox.get(count) != str(task[0]):
                    listbox.insert(count, str(task[0]))
                else:
                    continue
        #displaying the tasks
        label4["text"] = tasks
           

#function to delete tasks and display current tasks
def delete():
        
        tasks = ""
        #deleting tasks based on selected task
        for i in listbox.curselection():
            delete_text = listbox.get(i)
            listbox.delete(i)
            cursor.execute('''DELETE FROM note where content = ?''', (delete_text,))
            conn.commit()

        #displaying leftover tasks
        for n in range ((listbox.size())):
            tasks += (listbox.get(n)) + "\n"
        #displaying the tasks left
        label4["text"] = tasks
    
window = tk.Tk()
window.title("Task Viewer")
#Adding label to display text
label = tk.Label(text = "Task Viewer")
label.pack()
#frame to contain buttons
frame = tk.Frame()
#button to add tasks
btn_add = tk.Button(frame, text = "Add Task", command = add)
#button to delete tasks
btn_del = tk.Button(frame, text = "Delete Task", command = delete)
#adding buttons and frame to the window
btn_add.pack(expand = True, fill = tk.BOTH)
btn_del.pack(expand = True, fill = tk.BOTH)
frame.pack(fill = tk.BOTH, expand = True)
#Creating label to display text
label2 = tk.Label(text = "Enter task below to add:")
label2.pack(side = tk.TOP)
#entry widget to enter tasks
entry = tk.Entry()
entry.pack(fill = tk.BOTH, expand = True)
#Creating label to display text
label3 = tk.Label(text = "List of tasks:")
label3.pack()
#label to display tasks
label4 = tk.Label()
label4.pack(fill = tk.BOTH, expand = True)
#Adding label to display text
label5 = tk.Label(text = "Select the task to delete below from the listbox:")
label5.pack()
#Adding listbox to display and select tasks
listbox = tk.Listbox()
listbox.pack(fill = tk.BOTH, expand = True)

window.mainloop()
#closing connection
conn.close()


