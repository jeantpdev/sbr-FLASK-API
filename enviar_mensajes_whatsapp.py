import pyautogui, webbrowser
from time import sleep

#Numero al que se le quiere enviar mensajes
webbrowser.open("https://web.whatsapp.com/send?phone=+573003764436")

#Se coloca un temporizador para que cargue la pagina completa y pueda continuar
sleep(10)

for i in range(25):
    #Mensaje a enviar según la cantidad a repetir en el FOR
    pyautogui.typewrite('cuenta')
    #Luego de escribir el mensaje, presiona la tecla ENTER del teclado
    pyautogui.press('enter')