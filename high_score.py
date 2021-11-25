import json

import pygame


def is_high_score(new_score, high_score_list):
    if len(high_score_list)< 10:
        return True
    else:
        for score in high_score_list:
            if score.get('totalScore') < new_score:
                return True
    return False


def get_data():
    try:
        with open('high_score.json', 'r') as f:
            high_score_list = json.loads(f.read())
        return high_score_list
    except ValueError:
        return {}


def save_high_score(data: dict):
    with open('high_score.json', 'w') as f:
        json.dump(data, f)


def create_high_score(user_id: str, score: int, coins: int):
    return {"id": user_id, "coins": coins, "score": score, "totalScore": score + coins}


def add_high_core(high_score, high_score_list: list):
    high_score_list.append(high_score)
    high_score_list = sorted(high_score_list,key=lambda sc: sc['totalScore'], reverse=True)
    if len(high_score_list)>= 10:
        high_score_list.pop()
    return high_score_list


def draw_text(screen, text, color, position):
    text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text_surf = text_font.render(text, False, color)
    text_rect = text_surf.get_rect(midtop=position)
    screen.blit(text_surf, text_rect)


def list_high_score(screen, high_score_list: list, field_name: str, color, position: tuple):
    x, y = position
    high_score_list = sorted(high_score_list, key=lambda sc: sc[field_name], reverse=True)
    for score in high_score_list:
        draw_text(screen, f'{score.get(field_name)}', color, (x, y))
        y += 50


def list_total_high_score(screen, high_score_list: list):
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


def high_score(screen, id, score, coins, view):

    data = get_data()
    list_users = data.get('users')
    if is_high_score(score + coins, list_users):
        list_users = add_high_core(create_high_score(id, score, coins), list_users)
        data["users"] = list_users
        save_high_score(data)
    if view:
        pygame.draw.rect(screen, (51, 153, 255), (150, 0, 500, 400))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(data)
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('runner')

            list_total_high_score(screen, list_users)
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('High Score')
    screen = pygame.display.set_mode((800, 400))
    # high_score(screen, 'ABC', 15, 25, True)


