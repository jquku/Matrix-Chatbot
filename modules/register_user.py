class Registration:

    import nio

    def __init__(self):
        print("init")
        register_new_user(self)


    def register_new_user(self):
        user = "chatbot:matrix.org"
        password = "chatbot123454321"
        device_name = ""
        device_id = ""
        self.register(user, password, device_name, device_id)

    if __name__ == '__main__':
        #register_new_user(self)
        print("main call")
