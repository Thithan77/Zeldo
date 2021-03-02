from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=0.1, seed=123456)
for i in range(200):
    for j in range(200):
        print(noise([i,j]))
