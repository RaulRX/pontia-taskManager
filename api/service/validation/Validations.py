from starlette.responses import Content


class Note_validation:

    _MAX_LENGTH_CONTENT = 255
    
    @staticmethod
    def is_note_writtable(current_content: str, additional_content: str) -> bool:
        content_space_left = Note_validation._MAX_LENGTH_CONTENT - len(current_content)
        return True if content_space_left < len(additional_content) else False