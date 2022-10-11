def save_images_names_to_txt(images_list, save_path):
    with open(save_path, 'w') as log_file:
        log_file.writelines([image + '\n' for image in images_list])
