import os
import PySimpleGUI as sg

def rename_files(directory_path, new_base_name, episode_format, window):
    if not os.path.exists(directory_path):
        sg.popup_error(f"Directory '{directory_path}' does not exist.")
        return

    files = os.listdir(directory_path)

    for i, filename in enumerate(files, start=1):
        episode_number = str(i).zfill(2)  # Pad the episode number with leading zeros if needed
        new_filename = f"{new_base_name}_{episode_format}{episode_number}"
        file_extension = os.path.splitext(filename)[-1]
        new_filename_with_extension = f"{new_filename}{file_extension}"
        
        old_filepath = os.path.join(directory_path, filename)
        new_filepath = os.path.join(directory_path, new_filename_with_extension)

        os.rename(old_filepath, new_filepath)
        
        # Update progress bar
        window['progress_bar'].update_bar(i, len(files))

    sg.popup(f"Renamed {len(files)} files in '{directory_path}'.")

sg.theme('DarkGrey5')  # Set a theme for the GUI
layout = [
    [sg.Text('Select a directory:')],
    [sg.InputText(key='directory_path'), sg.FolderBrowse()],
    [sg.Text('New Base Name:'), sg.InputText(key='new_base_name')],
    [sg.Text('Season/Episode Format:'), sg.InputText(key='episode_format', default_text='S01E', disabled=False)],
    [sg.Button('Rename Files')],
    [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress_bar', visible=False)],
]

window = sg.Window('File Renamer', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Rename Files':
        directory_path = values['directory_path']
        new_base_name = values['new_base_name']
        episode_format = values['episode_format']

        if not directory_path or not new_base_name:
            sg.popup_error("Please fill in all fields.")
            continue

        window['progress_bar'].update_bar(0, 100)
        window['progress_bar'].update(visible=True)

        rename_files(directory_path, new_base_name, episode_format, window)
        window['progress_bar'].update(visible=False)

window.close()
