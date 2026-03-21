from datetime import datetime, timezone

class Note_validation:

    _MAX_LENGTH_CONTENT = 255

    @staticmethod
    def is_note_writtable(current_content: str, additional_content: str) -> bool:
        content_space_left = Note_validation._MAX_LENGTH_CONTENT - len(current_content)
        return True if content_space_left < len(additional_content) else False

    @staticmethod
    def is_integer_value(value) -> bool:
        return isinstance(value, int)

    @staticmethod
    def valid_date(date_str) -> bool:
        if date_str is None:
            return False
        
        try:
            parsed = datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return False

        if parsed.tzinfo is not None:
            return False

        today_utc = datetime.now(timezone.utc).date()
        return parsed.date() >= today_utc
