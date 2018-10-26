class Lookup:
    def __init__(self,items):
        self.items = items
    def __iter__(self):
        for item in self.items:
            yield(item)
        
STATUSES = [('0','Open'),
            ('1','Working'),
            ('2','Closed'),
            ('3','Stopped'),
            ('4','Not doing this')]
PRIORITIES = [('0','Low'),
              ('1','Medium'),
              ('2','High')]
