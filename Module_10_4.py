from time import sleep
from threading import Thread, Lock


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Cafe:

    def __init__(self, tables):
        self.queue = []
        self.tables = tables
        self.customer_count = 0
        self.lock = Lock()

    def customer_arrival(self):
        for i in range(20):
            self.customer_count += 1
            print(f"Посетитель {self.customer_count} прибыл")
            self.serve_customer(self.customer_count)
            sleep(1)

    def serve_customer(self, customer_number):
        with self.lock:
            table = next((t for t in self.tables if not t.is_busy), None)
            if table:
                print(f'Посетитель номер {customer_number} занимает стол номер {table.number}')
                table.is_busy = True
                customer_threading = Customer(customer_number, table, self)
                customer_threading.start()
            else:
                print(f'Посетитель номер {customer_number} ожидает свободный стол')
                self.queue.append(customer_number)


class Customer(Thread):
    def __init__(self, customer_number, table, cafe):
        super().__init__()
        self.customer_number = customer_number
        self.table = table
        self.cafe = cafe

    def run(self):
        print(f'Посетитель номер {self.customer_number} ест за столиком номер {self.table.number}')
        sleep(5)
        print(f'Посетитель номер {self.customer_number} поел и ушел')
        self.table.is_busy = False
        with cafe.lock:
            while cafe.queue:
                table = next((t for t in cafe.tables if not t.is_busy), None)
                if table:
                    current_customer = cafe.queue.pop(0)
                    print(f'Пользователь номер {current_customer} сел за стол номер {table.number}')
                    table.is_busy = True
                    customer_threading = Customer(current_customer, table, self)
                    customer_threading.start()
                else:
                    break


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()
