def lerp(start_angle, end_angle, steps):
#a + (b-a) * weight
    return start_angle + (end_angle - start_angle) * steps


print (lerp(0, 360, 0.5))
