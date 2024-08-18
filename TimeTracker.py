from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_records(file_path):
    if not os.path.isfile(file_path):
        df = pd.DataFrame({
            'Task Name': [],
            'Task Type': [],
            'Start Time': [],
            'End Time': [],
            'Duration': [],
            'Date': []
        })
        df.to_csv(file_path, index=False)


def add_records(file_path, task_name, task_type, start_time, end_time, duration, date):
    data = {
        'Task Name': [task_name],
        'Task Type': [task_type],
        'Start Time': [start_time],
        'End Time': [end_time],
        'Duration': [duration],
        'Date': [date]
    }
    df = pd.DataFrame(data)

    df.to_csv(file_path, mode='a', header=False, index=False)


create_records('timedata.csv')

start_time = None
end_time = None
time_duration = None
timer_running = True
is_cancel = False


def start_test():
    global start_time, timer_running, is_cancel
    timer_running = True
    is_cancel = False
    start_time = datetime.now()
    formatted_start_time = start_time.strftime('%H:%M:%S')
    start_button.config(state='disabled')
    done_button.config(state='normal')
    cancel_button.config(state='normal')
    user_typing.config(state='disabled')
    work_menu.config(state='disabled')
    instruction_button.config(state='disabled')
    user_typing.config(state='disabled')

    start_time_label.config(text=f"Start Time: {formatted_start_time}", fg='gold')
    end_time_label.config(text="End Time: ...")
    user_typing.focus()

    timer_function()


def timer_end():
    global timer_running
    timer_running = False


def cancel_timer():
    global is_cancel
    is_cancel = True


def timer_function():
    global start_time, timer_running

    if not is_cancel:
        if timer_running:
            elapsed_time = datetime.now() - start_time
            formatted_time = str(elapsed_time).split('.')[0]  # Removes microseconds part

            time_duration_label.config(text=f"Duration: {formatted_time}",
                                       fg='SpringGreen2')

            info_frame.after(1000, timer_function)
        else:
            results()
    else:
        results()


def results():
    global end_time, start_time
    start_button.config(state='normal')
    done_button.config(state='disabled')
    cancel_button.config(state='disabled')
    instruction_button.config(state='normal')
    user_typing.config(state='normal')
    work_menu.config(state='normal')
    graph_summary_button.config(state='normal')

    end_time = datetime.now()
    formatted_end_time = end_time.strftime('%H:%M:%S')
    end_time_label.config(text=f"End Time: {formatted_end_time}", fg='gold')

    duration = end_time - start_time
    formatted_duration = str(duration)
    end_time_label.config(text=f"End Time: {formatted_end_time}")

    if not is_cancel:
        add_records('timedata.csv',
                    task_name=user_typing.get('1.0', END).strip() or "Not Provided",
                    task_type=work_var.get(),
                    start_time=start_time.strftime('%H:%M:%S'),
                    end_time=formatted_end_time,
                    duration=formatted_duration.split('.')[0],
                    date=end_time.strftime('%d/%m/%Y'))



