class Pagination:
    def __init__(self, page, size):
        self.page = int(page)
        self.size = int(size)
        self.range_from = (self.page - 1) * self.size
        self.range_to = self.page * self.size
