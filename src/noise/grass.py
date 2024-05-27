import noise

def get_noise_val(x, y, seed=0):
    scale = 0.015  # Scale factor for noise granularity

    persistence = 0.80  # specifies the amplitude of each successive octave relative to the one below it
    lacunarity  = 3.5  # specifies the frequency of each successive octave relative to the one below it, similar to persistence.

    noise_val = noise.snoise2(
        x           = x * scale, 
        y           = y * scale, 
        octaves     = 20,
        persistence = persistence, 
        lacunarity  = lacunarity,
        base        = seed
    )

    noise_val += 0.90 * noise.snoise2(
        x           = x * scale, 
        y           = y * scale, 
        octaves     = 30,
        persistence = persistence, 
        lacunarity  = lacunarity,
        base        = seed
    )

    return noise_val

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import random

    seed = 26946 # random.randint(0, 100)

    xpix, ypix = 208, 208
    pic = []
    for x in range(xpix):
        row = []
        for y in range(ypix):
            noise_val = get_noise_val(x,y,seed)
            row.append(noise_val)
        pic.append(row)

    # Define a color map where 0 is blue and 1 is green
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#1CFF00", "black"])

    plt.imshow(pic, cmap=cmap)
    plt.box(False)

    # Set grid lines
    plt.grid(color='white', linestyle='dashed', linewidth=0.5)

    # Set ticks every 16 units
    plt.gca().set_xticks([(x+1)*16 for x in range(0, xpix//16)], minor=False)
    plt.gca().set_yticks([(y+1)*16 for y in range(0, ypix//16)], minor=False)

    # Remove tick labels
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])

    # Remove ticks
    plt.tick_params(length=0)

    plt.show()