import CameraSecurity

if __name__ == "__main__":
    try:
        CameraSecurity.CameraSecurity(23)
    except BaseException:
        print("process killed")
