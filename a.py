import click

k = click.getchar()

print(k)

if k == "\x1b[A":
    print("up")
elif k == "\x1b[B":
    print('down')
elif k == "\x1b[D":
    print('left')
elif k == "\x1b[C":
    print('right')
