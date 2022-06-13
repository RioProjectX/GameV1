from datetime import datetime

class LimitHelper:
    def __init__(self):
        self.private_limit = 2
        self.group_limit = 4

    def get_time(self):
        return datetime.now()

    def is_limited(self, ctx, types):
        data = ctx.user_data if types == "private" else ctx.chat_data
        limit = self.private_limit if types == "private" else self.group_limit 

        past = data["time"] if "time" in data else None
        if not past:
            data["time"] = self.get_time()
            return False

        now = self.get_time()
        difference = (now - past).total_seconds()

        result = True if difference <= limit else False
        return result

    def is_admin(self, ctx, chat_id):
        me = ctx.bot.get_me()
        status = ctx.bot.get_chat_member(chat_id, me.id)

        if ( status.status != "administrator" or not status.can_delete_messages ):
            return False

        return True

limiter = LimitHelper()