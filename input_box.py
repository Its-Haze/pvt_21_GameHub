import pygame


class InputBox:
    """ Input Box class"""
    def __init__(self, x, y, w, h, color_active, color_inactive, text='',):
        self.color_inactive = pygame.Color(color_inactive)
        self.color_active = pygame.Color(color_active)
        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = self.font.render(text, False, self.color)
        self.active = False

    def handle_event(self, event):
        """ Handle all event and return text if user enter"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                # Toggle the active variable.
            else:
                self.active = False

            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode
                # Re-render the text.
            self.txt_surface = self.font.render(self.text, False, self.color)

    def update(self):
        """Resize the box if the text is too long."""
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        """ Draw text and input box"""
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
