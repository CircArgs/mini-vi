import curses
import sys

def main(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)
    max_y, max_x = stdscr.getmaxyx()
    buffer = ['']
    y, x = 0, 0
    mode = 'COMMAND'
    message = ''

    while True:
        stdscr.clear()
        for idx, line in enumerate(buffer):
            stdscr.addstr(idx, 0, line)
        stdscr.addstr(max_y - 1, 0, f'-- {mode} -- {message}')
        stdscr.move(y, x)
        stdscr.refresh()

        key = stdscr.getch()
        message = ''

        if mode == 'COMMAND':
            if key == ord('i'):
                mode = 'INSERT'
            elif key == ord('h'):
                x = max(0, x - 1)
            elif key == ord('l'):
                x = min(len(buffer[y]), x + 1)
            elif key == ord('k'):
                y = max(0, y - 1)
                x = min(len(buffer[y]), x)
            elif key == ord('j'):
                y = min(len(buffer) - 1, y + 1)
                x = min(len(buffer[y]), x)
            elif key == ord(':'):
                message = ''
                stdscr.addstr(max_y - 1, 0, ':')
                curses.echo()
                command = stdscr.getstr(max_y - 1, 1).decode()
                curses.noecho()
                if command == 'w':
                    with open('output.txt', 'w') as f:
                        f.write('\n'.join(buffer))
                    message = 'File saved as output.txt'
                elif command == 'q':
                    return
                else:
                    message = f'Unknown command: {command}'
        elif mode == 'INSERT':
            if key == 27:  # ESC key
                mode = 'COMMAND'
            elif key in (curses.KEY_BACKSPACE, 127):
                if x > 0:
                    buffer[y] = buffer[y][:x - 1] + buffer[y][x:]
                    x -= 1
                elif y > 0:
                    x = len(buffer[y - 1])
                    buffer[y - 1] += buffer[y]
                    del buffer[y]
                    y -= 1
            elif key == curses.KEY_ENTER or key == 10:
                buffer.insert(y + 1, buffer[y][x:])
                buffer[y] = buffer[y][:x]
                y += 1
                x = 0
            else:
                buffer[y] = buffer[y][:x] + chr(key) + buffer[y][x:]
                x += 1

        # Adjust for window resizing
        max_y, max_x = stdscr.getmaxyx()
        y = min(y, max_y - 2)
        x = min(x, max_x - 1)

if __name__ == '__main__':
    curses.wrapper(main)
