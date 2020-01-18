'''Model of flight reservation system'''
from pprint import pprint as pp
class Flight(object):
    """ A Flight with particular passenger aircraft"""
    def __init__(self, number, aircraft):
        if not str(number[:2]).isalpha():
            raise ValueError("No airline code in '{}'".format(number))

        if not str(number[:2]).isupper():
            raise ValueError("Invalid airline code '{}'".format(number))

        if not (str(number[2:]).isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number '{}'".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def get_number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self,seat):
        rows, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in rows:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter

    def allocate_seats(self, seat, passenger):
        """
        Allocate seats to a passenger
        :param passenger:
        :return:
        Raise: ValueError: If the seat is unavailable
        """
        row, letter = self._parse_seat(seat)
        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))

        self._seating[row][letter] = passenger

    def realocate_passenger(self, from_seat, to_seat):
        """Realocate seats"""
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger allocated to this seat {}".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)

        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} is already occupied".format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.get_number(), self.aircraft_model())

    def _passenger_seats(self):
        row_number, sear_letters = self._aircraft.seating_plan()
        for row in row_number:
            for letter in sear_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row, letter))

class Aircraft:
    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)

class AirbusA319(Aircraft):
    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"




class Boeing777(Aircraft):
    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHIJ"



def console_card_printer(passenger, seat, flight_number, aircraft):
    output = "| Name: {0}   Flight: {1}     Seat: {2}   Aircraft: {3} |".\
        format(passenger, seat, flight_number, aircraft)
    banner = '+' + '-' * (len(output)-2) + '+'
    border = '|' + ' ' * (len(output)-2) + '|'
    lines = [banner, border,output, border,banner]
    card = '\n'.join(lines)
    print(card)
    print()


def main():
    a = AirbusA319('G-EUPT')
    print(a.num_seats())

    b = Boeing777('G-GSPS')
    print(b.num_seats())
    f = Flight("SN1234", AirbusA319('G-EUPT'))
    print(f.aircraft_model())
    f.allocate_seats("12A", "passenger1")
    f.allocate_seats("15F", "passenger2")
    f.allocate_seats("15E", "passenger3")
    f.allocate_seats("1C", "passenger4")
    f.allocate_seats("1D", "passenger5")
    f.realocate_passenger('12A', '15D')
    print(f.num_available_seats())
    f.make_boarding_cards(console_card_printer)

    g = Flight("SN1236", Boeing777('G-GSPS'))
    print(f.aircraft_model())
    g.allocate_seats("12A", "passenger1")
    g.allocate_seats("15D", "passenger2")
    g.allocate_seats("15E", "passenger3")
    g.allocate_seats("1C", "passenger4")
    g.allocate_seats("1D", "passenger5")

    print(g.num_available_seats())

    # f = Flight("12345")
    # f = Flight("as345")


if __name__ == '__main__':
    main()
