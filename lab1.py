class CubeWorld:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.matrix = [['0' for _ in range(width)] for _ in range(length)]
        self.logging = []

    def print_world(self):
        for row in self.matrix:
            print(' '.join(row))

    def place_block(self, block, x, y):
        if x < self.length and y < self.width:
            self.matrix[x][y] = block
        else:
            print("Invalid coordinates.")

    def grasp(self, block):
        self.logging.append(f"Grasped {block}")

    def move(self, block_1, block_2, get_rid_of=False):
        if get_rid_of:
            self.logging.append(f"Cleared top of {block_1}")
        self.logging.append(f"Put {block_1} on {block_2}")
        if get_rid_of:
            self.logging.append(f"Got rid of {block_2}")

        x1, y1 = self.find_block_coords(block_1)
        x2, y2 = self.find_block_coords(block_2)
        self.matrix[x1][y1] = '0'
        self.matrix[x2][y2] = block_1

    def put_on(self, block_1, x, y):
        block_2 = self.matrix[x][y]
        if block_2 != '0':
            print(f"Cell ({x}, {y}) is occupied. Please choose another destination.")
            new_x, new_y = map(int, input("Enter new destination coordinates (x, y): ").split(','))
            self.put_on(block_1, new_x, new_y)
            return

        # Check if there are blocks above the block to be moved
        if self.has_blocks_above(x, y):
            print(f"Cannot move block {block_1} yet. There are blocks on top of it.")
            return

        self.grasp(block_1)
        self.move(block_1, block_2, get_rid_of=True)
        path = self.get_path(block_1, (x, y))
        print(f"Moved block {block_1} to ({x}, {y}) along path: {path}")

    def has_blocks_above(self, x, y):
        return any(self.matrix[i][y] != '0' for i in range(x))

    def find_block_coords(self, block):
        for i in range(self.length):
            for j in range(self.width):
                if self.matrix[i][j] == block:
                    return i, j
        return -1, -1

    def get_path(self, block_1, dest_coords):
        x1, y1 = self.find_block_coords(block_1)
        x2, y2 = dest_coords
        path = [(x1, y1)]
        while (x1, y1) != (x2, y2):
            if x1 < x2:
                x1 += 1
            elif x1 > x2:
                x1 -= 1
            if y1 < y2:
                y1 += 1
            elif y1 > y2:
                y1 -= 1
            path.append((x1, y1))
        return path

def main():
    length = 3
    width = 3
    world = CubeWorld(length, width)

    num_blocks = int(input("Enter the number of blocks: "))
    for i in range(num_blocks):
        block = input(f"Enter block {i+1} coordinates (x, y): ").split(',')
        x, y = int(block[0]), int(block[1])
        world.place_block(str(i+1), x, y)

    world.print_world()

    while True:
        from_block = input("Enter block to move (block number): ")
        x_dest, y_dest = map(int, input("Enter destination coordinates (x, y): ").split(','))

        if from_block.isdigit():
            x_from, y_from = world.find_block_coords(from_block)
            if not is_top_block(world, x_from, y_from) or has_blocks_above(world, x_from, y_from):
                print("Cannot move the block yet.")
                continue
            
            world.put_on(from_block, x_dest, y_dest)  # Corrected coordinates order
            world.print_world()
            break
        else:
            print("Invalid input. Please enter block numbers.")

def is_top_block(world, x, y):
    return x == 0 or world.matrix[x - 1][y] == '0'

def has_blocks_above(world, x, y):
    return any(world.matrix[i][y] != '0' for i in range(x))

if __name__ == "__main__":
    main()
