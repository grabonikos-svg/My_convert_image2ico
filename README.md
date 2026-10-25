# My_convert_image2ico

Εφαρμογή για Windows που μετατρέπει μια εικόνα σε εικονίδιο `.ico` 256×256. Δέχεται PNG, JPG, WEBP και BMP. Το αποτέλεσμα αποθηκεύεται στον φάκελο `icon_output`, δίπλα στην αρχική εικόνα.

## Εκτέλεση από τον κώδικα

```bat
python -m venv .venv
.venv\Scripts\python.exe -m pip install customtkinter pillow
.venv\Scripts\python.exe main.py
```

## Εγκατάσταση του έτοιμου προγράμματος

Αν υπάρχει το `dist\main.exe`, το `install.bat` το αντιγράφει στο `%LOCALAPPDATA%\My_convert_image2ico` και δημιουργεί συντόμευση στην επιφάνεια εργασίας και στο μενού Έναρξη.

Το εικονικό περιβάλλον και τα αρχεία build δεν περιλαμβάνονται σε αυτό το repository.
