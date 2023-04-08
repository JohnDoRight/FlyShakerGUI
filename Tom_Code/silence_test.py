import time
import cv2

def wait_elapsed_time(time_to_wait):

    start_time = time.monotonic()

    elapsed_time = 0

    # Load a dummy image (actual version should say "Press any key or spacebar to stop the silence")
    img = cv2.imread('stop_image.png')

    while elapsed_time < time_to_wait:

        time.sleep(1)

        current_time = time.monotonic()
        elapsed_time = current_time - start_time

        # print("elapsed_time:", elapsed_time)
        print(f"elapsed_time: {elapsed_time:.1f} seconds")

        cv2.imshow("img", img)

        key = cv2.waitKey(1000)
        print(key)
        if key == ord('a'):
            print("You pressed a")
        if key == 32:
            print("You pressed spacebar")

        if key >= 0:
            print("You pressed any key, breaking loop")
            break

    print(f"elapsed_time: {elapsed_time:.1f} seconds")
    cv2.destroyAllWindows()
    print("End of Loop")


    pass


def main():
    print("Main")

    # seconds
    time_to_wait = 10

    wait_elapsed_time(time_to_wait)



    pass


if __name__ == "__main__":
    main()
