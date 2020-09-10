# Classic Asteroid Game
Risks of getting lucky in space

1. ~~Generate Asteroid from flexible JSON blueprint~~
2. ~~"Mine" asteroid JSON object by randomly deducting from asteroid elements~~
3. ~~Save to a JSON file~~
4. Create Events JSON blueprint schema

    * EventID: UUID,
    * MoveState: 
        ```
            [   traveling,
                mining,
                travelingLaden,
                arrivingRescue,
                arrivingRepair,
                arrivingAsteroid ]
        ```
        * **If left blank, can be executed upon any move**
    * Target: miner
    * LevelCheck: 3 
        * **Level 3 and higher are affected by this**
    * LuckCheck: int 
        * **0 is good 13 is bad**
    * PowerCheck: >1000
        * **Not sure if I should check for power levels or use this to gauge how dangerous this is**
    * ShieldCheck: 5 
        * **Fix so that it scales with shield + luck modifier**
    * Category: Meteoroid
        * **Not sure how to use this other than organization**
    * ElementCheck: `["Nitrogen"]`
        * **This fits with the 'Organics'/'Mystery Object' plans**
    * Describe: 
      * "A small meteoroid `<range[1-100*Luck]>`grams in size has struck `<ship_module(s)>` causing `<Elements>` to leak.  
        At your current speed of `<speed>` you will lose `<Damage=range[1-100*Luck*Speed*TTD]> <Elements>` at a current value of `<Damage*ElementMarketValue>`.  
        OBAI recommends the following solutions for your approval."
    * Actions: 
      1. "Continue to `<Destination>` and accept loss of `<Damage*ElementMarketValue>`"
         * Results: 
           * Remove `<Damage*ElementMarketValue> / <Moves> per move`
        * **Maybe all results should assume "per move" for x moves**
      2. "Repairs will take `<moves>` days, extending travel to `<Destination>`."
      3. "Attempt to repair on the way? `<roll*luck>` compares to `<roll*luck>` on next move 
5. Create engine for selecting events from blueprint based on criteria of each event
6. Create Admin portal for editing blueprints
   * **Will become precurser to game UI**
7. Use database instead of JSON files for blueprints?

## Version 2
1. Create speed, location, distance attributes.
1. Create base attributes `[Mineral Processing/Water, Refinery/Fuel, Forge/Metal, Miner Ships and upgrades, ]`
1. Can only repair if has a 'Repair Drone', Repair Drones have levels that can speed time to repair in x moves.

## Game Loop
```
While gameOn isTrue:
	ORDER By EventQueueFIFO()
		THEN EventQueuePriority
    EXECUTE Tasks in EventQueue
```
## Game Logic
traveling = unladen with any materials, if ship is hit by meteoroid, and `<shield>` isn't more powerful than impact `<Damage=[TimeToRepair,]>`
travelingLaden = has material mass which is in 'front' during travel, will add to shield bonus, HOWEVER, depending on mass
