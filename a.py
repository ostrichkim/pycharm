import click

k = click.getchar()

if k == "w":
    print(k,'up')
elif k == "s":
    print(k,'down')
elif k == "a":
    print(k,'left')
elif k == "d":
    print(k,'right')

print(k)
