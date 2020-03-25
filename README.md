# Context-Aware-Recommender-System

A context-aware recommendation system for music data in cars

# Running the program

To start the program:

1) Open a command prompt
2) Navigate to the root directory
3) Type `python Interface.py`

# Main menu

When the program starts, enter a valid user ID (1001 to 1042). 
Enter a context when prompted: `u` for urban, `m` for mountains, `cs` for countryside, or `cl` for coastline - press `v` to view these options in the menu at this point.

At the main menu, press:

`G` to generate your recommendations,
`E` to enter evaluation mode,
    Press `M` to calculate the mean absolute error
          `P` to calculate the precision
          `R` to calculate the recall
          `B` to return to the main menu
`S` to configure the settings
    Press `R` to change # of recommendations to display
          `C` to change the current landscape context
          `B` to return to the main menu
`X` to sign out of the system
`Q` to quit the system

The evaluation metrics may take a few minutes to run (especially MAE), so please be patient.
