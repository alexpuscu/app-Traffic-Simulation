from utils import Direction, is_horizontal, manhattan_distance

class Place(object):

    def __init__(self, block, number):
        self.block = block
        self.number = number


class Route(object):

    def __init__(self, blocks, origin, destiny):
        self.blocks = blocks
        self.index = 0
        self.origin = origin
        self.destiny = destiny


class Block(object):

    def __init__(self, number, road, from_n, to_n):
        self.number = number
        self.road = road
        self.from_n = from_n
        self.to_n = to_n
        self.cars = []


class Road(object):

    def __init__(self, number, direction, size, blocks_count, city):
        self.number = number
        self.direction = direction
        self.blocks = []
        self.size_per_block = size / blocks_count
        for i in range(blocks_count):
            self.blocks.append(Block(i, self, i * self.size_per_block, (i + 1) * self.size_per_block))

        self.city = city

    def get_block(self, position):
        index = int(position / self.size_per_block)
        final_index = 0 if index < 0 else index - 1 if index >= len(self.blocks) else index
        return self.blocks[final_index]

    def get_next_block(self, block):
        index = block.number
        if self.direction == Direction.NS or self.direction == Direction.WE:
            if index + 1 < len(self.blocks):
                return self.blocks[(index + 1)]
            return
        else:
            if index - 1 >= 0:
                return self.blocks[(index - 1)]
            return

    def get_next_turning_block(self, block):
        index = block.number
        if self.direction == Direction.NS:
            road = self.city.horizontal_roads[(index + 1)]
            if road.direction == Direction.WE:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            block_number = self.number - 1
            if block_number >= 0:
                return road.blocks[block_number]
            return
        if self.direction == Direction.SN:
            road = self.city.horizontal_roads[index]
            if road.direction == Direction.WE:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            block_number = self.number - 1
            if block_number >= 0:
                return road.blocks[block_number]
            return
        if self.direction == Direction.WE:
            road = self.city.vertical_roads[(index + 1)]
            if road.direction == Direction.NS:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            block_number = self.number - 1
            if block_number >= 0:
                return road.blocks[block_number]
            return
        if self.direction == Direction.EW:
            road = self.city.vertical_roads[index]
            if road.direction == Direction.NS:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            block_number = self.number - 1
            if block_number >= 0:
                return road.blocks[block_number]
            return

    def get_priority_block(self, block):
        index = block.number
        if self.direction == Direction.NS:
            road = self.city.horizontal_roads[(index + 1)]
            if road.direction == Direction.WE:
                block_number = self.number - 1
                if block_number >= 0:
                    return road.blocks[block_number]
                return
            return
        if self.direction == Direction.SN:
            road = self.city.horizontal_roads[index]
            if road.direction == Direction.EW:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            return
        if self.direction == Direction.WE:
            road = self.city.vertical_roads[(index + 1)]
            if road.direction == Direction.SN:
                block_number = self.number
                if block_number < len(road.blocks):
                    return road.blocks[block_number]
                return
            return
        if self.direction == Direction.EW:
            road = self.city.vertical_roads[index]
            if road.direction == Direction.NS:
                block_number = self.number - 1
                if block_number >= 0:
                    return road.blocks[block_number]
                return
            return