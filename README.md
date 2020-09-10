# Classic Asteroid Game
Risks of getting lucky in space

1. ~~Generate Asteroid from flexible JSON blueprint~~
2. ~~"Mine" asteroid JSON object by randomly deducting from asteroid elements~~
3. ~~Save to a JSON file~~
4. Create Events JSON blueprint schema

    * EventID: UUID,
    * States: ["Transit"] 
        * **If left blank, can be executed upon any move**
    * Target: miner
    * Level: 3 
        * **Level 3 and higher are affected by this**
    * Luck: int 
        * **0 is good 13 is bad**
    * Power: >1000
        * **Not sure if I should check for power levels or use this to gauge how dangerous this is**
    * Shield: <5 
        * **Fix so that it scales with shield + luck modifier**
    * Category: Meteoroid
        * **Not sure how to use this other than organization**
    * Elements: ["Nitrogen"]
        * **This fits with the 'Organics'/'Mystery Object' plans**
    * Describe: "A small meteoroid `<range[1-100*Luck]>`grams in size has struck `<ship_module(s)>` causing `<Elements>` to leak.  At your current speed of `<speed>`, you will lose `<Damage=range[1-100*Luck*Speed*TTD]> <Elements>` at a current value of `<Damage*ElementMarketValue>`.  OBAI recommends the following solutions for your approval."
    * Actions: "Continue to `<Destination>` and accept loss of `<Damage*ElementMarketValue>`"
    * Results: Remove `<Damage*ElementMarketValue> / <Moves> per move`
        * **Maybe all results should assume "per move" for x moves**
    * Actions: "Repairs will take `<moves>` days, extending travel to `<Destination>`."
    * Actions: "Attempt to repair on the way? `<roll*luck>` compares to `<roll*luck>` on next move 
6. Create engine for selecting events from blueprint based on criteria of each event
7. Create Admin portal for editing blueprints **Will become precurser to game UI**
8. Use database instead of JSON files for blueprints?

### Version 2
1. Create speed, location, distance attributes.
1. Create base attributes [Mineral Processing/Water, Refinery/Fuel, Forge/Metal, Miner Ships and upgrades, ]
1. Can only repair if has 'Repair Drone', Repair Drones have levels that can speed time to repair in x moves.

Game Loop
