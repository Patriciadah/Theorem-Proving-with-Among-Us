import prover as p
from prover import player_sentences

def kill_sentence_decoder(rawString,sentence):
    """
    Decodes a sentence about a kill and generates a logical statement for the FOL.
    Example: "Blue killed Brown" -> kill(Blue, Brown).
    """
    parts = rawString.split()
    if len(parts) >= 3 and "killed" in parts:
        killer = parts[0]  # First word
        victim = parts[2]  # Third word
        player_sentences[sentence]=f"killObj({killer}, {victim})"
        print(f"Decoded kill statement: killObj({killer}, {victim})")

def is_dead_decoder(rawString,sentence):
    """
    Decodes a sentence about a dead player and generates a logical statement.
    Example: "I can't believe Brown is dead!" -> victim(Brown).
    """
    parts = rawString.split()
    if "is" in parts and "dead!" in parts:
        victim_index = parts.index("is") - 1  # Word before 'is'
        victim = parts[victim_index]
        player_sentences[sentence]=f"victimObj({victim})"
        print(f"Decoded dead statement: victimObj({victim})")

def i_do_task_decoder(rawString, sentence):
    """
    Decodes a player's own task statement.
    Example: "I was doing Scan at Medbay" -> doTask(Player, task(Scan, Medbay)).
    """
    parts = rawString.split()
    if "doing" in parts and "at" in parts:
        player = sentence  # Player who said the statement
        task_index = parts.index("doing") + 1
        place_index = parts.index("at") + 1
        task = parts[task_index]
        place = parts[place_index]
        player_sentences[sentence]=f"doTaskObj({player}, task({task}, {place}))"
        print(f"Decoded self-task statement: doTaskObj({player}, task({task}, {place}))")

def he_does_task_decoder(rawString,sentence):
    """
    Decodes a statement about another player's task.
    Example: "I saw Red doing FixMeltdown at Reactor" -> doTask(Red, task(FixMeltdown, Reactor)).
    """
    parts = rawString.split()
    if "saw" in parts and "doing" in parts and "at" in parts:
        observer = parts[0]  # The player making the statement
        observed_player_index = parts.index("saw") + 1
        observed_player = parts[observed_player_index]
        task_index = parts.index("doing") + 1
        place_index = parts.index("at") + 1
        task = parts[task_index]
        place = parts[place_index]
        player_sentences[sentence]=f"saw({observer}, doTaskObj({observed_player}, task({task}, {place}))))."
        print(f"Decoded observed-task statement: saw({observer}, doTaskObj({observed_player}, task({task}, {place}))).")

def recieve_sentences_as_strings(sentences):
    """
    Processes all sentences and routes them to the appropriate decoder function.
    """
    for sentence in sentences:
        rawString = sentences[sentence]

        if "killed" in rawString:
            kill_sentence_decoder(rawString,sentence)
        elif "dead" in rawString:
            is_dead_decoder(rawString,sentence)
        elif "I" in rawString:
            i_do_task_decoder(rawString, sentence)
        elif "doing" in rawString:
            he_does_task_decoder(rawString,sentence)
