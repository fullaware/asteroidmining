# Classic Asteroid Game
Risks of getting lucky in space

## TODO
1. ~~Generate Asteroid from flexible JSON blueprint~~
2. ~~"Mine" asteroid JSON object by randomly deducting from asteroid elements~~
3. ~~Save to a JSON file~~
4. Create Events JSON blueprint schema
5. Create query engine for selecting events from blueprint based on criteria of each event
6. Create Admin portal for editing blueprints
   * **Will become precurser to game UI**
7. Create speed, location, distance attributes.

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
   * 10-19 initiative + good or bad luck. No New events.  
   * 2-9 initiative + bad luck. 
      * Query Events for matching criteria, and execute with `<Initiative + Luck>`.  
   * 20 initiative + good luck. +1 to good luck modifier
   * 1 initiative + bad luck. +1 to bad luck modifier AND
      * Query Events for matching criteria, and execute with `<Initiative + Luck>`.

### 2. TurnStates - Definitions
Each turn is categorized by what kind of actions can be executed against them.  Upon execution of the turn, an 'Initiative Roll d20' and 'Luck Roll bool' are used to impact the effectiveness of the turn.

* `traveling` = unladen with any materials. If ship is hit by meteoroid, and `<shield>` isn't more powerful than impact, execute `<Damage=[TimeToRepair * Luck]>`
* `travelingLaden` = Since material mass is in 'front' during travel, this will add to shield bonus.  Instead of impacting ship, it could impact the cargo and a value loss if not repaired.  Repairs can be done in transit `<Initiative + Luck>` OR stop for repairs = lost time.
* `repairing` = Ship is stopped for for x turns for repair. `<RepairTime-1>`
* `mining` = Each miner will execute mining on turn. `<Initiative ? Luck ? Power>`
* `arrivingRescue` = Miners can be sent to rescue other miners.  They are valuable assets after all, especially if they are loaded with materials.
* `arrivingAsteroid` = All sorts of things can go wrong/right on approach to your target. At this stage, the miner is scanning surface for optimal mining site.  