def create_summary_graph():
    df = pd.read_csv('timedata.csv')
    df['Duration'] = pd.to_timedelta(df['Duration'])
    summary_df = df.groupby(['Task Type', 'Date'])['Duration'].sum().reset_index()

    # Convert duration to hours
    summary_df['Duration_Hours'] = summary_df['Duration'].dt.total_seconds() / 3600

    # Convert date to datetime format and then to dd/mm/yyyy format
    summary_df['Date'] = pd.to_datetime(summary_df['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')

    # Set a color palette for better visual distinction
    palette = sns.color_palette("Set2")

    # Plotting the graph with all task types
    plt.figure(figsize=(16, 10))
    sns.barplot(x='Date', y='Duration_Hours', hue='Task Type', data=summary_df, palette=palette)

    # Improve labels and formatting
    plt.title('Total Time Spent on Each Task Type by Date', fontsize=18, weight='bold')
    plt.xlabel('Date (dd/mm/yyyy)', fontsize=14)
    plt.ylabel('Total Time Spent (Hours)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Task Type', fontsize=12, title_fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Save the improved plot as an image file
    plt.savefig('generated_graph')

    # Show the final improved plot
    plt.show()



def instructions():
    messagebox.showinfo(
        title='Time Tracker Instructions',
        message=(
            'Welcome to the Time Tracker App!\n\n Time Format is 24 Hours Hours:Minutes:Seconds\n\n'
            'This app records the start and end times of tasks, calculates the total duration, '
            'and logs the data with the current date.\n\n'
            'Instructions:\n'
            '- Enter the Task name and Task type manually.\n'
            '- Press "Start" to begin tracking time.\n'
            '- Press "Done" to stop the timer and save the log.\n'
            '- Press "Cancel" to reset the timer and start again.\n\n'
            'After stopping the timer, you can generate a graph to view a summary of the recorded tasks and durations.'
        )
    )



window = Tk()
window.config(height=800, width=1000, padx=20, pady=20, bg='black')
window.title('Time Tracker App')

label_fonts = ("Verdana", 14)

# Frame For Typing
typing_frame = Frame(window, bg='black')
typing_frame.grid(row=0, column=0, padx=10, pady=10)

# Frame For info
info_frame = Frame(window, bg='black')
info_frame.grid(row=0, column=1, padx=20, pady=10, sticky='n')
###############################################


write_below = Label(typing_frame,
                    text='Write Exact Work Below (Optional)',
                    bg='black',
                    fg='lightcyan',
                    font=("Georgia", 14)
                    )
write_below.grid(row=0, column=0, pady=(10, 5))

user_typing = Text(typing_frame,
                   font=label_fonts,
                   width=25,
                   height=2
                   )
user_typing.grid(row=1, column=0, pady=(10, 5))

instruction_button = Button(typing_frame,
                            text='Instructions',
                            bg='black',
                            fg='mediumpurple',
                            font=label_fonts,
                            activeforeground='black',
                            activebackground='deeppink2',
                            width=10,
                            command=instructions
                            )
instruction_button.grid(row=3, column=0, pady=(40, 20))

graph_summary_button = Button(typing_frame,
                              text='Show Graph Summary',
                              bg='black',
                              fg='mediumpurple',
                              font=label_fonts,
                              activeforeground='black',
                              activebackground='deeppink2',
                              width=25,
                              command=create_summary_graph,
                              state='disabled'
                              )
graph_summary_button.grid(row=4, column=0, pady=(20, 20))

############################ INFO FRAME

about_label = Label(info_frame,
                    text='Welcome To Time Tracker',
                    bg='black',
                    fg='lightcyan',
                    font=("Georgia", 14)
                    )
about_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

start_time_label = Label(info_frame,
                         text='Start time: 00:00:00',
                         bg='black',
                         fg='salmon',
                         font=label_fonts
                         )
start_time_label.grid(row=1, column=0, pady=(10, 5))

end_time_label = Label(info_frame,
                       text='End Time : 00:00:00',
                       bg='black',
                       fg='salmon',
                       font=label_fonts
                       )
end_time_label.grid(row=2, column=0, pady=(10, 5))

time_duration_label = Label(info_frame,
                            text='Duration: 00:00:00',
                            bg='black',
                            fg='salmon',
                            font=label_fonts
                            )
time_duration_label.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))

work_option_label = Label(info_frame,
                          text="Select Work",
                          font=("Segoeui", 14),
                          bg='black',
                          fg='deepskyblue')
work_option_label.grid(row=4, column=0, pady=(20, 10), padx=(10, 10), sticky='nw')

work_var = StringVar(info_frame, value="Study")  # Get Answer by "difficulty_var.get()".
timer_options = ["Study", "Work", "Entertaintment", "Other"]
work_menu = OptionMenu(info_frame, work_var, *timer_options)
work_menu.grid(row=4, column=0, pady=(20, 10), padx=(10, 10), sticky='ne')

