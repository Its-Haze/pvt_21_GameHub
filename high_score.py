import json

import pygame


def is_not_new_user(user_id, all_score, high_score_list, game_name):
    score, *coins = all_score
    if game_name == 'tetris':
        for i, score in enumerate(high_score_list, start=1):
            if user_id == score.get('id') and score > score.get('score'):
                return i
    if game_name == 'runner':
        for i, score in enumerate(high_score_list, start=1):
            if user_id == score.get('id') and score + coins[0] > score.get('totalScore'):
                return i
    return 0


def is_high_score(all_score: tuple, high_score_list, game_name: str):
    score, * coins = all_score
    new_score = score + coins[0]
    if not new_score:
        return False
    if len(high_score_list) < 10:
        return True
    else:
        for score in high_score_list:
            if game_name == 'runner':
                if score.get('totalScore') < new_score:
                    return True
            if game_name == 'tetris':
                if score.get('score') < new_score:
                    return True
    return False


def get_data(game_name: str):

    try:
        if game_name == 'runner':
            with open('high_score.json', 'r') as f:
                high_score_list = json.loads(f.read())
        if game_name == 'tetris':
            with open('Tetris_folder/high_score_tetris.json', 'r') as f:
                high_score_list = json.loads(f.read())
        return high_score_list
    except ValueError:
        return {}


def save_high_score(data: dict, game_name: str):
    if game_name == 'runner':
        with open('high_score.json', 'w') as f:
            json.dump(data, f)
    if game_name == 'tetris':
        with open('Tetris_folder/high_score_tetris.json', 'w') as f:
            json.dump(data, f)


def create_high_score(user_id: str, total_score: tuple, game_name: str):
    score, *coins = total_score
    """return a high score to add to list"""
    if game_name == 'runner':
        return {"id": user_id, "coins": coins[0], "score": score, "totalScore": score + coins[0]}
    if game_name == 'tetris':
        return {"id": user_id, "score": score}


def add_high_core(high_score, high_score_list: list, game_name: str):
    """ add high score and return new high_score list"""
    high_score_list.append(high_score)
    if game_name == 'runner':
        high_score_list = sorted(high_score_list, key=lambda sc: sc['totalScore'], reverse=True)
    if game_name == 'tetris':
        high_score_list = sorted(high_score_list, key=lambda sc: sc['score'], reverse=True)
    if len(high_score_list) >= 10:
        high_score_list.pop()
    return high_score_list


def draw_text(screen, text: str, color, position: tuple):
    """ draw text on screen"""
    text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text_surf = text_font.render(text, False, color)
    text_rect = text_surf.get_rect(midtop=position)
    screen.blit(text_surf, text_rect)


def list_total_high_score_runner(screen, high_score_list: list):
    """ list all high score for runner game"""
    draw_text(screen, 'High Score', 'Green', (400, 50))
    draw_text(screen, 'User Id', (64, 64, 64), (250, 100))
    draw_text(screen, 'Score', (64, 64, 64), (400, 100))
    draw_text(screen, 'Coins', (64, 64, 64), (550, 100))
    y = 0
    high_score_list = sorted(high_score_list, key=lambda sc: sc['totalScore'], reverse=True)
    for score in high_score_list:
        draw_text(screen, f'{score.get("id")}', 'Grey', (250, 150 + y))
        draw_text(screen, f'{score.get("score")}', 'Grey', (400, 150 + y))
        draw_text(screen, f'{score.get("coins")}', 'Grey', (550, 150 + y))
        y += 50


def list_total_high_score_tetris(screen, high_score_list: list):
    draw_text(screen, 'High Score', (153, 0, 0), (200, 50))
    draw_text(screen, 'User Id', (204, 102, 0), (120, 100))
    draw_text(screen, 'Score', (204, 102, 0), (270, 100))
    y = 0
    high_score_list = sorted(high_score_list, key=lambda sc: sc['score'], reverse=True)
    for score in high_score_list:
        draw_text(screen, f'{score.get("id")}', (155, 128, 0), (120, 150 + y))
        draw_text(screen, f'{score.get("score")}', (155, 128, 0), (270, 150 + y))
        y += 50


def high_score(game_name: str, screen, _id: str, all_score: tuple, view: bool):
    from tetris import play_tetris
    from eriks_runner import play_runner
    clock = pygame.time.Clock()
    data = get_data(game_name)
    list_users = data.get('users')
    back_rect = pygame.rect
    if view:
        if game_name == 'runner':
            pygame.draw.rect(screen, (94, 129, 162), (0, 0, 800, 400))
            go_back_btn = pygame.image.load('Runner_folder/graphics/end_screen/back_button2.png').convert_alpha()
            go_back_surf_rect = go_back_btn.get_rect(topleft=(30, 30))
            screen.blit(go_back_btn, go_back_surf_rect)
        if game_name == 'tetris':
            back_surface = pygame.image.load('Tetris_folder/back_arrow.png').convert_alpha()
            back_rect = back_surface.get_rect(topleft=(10, 5))
            screen.blit(back_surface, back_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # save_high_score(data)
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_name == 'runner':
                            play_runner()
                        if game_name == 'tetris':
                            play_tetris()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back_surf_rect.collidepoint(event.pos):
                        if game_name == 'runner':
                            play_runner()
                    if back_rect.collidepoint(event.pos):
                        if game_name == 'tetris':
                            play_tetris()

            if game_name == 'runner':
                list_total_high_score_runner(screen, list_users)
            if game_name == 'tetris':
                list_total_high_score_tetris(screen, list_users)
            pygame.display.update()
            clock.tick(60)
    else:
        if is_high_score(all_score, list_users, game_name):
            score, *coins = all_score
            print(_id)
            index = is_not_new_user(_id, list_users)
            if index:
                if game_name == 'runner':
                    list_users[index - 1]['score'] = score
                    list_users[index - 1]['coins'] = coins[0]
                    list_users[index - 1]['totalScore'] = score + coins[0]
                if game_name == 'tetris':
                    list_users[index-1]['score'] = score
            else:
                new_score = create_high_score(_id, all_score, game_name)
                list_users = add_high_core(new_score, list_users, game_name)
            data["users"] = list_users
            save_high_score(data, game_name)


if __name__ == '__main__':
    # pygame.init()
    # pygame.display.set_caption('High Score')
    # screen = pygame.display.set_mode((800, 400))
    # high_score('tetris', screen, 'id1', (15, 0), True)
    pass


