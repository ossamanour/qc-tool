import inquirer


def inquirer_list(
        name: str = None, 
        message: str = None, 
        choices: list = None):
    questions = [
        inquirer.List(
            name=name, 
            message=message, 
            choices=choices,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers[name]


def inquirer_text(
        name: str = None, 
        message: str = None):
    questions = [
        inquirer.Text(
            name=name, 
            message=message,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers[name]