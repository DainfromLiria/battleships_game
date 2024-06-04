"""
    Class that represents chat between two players.
"""
import sys
import copy
from typing import List
import pygame as pg

from utils.settings import COLORS, BASE, FONT_SIZE, FONT_NAME, CHAT
from utils.helper import draw_text, draw_rect
from online.network import Network


class Chat:
    """Class that represents chat between two players.

    Attributes:
    """
    def __init__(self):
        self.input_box = pg.Rect(BASE["WIDTH"] // 2 - 150, BASE["HEIGHT"] // 2 + 300, 300, 23)
        self.output_box = pg.Rect(BASE["WIDTH"] // 2 - 150, BASE["HEIGHT"] // 2 + 185, 300, 100)
        self.input_box_color = COLORS["GRAY"]
        self.active = False
        self.text = ''
        self.messages = []
        self.scroll = 0

    def draw(self, net: Network) -> None:
        """Draw chat. Draw rect with inputted user's messages and
        draw rect with all messages.

        Attributes:
            net - Network - used for synchronize text in output text box.
        """
        self.input_text_box()
        self.output_text_box(net)

    def is_in_chat(self, x, y) -> bool:
        """Check if user is clicked on input or output chat box.

        Attributes:
            x - int - x coordinate of mouse click.
            y - int - y coordinate of mouse click.
        Return:
            bool -True if user is clicked on input or output box, False otherwise.
        """
        return self.input_box.collidepoint(x, y) or self.output_box.collidepoint(x, y)

    @staticmethod
    def get_text_width(text: str) -> int:
        """Get text as string and calculate his width using chat's font.

        Attributes:
            text - str - text of the message.
        Return:
            int - width of the text.
        """
        font = pg.font.SysFont(FONT_NAME["CHAT"], FONT_SIZE["CHAT"])
        return font.size(text)[0]

    def split_text(self, box: pg.Rect = None) -> List[str]:
        """Split input text on parts that can be shown in the output chat box.

        Attributes:
            box - pg.Rect - output text box,
            by default None for split text in message list.
        Return:
            List[int] - list of split parts of the text.
        """
        split_texts = []
        tmp_text = self.text
        txt_part = ''
        for c in self.text:
            txt_part += c
            text_width = self.get_text_width(txt_part)
            if text_width > 280:
                tmp_text = tmp_text[len(txt_part):]
                split_texts.append(txt_part[:-1])
                if box is not None:
                    box.h += 20
                tmp_text += txt_part[-1]
                txt_part = ''
        split_texts.append(tmp_text)
        return split_texts

    def input_text_box(self) -> None:
        """Draw box where user enters message.
        Draw rect and in this rect users entered text.
        """
        box = copy.deepcopy(self.input_box)
        texts = self.split_text(box)
        ofs = 0
        draw_rect(box, self.input_box_color, 2)
        for txt in texts:
            dest = (box.x + 5, box.y + ofs + 5)
            draw_text(txt, dest, FONT_SIZE["CHAT"], FONT_NAME["CHAT"], COLORS["BLACK"])
            ofs += 20

    def output_text_box(self, net: Network) -> None:
        """Draw box where is all chat messages.
        Firstly ask server if other player sent some messages and sent
        his list of messages. Then draw output box (rect) with text from list
        of messages (self.messages).

        Attributes:
            net - Network - player part of online.
        """
        self.messages = net.send(("chat", self.messages))

        dst_label = (BASE["WIDTH"] // 2 - 20, BASE["HEIGHT"] // 2 + 160)
        draw_text("Chat", dst_label, FONT_SIZE["CHAT"])

        min_msg = max(-1, len(self.messages) - 5)
        max_msg = len(self.messages) - 1
        scroll_ofs = self.scroll // 10
        if scroll_ofs < 0:
            min_msg = max(-2, min(min_msg, min_msg + scroll_ofs))
            # don't allow scroll higher than first message
            if min_msg == -2:
                min_msg = -1
                self.scroll += 10
            max_msg = min(max_msg, max_msg + scroll_ofs)
        else:
            # don't allow scroll lower than last message
            self.scroll = 0
        draw_rect(self.output_box, COLORS["BLACK"], 2)

        ofs = 0
        for i in range(max_msg, min_msg, -1):
            w = BASE["WIDTH"] // 2 - 145
            # self.scroll * 0.001 is for minimize dist between messages in output_box
            # during scrolling.
            h = BASE["HEIGHT"] // 2 + 265 - ofs + self.scroll * 0.001
            draw_text(self.messages[i], (w, h), FONT_SIZE["CHAT"],
                      FONT_NAME["CHAT"], COLORS["BLACK"])
            ofs += 21

    def chat_loop(self) -> bool:
        """Main method of this class. Handling all events in chat.

        Return:
            bool - True if chat is active, False if not."""
        self.active = True
        self.input_box_color = COLORS["GREEN"]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # leave chat
                if not self.is_in_chat(event.pos[0], event.pos[1]):
                    self.active = False
                    self.input_box_color = COLORS["GRAY"]
                    return self.active
            # typing messages and store it in message list
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN and len(self.text) > 0:
                    txt_split = self.split_text()
                    for i, txt in enumerate(txt_split):
                        txt = "> " + txt if i == 0 else "   " + txt
                        self.messages.append(txt)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < CHAT["MAX_MSG_SIZE"]:
                        self.text += event.unicode
            # scrolling
            if event.type == pg.MOUSEWHEEL:
                self.scroll -= event.y * CHAT["SCROLL_SPEED"]
        return self.active
