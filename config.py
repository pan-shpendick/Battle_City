volume = 5
menu_selected = 0
settings_mode = False
game_state = "menu"
player_spawned = False
game_over = False
game_over_start_time = 0

enemy_spawn_time = 0
enemy_spawned_count = 0
enemy_max_count = 18
enemy_alive_limit = 5
enemy_remaining_count = 18

player_lives = 3
player_score = 0

killed_normal = 0
killed_fast = 0

start_sound_played = False
defeat_sound_played = False


def reset_stats():
    global player_score, killed_normal, killed_fast
    player_score = 0
    killed_normal = 0
    killed_fast = 0