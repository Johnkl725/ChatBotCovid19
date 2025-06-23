
# utils.py

def validate_age(age_str):
    """Valida que la edad sea un número entero dentro del rango 5-110."""
    try:
        age = int(age_str)
        if 5 <= age <= 110:
            return True, age
        else:
            return False, "La edad debe estar entre 5 y 110 años."
    except ValueError:
        return False, "Por favor, ingresa un número válido para la edad."

def get_multiple_choice_selection(options, prompt):
    """Permite al usuario seleccionar múltiples opciones de una lista."""
    selected_indices = []
    while True:
        print(prompt)
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        print("0. Terminar selección")

        choice = input("Ingresa el número de la opción (o 0 para terminar): ")
        try:
            choice = int(choice)
            if choice == 0:
                break
            elif 1 <= choice <= len(options):
                if choice - 1 not in selected_indices:
                    selected_indices.append(choice - 1)
                else:
                    print("Ya seleccionaste esta opción.")
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")
    
    return [options[i] for i in selected_indices]


