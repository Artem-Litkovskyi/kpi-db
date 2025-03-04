from db_sim import TelNumberDB


def main():
    db = TelNumberDB()

    db.insert('Літковський', '+380-12-345-67-89')

    print('Table:\n', db.df)
    print('\n\nIndex:\n', db.surname_index)

    surname = 'Ковалишин'

    print(f'\n\nRows with surname \'{surname}\':\n')
    for row in db.search_by_surname(surname):
        print(row, '\n')

    print(f'\n\nRows before \'{surname}\':\n')
    for row in db.search_by_surname_less(surname):
        print(row, '\n')

    print(f'\n\nRows after \'{surname}\':\n')
    for row in db.search_by_surname_greater(surname):
        print(row, '\n')


if __name__ == '__main__':
    main()