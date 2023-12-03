def create_prompt(user, main_question):
    system_prompt = f"Ти соціальний працівник з країни під назвою {user.country}, асистент людини, яка емігрувала з України і повинен допомогти їй з питаннями у різних сферах життя для адаптації та нормального життя в ції країні."
    add_info  = additional_info(user)
    client_prompt = f"{add_info} {main_question} Надай актуальну та стислу інформацію по цьому питанню, намагайся знаходити інформацію з офіційних джерел. Відповідь на нього дуже важлива для мене, оскільки я знаходжусь і іншій країні."
    return (system_prompt, client_prompt)

def additional_info(user):
    additional_info= ""
    if user.gender is not None:
        if user.age is not None:
            if user.age < 30:
                additional_info+= "Я хлопець з України." if user.gender == "M" else  "Я дівчина з України."
            else:
                additional_info += "Я чловік з України." if user.gender == "M" else "Я жінка з України."
        else:
            additional_info+="Я чловік з України." if user.gender == "M" else "Я жінка з України."
    if user.age is not None:
        additional_info += f" Мені {str(user.age)} років."
    if user.children:
        additional_info += f" Маю неповнолітніх дітей."
    if user.profession is not None:
        additional_info += f" Маю досвід в таких видах робіт як {user.profession} ."
    return additional_info
