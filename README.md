# Classic Asteroid Game
Risks of getting lucky in space

- [Classic Asteroid Game](#classic-asteroid-game)
  - [TODO](#todo)
  - [TODO Version 2](#todo-version-2)
  - [Game Loop](#game-loop)
  - [Game Logic](#game-logic)
    - [1. Turn execution](#1-turn-execution)
    - [2. TurnStates - Definitions](#2-turnstates---definitions)

## TODO
1. ~~Generate Asteroid from flexible JSON blueprint~~
2. ~~"Mine" asteroid JSON object by randomly deducting from asteroid elements~~
3. ~~Save to a JSON file~~
4. Create Events JSON blueprint schema
   * **In Progress**
   * DEV NOTES:
      * [`events_blueprint.json`](data/events_blueprint.json) outline drafted, needs schema
5. Build "Luck" system simulator to test game logic.
   * **In Progress**
   * DEV NOTES:
      * Current Luck system is based on a random width moving range within 1-20 & coinflip (0 bad 1 good).
         * Simple Example:  `range_width = 5, range_start = 5, range_end = 10`
      * If d20 = within range, take damage.  Good results; range of unassisted turns is 100 - 260+ but VERY hard to code.
         * d20 = 1 & coin bad = Guaranteed damage random(1,6)
         * d20 = 5-10 & coin bad = Damage random(1,6)
         * d20 = 5-10 & coin good = damage is 1 due to 'evasive maneuver' 
         * d20 != 5-10 & coin good = Dodge damage 0 due to 'evasive maneuver'
         * d20 = 20 & coin good = Evade completely, no threat
      * Instead of random width, limit to width options to 1,3,5,7
      * Reverse 'Luck' range of 0 = bad 13 = good, that way the higher the bad luck the higher the modifier of bad things?
      * OR THROW AWAY range idea and use D20 initiative, 4 fates 4d6
         * Odd is negative
         * Even is Positive
         * 4 positives locks 1 d6 to positive for next round
         * 4 positives AGAIN locks 2 d6 to positive for next round, resume 4d6
         * Same for Negative
      * OR THROW AWAY d20, JUST use 2d6s (FATE alternative). You roll one as positive and one as negative. Subtract the value of the negative d6 from the value of the positive one. So if you roll a 4 on the positive and 2 on the negative, that's a +2. If you roll 3 on the positive and 6 on the negative, that's a -3.  The range of that is from -5 to +5. 

7. Create query engine for selecting events from blueprint based on criteria of each event
8. Create Admin portal for editing blueprints
   * **Will become precurser to game UI**
9. Create speed, location, distance attributes.


Rescue mission finds 2 closest miners + dedicated rescue ship.

Each miner is equipped with a basic repair drone.


## TODO Version 2
1. Create base attributes `[Mineral Processing/Water, Refinery/Fuel, Forge/Metal, Habitat, Hydroponics, Miner/Transport Ships and upgrades, ]`
2. Use database instead of JSON files for blueprints?
3. Can only repair if has a 'Repair Drone', Repair Drones have levels that can speed time to repair in x moves.

## Game Loop
   ```
   while gameOn isTrue:
      ORDER by EventQueue().FIFO()
         THEN ORDER by EventQueue().Priority()
      for tasks in EventQueue():
         EventQueue().execute()
   ```
## Game Logic

### 1. Turn execution  
   Upon execution of the turn, an 'Initiative Roll d20' and 'Luck Roll ?' are used to impact the effectiveness of the turn.  

Set range of "fate" within each event manually per event?  
Set range of "fate" within each event based on Luck?  
Set range of "fate" within each event with another d20?  

   * 10-19 initiative + good or bad luck. No New events.  
   * 2-9 initiative + bad luck. 
      * Query Events for matching criteria, and execute with `<Initiative + Luck>`.  
   * 20 initiative + good luck. +1 to good luck modifier
   * 1 initiative + bad luck. +1 to bad luck modifier AND
      * Query Events for matching criteria, and execute with `<Initiative + Luck>`.

### 2. TurnStates - Definitions
   Each turn is categorized by what kind of actions can be executed against them.  


   * `traveling` = unladen with any materials. If ship is hit by meteoroid, and `<shield>` isn't more powerful than impact, execute `<Damage=[TimeToRepair * Luck]>`
   * `travelingLaden` = Since material mass is in 'front' during travel, this will add to shield bonus.  Instead of impacting ship, it could impact the cargo and a value loss if not repaired.  Repairs can be done in transit `<Initiative + Luck>` OR stop for repairs = lost time.
   * `repairing` = Ship is stopped for for x turns for repair. `<RepairTime-1>`
   * `mining` = Each miner will execute mining on turn. `<Initiative ? Luck ? Power>`
   * `arrivingRescue` = Miners can be sent to rescue other miners.  They are valuable assets after all, especially if they are loaded with materials.
   * `arrivingAsteroid` = All sorts of things can go wrong/right on approach to your target. At this stage, the miner is scanning surface for optimal mining site.  