start_button = Button(info_frame,
                      text='Start',
                      bg='black',
                      fg='olivedrab1',
                      font=label_fonts,
                      activeforeground='black',
                      activebackground='lightblue',
                      width=10,
                      command=start_test
                      )
start_button.grid(row=5, column=0, pady=(10, 10), sticky='nw')

done_button = Button(info_frame,
                     text='Done',
                     bg='black',
                     fg='olivedrab1',
                     font=label_fonts,
                     activeforeground='black',
                     activebackground='lightblue',
                     width=10,
                     command=timer_end,
                     state='disabled'
                     )
done_button.grid(row=5, column=0, pady=(10, 10), sticky='ne')

cancel_button = Button(info_frame,
                       text='Cancel',
                       bg='black',
                       fg='olivedrab1',
                       font=label_fonts,
                       activeforeground='black',
                       activebackground='lightblue',
                       width=10,
                       command=cancel_timer,
                       state='disabled'
                       )
cancel_button.grid(row=6, column=0)

window.mainloop()

# typing_label = Label(typing_frame,
#                      height=20,
#                      width=30,
#                      font=label_fonts,
#                      wraplength=350)

# typing_label.grid(row=0, column=0)
# user_typing.bind("<KeyRelease>", compare_text)
# user_typing.bind("<KeyRelease>", real_time_results)
#
# user_typing.tag_configure("correct", foreground="green")
# user_typing.tag_configure("incorrect", foreground="red")


#
# difficulty_var = StringVar(info_frame, value="Easy")  # Get Answer by "difficulty_var.get()".
# difficulty_options = ["Easy", "Medium", "Hard"]
# difficulty_menu = OptionMenu(info_frame, difficulty_var, *difficulty_options)
# difficulty_menu.grid(row=7, column=0, pady=(20, 10), padx=(10, 10), sticky='ne')

# accuracy_label = Label(info_frame,
#                        text='Accuracy: 0%',
#                        bg='black',
#                        fg='salmon',
#                        font=label_fonts
#                        )
# accuracy_label.grid(row=4, column=0, pady=(10, 5))
#
#
#
#
#
#
# high_speed_label = Label(info_frame,
#                          text=" dddd ",
#                          bg='black',
#                          fg='salmon',
#                          font=label_fonts,
#                          wraplength=200
#                          )
# high_speed_label.grid(row=5, column=0, pady=(10, 5))

# def real_time_results(event):
#     global chosen_sentence, start_time
#
#     elapsed_time = time.time() - start_time
#     typed_text = user_typing.get('1.0', END).strip()
#     num_words = len(typed_text.split())
#     num_chars = len(typed_text)
#
#     # Calculate WPM and CPM
#     # wpm = (num_words / elapsed_time) * 60
#     cpm = (num_chars / elapsed_time) * 60
#
#     # Calculate accuracy
#     correct_chars = sum(1 for a, b in zip(typed_text, chosen_sentence) if a == b)
#     accuracy = (correct_chars / len(chosen_sentence)) * 100 if chosen_sentence else 0
#
#     # wpm_label.config(text=f"WPM: {wpm:.0f}")
#     cpm_label.config(text=f"CPM: {cpm:.0f}")
#     accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")

# def read_csv_as_int(file_path):
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(file_path)
#
#     # Convert the columns to integer type
#     df = df.astype(int)
#
#     return df

# def compare_text(event):
#     typed_text = user_typing.get('1.0', END).strip()
#     correct_text = chosen_sentence
#     if not correct_text:
#         return
#
#     user_typing.tag_remove("correct", "1.0", "end")
#     user_typing.tag_remove("incorrect", "1.0", "end")
#
#     for i, char in enumerate(typed_text):
#         if i < len(correct_text):
#             if char == correct_text[i]:
#                 user_typing.tag_add("correct", f"1.{i}", f"1.{i+1}")
#             else:
#                 user_typing.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
