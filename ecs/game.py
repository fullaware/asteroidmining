#!/usr/bin/env python3
"""
    Getting into space is expensive and risky
    Running a mining operation is expensive and risky
    Running a mining operation in space is crazy expensive and borderline insane.
    This requires investors
    Investors want to make back their money at least 5X
    Their initial investment gets you a base of operations and 2 mining ships.
    You have 30? days to locate an asteroid and start mining in order to continue funding.
    Once you hit critical mass, making enough money to no longer require investment 
    the game is truly in your hands.  You have up to 4 rounds of funding with various perks to help you achieve success.
    Smart strategy and a little luck will keep you running.
    Sound too easy?  Once you prove that mining asteriods is a profitable endeavour the more risk adverse investors
    will send fully decked out mining operations with everything you have (albeit a littler newer) with the exception 
    of a claim on asteroids.  Asteroids can only be claimed by physically tagging them with an encryption beacon that 
    notifies anyone else attempting to mine that rock that whatever profit is made, a percentage
    must be paid to the beacon holder after agreeing to the amount (can vary from 18-60%) in a contract. 
        AI Intelligence modifier offsets RISKS + bad luck modifier
    The days will go by in a flash, each piece of equipment is automated with 
    an On-Board Artificial Intelligence or "Oh Boy" for short that will only alert you if something needs organic based triage.
        O.B.A.I. computer systems have RISKS
        Traveling to an asteroid has RISKS
        Landing on an asteroid to mine has RISKS
        Mining at a profitable rate has RISKS
    Mine and return with raw materials to get next round of funding
        $ of investment is determined by your rate of success (rate of extraction - operating costs)
    Next round gives you a processing ship for water > hydrogen which is where you start making 
    money to receive next round of funding.
        Operating a hydrogen processing ship has RISKS
    Next round gives you 2 more mining ships with larger capacity.
    Next round gives you ore refinery for processing iron.
    Next round gives you 3 more mining ships with ability to process their own fuel from ice

    Asteroids will have a speed, this speed determines how long you can safely mine materials
    and return to base.
    Speed of travel to the asteroid and away laden with material is based on the 
    power of the vessel.  Power used for mining and engines.
"""

"""
    an entity is a collection of components which provide functionality. 

    Ship - Power, Fuel, Storage, Value
    Asteroid - Ice, Silica, Iron, Platinum, Value
    Base - Fuel, Shield, Storage, Value

"""

struct Entity {
    unsigned int id
}

struct HealthComponent {
    int currentHealth
    int maxHealth
}
"""
    Component   Description
    Transform   x,y coordinates
    Motion      acceleration, velocity
    Sprite      file to use as spritesheet, current sprite
    Collision   Size of collision box (w, h)
    Health      Current HP, Max HP
    Follow      Who to follow (entity)
"""


class EntityManager:
    {pass}


class HealthManager:
    {pass}


foreach(entity hit by bomb):
    HealthComponent hp = entity.getHealth()
    hp.maxHealth = hp.maxHealth * 0.8

struct Transform {
    int x
    int y
}
struct Motion {
    Vec2 velocity
    Vec2 acceleration
}

# Movement System
void update(int dt){
    for(entity in m_entities){
        TransformComponent position = entity.getTransform()
        MotionComponent motion = entity.getMotion()
        position.x += motion.velocity.x
        position.y += motion.velocity.y
        motion.velocity.x += motion.acceleration.x
        motion.velocity.y += motion.acceleration.y
    }
}

"""

remember that a system will only pay attention to an entity that has *all* of the required components

System          Components Required     Description
======          ===================     ===========
Movement        Transform, Motion       Updates position based on velocity
Player Input    Joystick, Motion        Changes player velocity based on arrow key presses     
Collision       Collision, Transform    Checks for collisions and resolves them
Follow          Transform, Motion, Follow   Changes velocity based on where the player is
Render          Transform, Sprite       Render the sprite to the screen


"""
