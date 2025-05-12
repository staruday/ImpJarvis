import pygame


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()  # ✅ Close mixer completely so file can be deleted
