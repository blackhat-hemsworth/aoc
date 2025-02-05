def find_all(s: str, sub: str): # https://stackoverflow.com/a/4665027
    start = 0
    while True:
        start = s.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


class WordSearch:
    horizontal_space: list[str]
    vertical_space: list[str]
    diagonal_space: list[str]
    width: int
    height: int

    @property
    def total_count(self):
        return self.horizontal_count + self.vertical_count + self.diagonal_count

    @property
    def horizontal_count(self):
        return sum([s.count(self.word) + s.count(self.word[::-1]) for s in self.horizontal_space])

    @property
    def vertical_count(self):
        return sum([s.count(self.word) + s.count(self.word[::-1]) for s in self.vertical_space])

    @property
    def diagonal_count(self):
        return sum([s.count(self.word) + s.count(self.word[::-1]) for s in self.diagonal_space])

    def cross_matches(self, word: str = "MAS"):
        # h_matches = self.find_pos(word, "h") # somehow only off by 30??
        # v_matches = self.find_pos(word, "v")
        df_matches = self.find_pos(word, "df")
        db_matches = self.find_pos(word, "db")
        return set(df_matches).intersection(db_matches)

    def __init__(self, letterbox: list[str], word: str):
        self.word = word

        self.width, self.height = len(letterbox[0]), len(letterbox)
        self.horizontal_space = letterbox
        self.vertical_space = [''.join([row[i] for row in letterbox]) for i in range(len(letterbox[0]))]

        flip_box = [word[::-1] for word in letterbox]
        fwd_words = []
        bck_words = []
        fwd_coord = []
        bck_coord = []
        for col in range(-self.height + 1, self.width):
            if col < 0:
                row = -col
                col = 0
            else:
                row = 0

            fwd_letters = []
            bck_letters = []
            fwd_key = []
            bck_key = []
            for vert_index, hor_index in zip(range(row, min(self.height + row, self.height)),
                                             range(col, min(self.width + col, self.width))):
                fwd_letters.append(letterbox[vert_index][hor_index])
                bck_letters.append(flip_box[vert_index][hor_index])
                fwd_key.append((vert_index , hor_index))
                bck_key.append((vert_index, self.width - hor_index - 1))

            fwd_words.append(''.join(fwd_letters))
            bck_words.append(''.join(bck_letters))
            fwd_coord.append(fwd_key)
            bck_coord.append(bck_key)

        self.diagonal_fwd_coord = fwd_coord
        self.diagonal_bck_coord = bck_coord

        self.diagonal_fwd_space = fwd_words
        self.diagonal_bck_space = bck_words
        self.diagonal_space = fwd_words + bck_words

    def find_pos(self, word: str, space_id: str = "h"):
        match space_id:
            case "h":
                mod = 1
                space = self.horizontal_space
            case "v":
                mod = -1
                space = self.vertical_space
            case "df":
                mod = 1
                space = self.diagonal_fwd_space
            case "db":
                mod = -1
                space = self.diagonal_bck_space

        pos = []
        for index, row in enumerate(space):
            pos.extend([(index, int(col_index + .5 * (len(word) - 1))) for col_index in find_all(row, word)])
            pos.extend([(index, int(col_index + .5 * (len(word) - 1))) for col_index in find_all(row, word[::-1])])
        if len(space_id) < 2:
            return [p[::mod] for p in pos]
        else:
            if space_id == "df":
                return [self.diagonal_fwd_coord[a][b] for a, b in pos]
            if space_id == "db":
                return [self.diagonal_bck_coord[a][b] for a, b in pos]


with open("input.txt","r") as f:
    lb = [line.strip() for line in f.readlines()]

ws = WordSearch(lb,"XMAS")
print(ws.total_count, ws.horizontal_count, ws.vertical_count, ws.diagonal_count)

print(len(ws.cross_matches("MAS")))