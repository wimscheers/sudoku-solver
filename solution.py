import json

def eliminate(values):

    SearchService().eliminate(values)

def naked_twins(values):

    SearchService().naked_twins(values)

class Sudoku:

    """Defines a Sudoku grid with number data
       In the form of  '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    """
    def __init__(self, title, grid):
        """

        @param title: The title of the sudoku to solve
        @type title: str
        @param grid: number data in the form of  '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
        @type grid: str
        """
        self.title = title
        self.grid = grid
        self.searchservice = SearchService()

    def search(self) -> str:
        return self.searchservice.convert_grid_from_string_to_dict(self.grid)

class SearchService:
    rows = 'ABCDEFGHI'
    cols = '123456789'
    values = dict()

    assignments = []

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def __init__(self) -> None:
        values = dict()
        self.boxes = self.cross('ABCDEFGHI', '123456789')

        row_units = [self.cross(r, self.cols) for r in self.rows]
        column_units = [self.cross(self.rows, c) for c in self.cols]
        square_units = [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
        unitlist = row_units + column_units + square_units
        units = dict((s, [u for u in unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(units[s], [])) - set([s])) for s in self.boxes)

    def convert_grid_from_string_to_dict(self, grid: str) -> dict:
        loaded_sample = json.loads(grid)
        values = self.extract_values(loaded_sample)
        # loaded_sample = json.load('sample.json')
        # print("loaded_sample: " + loaded_sample)
        return values


    def extract_values(self, loaded_sample:list) -> dict:
        #Build json document
        result = dict()
        for el in loaded_sample:
            key = next(iter(el))
            result[key] = {key: {el[key]}}

        #"i = 1
        #"for block in self.blocks:
        #"    grid_key = f"{block.index}{i}"
        #    self.grid[grid_key] = block.value

        return result

    def eliminate(self, values: dict) -> dict:
        """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.

        Arguments:
            values {list} -- A sudoku in dictionary form.

        Returns:
            dict {dict} -- The resulting sudoku in dictionary form.
        """
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_values:
            digit = values[box]
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(digit, '')
        return values

    def only_choice(self, values) -> dict:
        """
        Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        for unit in self.unitlist:
            for digit in self.cols:
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    values[dplaces[0]] = digit
        return values

    def reduce_puzzle(self, values: dict) -> dict:
        """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
            values = self.eliminate(values)
            values = self.only_choice(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False

        return values

    def naked_twins(self, values):
        """Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}
        Returns:
            the values dictionary with the naked twins eliminated from peers.
        """

        # Find boxes with 2 entries
        candidates = [box for box in values.keys() if len(values[box]) == 2]

        # Collect boxes that have the same elements
        twins = [[box1, box2] for box1 in candidates for box2 in self.peers[box1] if set(values[box1]) == set(values[box2])]

        for b1, b2 in twins:
            print(b1, b2, values[b1])

        for box1, box2 in twins:

            peers1 = set(self.peers[box1])
            peers2 = set(self.peers[box2])

            peers_int = peers1.intersection(peers2)

            # delete the two digits from all common peers
            for peer_box in peers_int:
                for rm_val in values[box1]:
                    values = self.assign_value(values, peer_box, values[peer_box].replace(rm_val, ''))

        return values

    def assign_value(self, values, box, value):
        """
        Please use this function to update your values dictionary!
        Assigns a value to a given box. If it updates the board record it.
        """

        # Don't waste memory appending actions that don't actually change any values
        if values[box] == value:
            return values

        values[box] = value
        if len(value) == 1:
            self.assignments.append(values.copy())
        return values

    def get_boxes(self):
        return self.boxes


if __name__ == "__main__":
    #grid = '..3.2.6.. 9..3.5.. 1..18.64. ...81.29. .7....... 8..67.82. ...26.95. .8..2.3.. 9..5.1.3..'
    grid = "[{\"A1\": \".\"},{\"A2\": \".\"},{\"A3\": \"3\"},{\"A4\": \".\"},{\"A5\": \"2\"},{\"A6\": \".\"},{\"A7\": \"6\"},{\"A8\": \".\"},{\"A9\": \".\"}," \
                "{\"B1\": \"9\"},{\"B2\": \".\"},{\"B3\": \".\"},{\"B4\": \"3\"},{\"B5\": \".\"},{\"B6\": \"5\"},{\"B7\": \".\"},{\"B8\": \".\"},{\"B9\": \".\"}," \
                "{\"C1\": \"1\"},{\"C2\": \".\"},{\"C3\": \".\"},{\"C4\": \"1\"},{\"C5\": \"8\"},{\"C6\": \".\"},{\"C7\": \"6\"},{\"C8\": \"4\"},{\"C9\": \".\"}," \
                "{\"D1\": \".\"},{\"D2\": \".\"},{\"D3\": \".\"},{\"D4\": \"8\"},{\"D5\": \".\"},{\"D6\": \".\"},{\"D7\": \"2\"},{\"D8\": \"9\"},{\"D9\": \".\"}," \
                "{\"E1\": \".\"},{\"E2\": \"7\"},{\"E3\": \".\"},{\"E4\": \".\"},{\"E5\": \".\"},{\"E6\": \".\"},{\"E7\": \".\"},{\"E8\": \".\"},{\"E9\": \".\"}," \
                "{\"F1\": \"8\"},{\"F2\": \".\"},{\"F3\": \".\"},{\"F4\": \"6\"},{\"F5\": \"7\"},{\"F6\": \".\"},{\"F7\": \"8\"},{\"F8\": \"2\"},{\"F9\": \".\"}," \
                "{\"G1\": \"3\"},{\"G2\": \"7\"},{\"G3\": \"2\"},{\"G4\": \"6\"},{\"G5\": \"8\"},{\"G6\": \"9\"},{\"G7\": \"5\"},{\"G8\": \"1\"},{\"G9\": \"4\"}," \
                "{\"H1\": \".\"},{\"H2\": \"8\"},{\"H3\": \".\"},{\"H4\": \"2\"},{\"H5\": \".\"},{\"H6\": \"3\"},{\"H7\": \"3\"},{\"H8\": \".\"},{\"H9\": \".\"}," \
                "{\"I1\": \"9\"},{\"I2\": \".\"},{\"I3\": \".\"},{\"I4\": \"5\"},{\"I5\": \".\"},{\"I6\": \"1\"},{\"I7\": \"0\"},{\"I8\": \".\"},{\"I9\": \".\"}]"

    sudoku = Sudoku("Wim's Sudoku", grid)
    values = sudoku.search()
    print('\n')
    print("result")
    print('\n')
    print(values)

