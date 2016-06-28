__author__ = 'Administrator'


# The Strategy Pattern provides a means of encapsulating a set of algorithms
# that can be used interchangeably, depending on the user¡¯s needs.


WINNERS = ("Nikolai Andrianov", "Matt Biondi", "Bj?rn D?hlie",
"Birgit Fischer", "Sawao Kato", "Larisa Latynina", "Carl Lewis",
"Michael Phelps", "Mark Spitz", "Jenny Thompson")

class Layout:
    def __init__(self, tabulator):
        self.tabulator = tabulator
    def tabulate(self, rows, items):
        return self.tabulator(rows, items)

def html_tabulator(rows, items):
    columns, remainder = divmod(len(items), rows)
    if remainder:
        columns += 1
    column = 0
    table = ['<table border="1">\n']
    for item in items:
        if column == 0:
            table.append("<tr>")
    table.append("<td>{}</td>".format(escape(str(item))))
    column += 1
    if column == columns:
        table.append("</tr>\n")
    column %= columns
    if table[-1][-1] != "\n":
        table.append("</tr>\n")
    table.append("</table>\n")
    return "".join(table)

def text_tabulator():
    pass

def main():
    htmlLayout = Layout(html_tabulator)
    for rows in range(2, 6):
        print(htmlLayout.tabulate(rows, WINNERS))
    textLayout = Layout(text_tabulator)
    for rows in range(2, 6):
        print(textLayout.tabulate(rows, WINNERS))