-- Auto Skill Master Upgrade System
-- Automatically upgrades skills from level 17 to Master 1

auto_skill_master_upgrade = {}

-- Maximum normal skill level (before becoming master)
local MAX_NORMAL_SKILL_LEVEL = 17

-- Function to check and upgrade skills
function auto_skill_master_upgrade.check_and_upgrade_skills()
	local upgraded_count = 0

	-- Get all skills for the current skill group
	local skill_group = pc.get_skill_group()
	local job = pc.get_job()

	-- Define skill ranges based on job and skill group
	local skill_ranges = {
		[0] = { -- Warrior
			[1] = {1, 2, 3, 4, 5, 6},     -- Skill group 1
			[2] = {1, 2, 3, 4, 5, 6}      -- Skill group 2
		},
		[1] = { -- Assassin
			[1] = {1, 2, 3, 4, 5, 6},
			[2] = {1, 2, 3, 4, 5, 6}
		},
		[2] = { -- Sura
			[1] = {1, 2, 3, 4, 5, 6},
			[2] = {1, 2, 3, 4, 5, 6}
		},
		[3] = { -- Shaman
			[1] = {1, 2, 3, 4, 5, 6},
			[2] = {1, 2, 3, 4, 5, 6}
		}
	}

	if skill_ranges[job] and skill_ranges[job][skill_group] then
		for _, skill_index in ipairs(skill_ranges[job][skill_group]) do
			-- Calculate skill vnum
			local skill_vnum = 100 * job + skill_group * 10 + skill_index

			-- Check current skill level and grade
			local current_level = pc.get_skill_level(skill_vnum)
			local current_grade = pc.get_skill_grade(skill_vnum) or 0

			-- If skill is at level 17 and still normal grade (0), upgrade to Master
			if current_level == MAX_NORMAL_SKILL_LEVEL and current_grade == 0 then
				-- Try to upgrade to Master
				if pc.learn_master_skill(skill_vnum) then
					-- Success! Send notification to player
					syschat(string.format("Skill upgraded to Master: %s", skill_vnum))
					upgraded_count = upgraded_count + 1

					-- Log for debugging
					print(string.format("[AUTO_SKILL_UPGRADE] Player %s upgraded skill %d to Master", pc.get_name(), skill_vnum))
				else
					-- Failed to upgrade (maybe not enough requirements)
					print(string.format("[AUTO_SKILL_UPGRADE] Failed to upgrade skill %d for player %s", skill_vnum, pc.get_name()))
				end
			end
		end
	end

	-- Notify player if any skills were upgraded
	if upgraded_count > 0 then
		syschat(string.format("%d skill(s) automatically upgraded to Master!", upgraded_count))
	end

	return upgraded_count
end

-- Alternative function using direct skill level manipulation (if learn_master_skill doesn't work)
function auto_skill_master_upgrade.force_upgrade_skill(skill_vnum)
	-- This is a fallback method if the normal upgrade doesn't work
	local current_level = pc.get_skill_level(skill_vnum)

	if current_level == MAX_NORMAL_SKILL_LEVEL then
		-- Force set skill grade to Master (1) and level to 1
		-- Note: This might not work depending on server implementation
		pc.set_skill_level(skill_vnum, 1)
		pc.set_skill_grade(skill_vnum, 1)

		return true
	end

	return false
end