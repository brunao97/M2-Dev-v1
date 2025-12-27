---
trigger: always_on
---

# Metin2 Questing Development

This document provides a guide for creating and managing quests in the Metin2 server environment.

## Quest Structure
All quests must follow a specific hierarchical structure using Lua syntax.

```lua
quest <questname> begin
    state start begin
        -- Events and triggers go here
    end
end
```

## Common Triggers (when)
Triggers define when a specific block of code should be executed.

- `login`: Triggered when a player logs into the game.
- `logout` / `disconnect`: Triggered when a player leaves the game.
- `kill`: Triggered when a player kills a monster/player.
- `party_kill`: Triggered when a party member kills a monster.
- `click`: Triggered when a player clicks on an NPC.
- `<mob_vnum>.chat."Selection"`: Adds a menu option to an NPC that triggers when selected.
- `take`: Triggered when a player drags an item onto an NPC.
- `button` / `info`: Triggered when a player clicks a quest scroll (usually used together).

## Conditions (with)
Use the `with` keyword to add logic constraints to triggers.

```lua
when login with pc.get_level() >= 25 begin
    chat("Welcome, veteran!")
end
```

## Essential Functions

### Interaction & UI
- `say_title("Title")`: Sets the header of the quest dialog.
- `say("Message")`: Displays text in the quest dialog.
- `say_reward("Message")`: Displays text in a reward-highlighted color.
- `wait()`: Pauses the dialog and waits for the player to click "Next".
- `chat("Message")`: Sends a message to the player's local chat area.
- `notice("Message")`: Sends a server-wide notice message.

### Player & NPC Data (pc & npc)
- `pc.get_name()`: Returns the player's name.
- `pc.get_level()`: Returns the player's current level.
- `pc.give_item2(vnum, count)`: Adds items to the player's inventory (preferred over `give_item`).
- `npc.get_race()`: Returns the Vnum of the NPC/Monster currently being interacted with.

## String Concatenation
Use `..` to combine strings and variables.
```lua
say("Hello " .. pc.get_name() .. "!")
```

## Implementation Workflow
1.  **Create file**: Add your quest to `m2server/main/srv1/share/locale/germany/quest/` (or your specific locale).
2.  **Add to list**: Add the quest filename to `locale_list` or `quest_list` in the same directory.
3.  **Compile**: Use the quest compiler (`qc`) to process the quest.
    ```bash
    ./qc my_quest.quest
    ```
4.  **Reload**: In-game, use `/reload q` as a GM to apply changes without restarting the server.
