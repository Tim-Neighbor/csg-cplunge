
from operations.os_ops import is_mac


class Fonts():
    font_type = 'Arial'

    # mac fonts
    mac_default_text_box_font = (font_type, 23)
    mac_default_label_font = (font_type, 14)
    mac_default_button_font = (font_type, 14)
    mac_data_set_text_box_font = (font_type, 14)
    mac_default_entry_font = (font_type, 14)
    mac_default_list_box_font = (font_type, 16)
    mac_default_help_text_box_font = (font_type, 15)
    mac_title_text_box_font = (font_type, 20, 'bold')

    # windows fonts
    win_default_text_box_font = (font_type, 10)
    win_default_label_font = (font_type, 10)
    win_default_button_font = (font_type, 10)
    win_data_set_text_box_font = (font_type, 11)
    win_default_entry_font = (font_type, 12)
    win_default_list_box_font = (font_type, 11)
    win_default_help_text_box_font = (font_type, 11)
    win_title_text_box_font = (font_type, 16, 'bold')

    @staticmethod
    def get_text_box_font():
        return Fonts.mac_default_text_box_font if is_mac() else Fonts.win_default_text_box_font

    @staticmethod
    def get_label_font():
        return Fonts.mac_default_label_font if is_mac() else Fonts.win_default_label_font

    @staticmethod
    def get_button_font():
        return Fonts.mac_default_button_font if is_mac() else Fonts.win_default_button_font

    @staticmethod
    def get_data_set_text_box_font():
        return Fonts.mac_data_set_text_box_font if is_mac() else Fonts.win_data_set_text_box_font

    @staticmethod
    def get_entry_font():
        return Fonts.mac_default_entry_font if is_mac() else Fonts.win_default_entry_font

    @staticmethod
    def get_list_box_font():
        return Fonts.mac_default_list_box_font if is_mac() else Fonts.win_default_list_box_font

    @staticmethod
    def get_help_text_box_font():
        return Fonts.mac_default_help_text_box_font if is_mac() else Fonts.win_default_help_text_box_font

    @staticmethod
    def get_title_text_box_font():
        return Fonts.mac_title_text_box_font if is_mac() else Fonts.win_title_text_box_font
