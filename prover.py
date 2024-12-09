import subprocess



base_content = """
assign(max_seconds, 100).
formulas(assumptions).

% At least one crewmate
crewmate(Blue) | crewmate(Yellow) | crewmate(Red) | crewmate(Green).

% At least one impostor
impostor(Blue) | impostor(Yellow) | impostor(Green) | impostor(Red).

% Exactly 3 crewmates and 1 impostor
all x (crewmate(x) <-> -impostor(x)).
all x (crewmate(x) | impostor(x)).
exists x (impostor(x) & all y (impostor(y) -> x = y)).

% Tasks and locations
place(Medbay).
place(Admin).
place(Cafeteria).
place(Reactor).
place(O2).

Admin!=Medbay.
Admin!=Cafeteria.
Admin!=Reactor.
Admin!=O2.
Cafeteria!=Medbay.
Cafeteria!=Reactor.
Cafeteria!=O2.
Reactor!=MedBay.
Reactor!=O2.
Medbay!=O2.


task_name(Scan).
task_name(SwipeCard).
task_name(InsertCode).
task_name(FixMeltdown).
task_name(FlushLeaves).


Scan!=SwipeCard.
Scan!=InsertCode.
Scan!=FixMeltdown.
Scan!=FlushLeaves.
SwipeCard!=InsertCode.
SwipeCard!=FixMeltdown.
SwipeCard!=FlushLeaves.
InsertCode!=FixMeltdown.
InsertCode!=FlushLeaves.
FixMeltdown!=FlushLeaves.

all x all y (is_valid (task(x, y)) -> task_name(x) & place(y)).

% Tasks are different
task(Scan, Medbay) != task(SwipeCard, Admin).
task(Scan, Medbay) != task(InsertCode, Admin).
task(Scan, Medbay) != task(InsertCode, O2).
task(Scan, Medbay) != task(FixMeltdown, Reactor).
task(Scan, Medbay) != task(FlushLeaves, Cafeteria).

task(SwipeCard, Admin) != task(Scan, Medbay).
task(SwipeCard, Admin) != task(InsertCode, Admin).
task(SwipeCard, Admin) != task(InsertCode, O2).
task(SwipeCard, Admin) != task(FixMeltdown, Reactor).
task(SwipeCard, Admin) != task(FlushLeaves, Cafeteria).

task(InsertCode, Admin) != task(Scan, Medbay).
task(InsertCode, Admin) != task(SwipeCard, Admin).
task(InsertCode, Admin) != task(InsertCode, O2).
task(InsertCode, Admin) != task(FixMeltdown, Reactor).
task(InsertCode, Admin) != task(FlushLeaves, Cafeteria).

task(InsertCode, O2) != task(Scan, Medbay).
task(InsertCode, O2) != task(SwipeCard, Admin).
task(InsertCode, O2) != task(InsertCode, Admin).
task(InsertCode, O2) != task(FixMeltdown, Reactor).
task(InsertCode, O2) != task(FlushLeaves, Cafeteria).

task(FixMeltdown, Reactor) != task(Scan, Medbay).
task(FixMeltdown, Reactor) != task(SwipeCard, Admin).
task(FixMeltdown, Reactor) != task(InsertCode, Admin).
task(FixMeltdown, Reactor) != task(InsertCode, O2).
task(FixMeltdown, Reactor) != task(FlushLeaves, Cafeteria).

task(FlushLeaves, Cafeteria) != task(Scan, Medbay).
task(FlushLeaves, Cafeteria) != task(SwipeCard, Admin).
task(FlushLeaves, Cafeteria) != task(InsertCode, Admin).
task(FlushLeaves, Cafeteria) != task(InsertCode, O2).
task(FlushLeaves, Cafeteria) != task(FixMeltdown, Reactor).

all y (is_valid (task(SwipeCard, y)) <-> y = Admin).
all y (is_valid (task(Scan, y)) <-> y = Medbay).
all y (is_valid(task(InsertCode, y)) <-> (y = O2 | y = Admin)).
all y (is_valid(task(FixMeltdown, y)) <-> y = Reactor).
all y (is_valid(task(FlushLeaves, y)) <-> y = Cafeteria).

all x all y all z (doTask(x, task(y, z)) -> (crewmate(x) & is_valid(task(y, z)))).

% Dead and kill constraints
all x (victim (x)) ->x=Brown | x=Purple | x=Pink.

% Only one victim
all x all y (victim(x) & victim(y) -> x = y).
all x all y (dead(x) & dead(y) -> x = y).
all x all y (kill(x, y) -> impostor(x) & victim(y)).
all x all y (victim(x) <-> dead(x)).

% Victim is killed by somebody
all x (victim(x) -> exists y kill(y, x)).

% Problem situations
DeadBody -> (exists x (dead(x))) & -doTask(x, task(y, Reactor)) & -doTask(x, task(y, O2)) & -doTask(x, task(InsertCode, Admin)).
ReactorActivated -> (all x (-victim(x))) & -doTask(x, task(y, O2)) & -doTask(x, task(InsertCode, Admin)).
OxygenDepletion -> (all x (-victim(x))) & -doTask(x, task(y, Reactor)).

% Lies and truths
all z all x all y all u (impostor(z) & saw(z, doTaskObj(x, task(y,u))) -> -doTask(x, task(y,u))).
all z all x all y all u (crewmate(z) & saw(z, doTaskObj(x, task(y,u))) -> doTask(x, task(y,u))).
all z all x all y  (impostor(z) & saw(z, killObj(x, y)) -> -kill(x, y)).
all z all x all y (crewmate(z) & saw(z, killObj(x, y)) -> kill(x, y)).
all z all x  (impostor(z) & saw(z, victimObj(x)) -> -victim(x)).
all z all x  (crewmate(z) & saw(z, victimObj(x)) -> victim(x)).

% Initial situation
-DeadBody.
ReactorActivated.
-OxygenDepletion.

"""

# Generate the .in file with additional player statements
def generate_amogus_in(player_statements):
    """
    Generates the dynamic .in file with player statements added.
    """
    with open("amogus_dynamic.in", "w") as file:
        # Write the base content
        file.write(base_content)

        # Add dynamic player statements
        for player, statement in player_statements.items():
            if statement:
                file.write(f"saw({player}, {statement}).\n")

        # End assumptions
        file.write("end_of_list.\n")

# Run Prover9 with a specific hypothesis
def check_impostor(hypothesis, player_statements):
    """
    Checks if the given hypothesis (impostor(player)) is provable using Prover9.
    """
    # Generate the .in file with the current hypothesis
    generate_amogus_in(player_statements)

    # Add the goal formula
    with open("amogus_dynamic.in", "a") as file:
        file.write("formulas(goals).\n")
        file.write(f"impostor({hypothesis}).\n")
        file.write("end_of_list.\n")

    # Run Prover9
    result = subprocess.run(["./prover9", "-f", "amogus_dynamic.in"], capture_output=True, text=True)


    # Check if the hypothesis was proved
    return "THEOREM PROVED" in result.stdout

# Main logic for identifying the impostor
def identify_impostor():
    """
    Identifies the impostor by testing each player with Prover9.
    """
    global player_sentences
    for player in ["Blue", "Yellow", "Green", "Red"]:
        if check_impostor(player, player_sentences):

            print(f"The impostor is {player}.")

            return f"The impostor is {player}."

    print("I am not sure.")


    return "I am not sure."

# Example usage with initial player statements
player_sentences = {
    "Blue": "doTaskObj(Red, task(FixMeltdown, Reactor))",
    "Green": "",
    "Yellow": "",
    "Red": ""
}
