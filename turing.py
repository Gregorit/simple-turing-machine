# Internal Modules
import argparse


def arguments():
    """Argunent pass handling."""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_in",
                        metavar="plik",
                        help="nazwa pliku wejsciowego")
    args = parser.parse_args()

    return args


def parser(filename):
    """Dataset file parser.
    
    It works when file is in correct format.
    """
    with open(filename, 'r') as f:
        print(f"[  OK  ] Plik {filename} załadowany!\n")

        alphabet_tape = ""
        alphabet_in = ""
        word_in = ""
        states = []
        state_start = ""
        states_accept = []
        table_relation = {}

        f.readline()
        alphabet_tape = f.readline().rstrip()

        f.readline()
        alphabet_in = f.readline().rstrip()

        f.readline()
        word_in = f.readline().rstrip()

        f.readline()
        states = f.readline().rstrip().split(' ')

        f.readline()
        state_start = f.readline().rstrip()

        f.readline()
        states_accept = f.readline().rstrip().split(' ')

        f.readline()
        while relation := f.readline():
            rel = relation.rstrip().split(' ')
            table_relation[(rel[0],rel[1])] = [rel[2],rel[3],rel[4]]  

        print(f"[  OK  ] Plik {filename} wczytany!\n")

        return alphabet_tape, alphabet_in, word_in, states, state_start, states_accept, table_relation


def word_to_tape(word_in):
    """Tape preparation.
    Extension to 32 cells. Non-used ones are filled with blanks."""
    tape = list(word_in)
    for _ in range(len(tape),32):
        tape.append('#')
    
    return tape


def hash_remover(tape):
    reverse_counter = 2

    while reverse_counter != 0:
        if tape[0] == "#":
            tape.pop(0)
        else:
            reverse_counter -= 1
            tape.reverse()

    return tape


def turing_machine(tape, state_start, states_accept, table_relation, word_in):
    """Definition solves Turing machine problem."""
    index = 0
    iteration = 0
    state = state_start
    showLog = True

    # Variable for comparison purposes only
    tape_init = ''.join(tape)

    print(f"Taśma startowa:\n"
          f"       {tape_init}\n\n")
    
    while state not in states_accept:
        try:
            iteration += 1
            if iteration == 1000:
                print("[ INFO ] Zbyt duzo interacji. Nie pokazuje wiecej")
                input("Aby kontynuować - Wciśnij Enter")
                showLog = False
            
            start_letter = tape[index]
            start_state = state
            relation = table_relation[(state, start_letter)]
            state = relation[0]
            tape[index] = relation[1]

            if showLog: 
                print("*******************************************\n"
                     f"** Iteracja: {iteration}  \n"
                      "*******************************************\n"
                      "** Stany:\n"
                     f"**       > Stan Startowy: {start_state}\n"
                     f"**       > Stan Końcowy:  {state} \n"
                      "** Litera:\n"
                     f"**       > Startowa: {start_letter}\n"
                     f"**       > Wstawiona: {relation[1]}\n"
                      "** Kierunek:")
                if relation[2] == "L":
                    print(f"**       {relation[2]} (index: {index} -> {index-1})")
                else:
                    print(f"**       {relation[2]} (index: {index} -> {index+1})")
                print("*******************************************\n"
                      "** Taśma po zmianach:\n"
                     f"**       {''.join(tape)}\n"
                     "*******************************************\n")

            if relation[2] == 'L':
                if index == 0:
                    # Add 32 empty cells to the left side add move index to left (cell 31)
                    for _ in range(0,32):
                        tape.insert(0,'#')
                    index = 31
                    if showLog:
                        print("** UWAGA: Taśma zostanie poszerzona w lewo!\n"
                              "*******************************************")
                else:
                    index -= 1
            else:
                if index == len(tape)-1:
                    # Add 32 empty cells to the right side and move index to right (cell+1)
                    for _ in range(0,32):
                        tape.append('#')
                    index += 1
                    if showLog:
                        print("** UWAGA: Taśma zostanie poszerzona prawo!\n"
                              "*******************************************")
                else:
                    index += 1
        except KeyError:
            print ("[ ERROR ] Błąd kodu:\n"
                  f"          Nie ma stanu obslugującego sytuację: STAN {state} LITERA {tape[index]}\n"
                  f"          [{state} {tape[index]} ? ? ?]")
            break
        except KeyboardInterrupt:
            print (f"[  OK  ] Zakonczenie na zamowienie")
            break

    print("\n\n[  OK  ] Program zakończył działanie.\n"
         f"         Stan: {state}\n"
         f"         Iteracja: {iteration}\n"
         f"         Pozycja głowicy: {index}")

    print("\n\n----- [ Porównanie taśm ] -----\n"
          "Taśma startowa:\n"
         f"       {tape_init}\n\n"
          "Końcowy stan taśmy:\n"
         f"       {''.join(tape)}")
    
    word = hash_remover(tape)
    print("\n\n----- [ Porównanie słów ] -----\n"
          "Słowo startowe:\n"
         f"       {word_in}\n\n"
          "Słowo końcowe:\n"
         f"       {''.join(word)}")


# File loading from argument and global variables generation
ALPHABET_TAPE, ALPHABET_IN, WORD_IN, STATES, STATE_START, STATES_ACCEPT, TABLE_RELATION = parser(arguments().file_in)

# Tape resizing to standard 32 cells
TAPE = word_to_tape(WORD_IN)

# Working with provided data from selected dataset
turing_machine(TAPE, STATE_START, STATES_ACCEPT, TABLE_RELATION, WORD_IN)
