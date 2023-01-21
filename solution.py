
from datetime import datetime
import asyncio
import math
import time

class AddressBook:
    def __init__(self, emp_id: str, first: str, last: str, email: str):
        self.emp_id = emp_id
        self.first = first
        self.last = last
        self.email = email

class Payroll:
    def __init__(self, emp_id: str, vacationDays: int):
        self.emp_id = emp_id
        self.vacationDays = vacationDays

class Employee:
    def __init__(self, id: str, name: str, startDate: datetime, endDate: datetime):
        self.id = id
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        
        
class EmailApi:
    def __init__(self):
        self.batch_id = 0
        

    def createBatch(self) -> int:
        self.queue = []
        self.batch_id += 1
        return self.batch_id

    def queueEmail(self, batch_id: int, email: str, subject: str, body: str):
        self.queue.append((email, subject, body))

    async def flushBatch(self, batch_id: int):
        #Simulation of flush function
        
        print("Flushing batch:", batch_id)
        while len(self.queue):
            
            time.sleep(1)  #not proper usage.just for simulation purposes
            print(self.queue.pop(0))

    
    
def years_since(start_date, end_date):
    return (end_date - start_date).days / 365.25

async def grant_vacation(email_api, payroll, addresses, employees):
    today = datetime.now()
    address_lookup = {address.emp_id: address for address in addresses}
    employee_lookup = {employee.id: employee for employee in employees}
    email_batch_id = email_api.createBatch()
    for payroll_info in payroll:
        
        emp_id = payroll_info.emp_id
        address_info = address_lookup[emp_id]
        emp_info = employee_lookup[emp_id]

        if emp_info.endDate:
            continue  #Do not want to send emails to former employees
        
        years_employed = math.floor(years_since(emp_info.startDate, today)) #Taking only the fully completed years into account

        new_vacation_balance = years_employed + payroll_info.vacationDays
        #Since we are not dealing with negative outputs,
        #its ok to cast this to int instead of using math.floor()

        email_api.queueEmail(
            email_batch_id,
            address_info.email,
            "Good news!",
            f"Dear {emp_info.name}, "
            f"based on your {years_employed} years of employment, you have been granted {years_employed} days of vacation, bringing your total to {new_vacation_balance}"
        )
    await email_api.flushBatch(email_batch_id)
    
    
    
    
    
#Employee A

emp_a = Employee(id='id_a', name='A', startDate=datetime(2021, 1, 1), endDate=None)
addr_a = AddressBook(emp_id='id_a', first='first_a', last='last_a', email='a@kidoz.com')
payroll_a = Payroll(emp_id='id_a', vacationDays=14)

    
#Employee B

emp_b = Employee(id='id_b', name='B', startDate=datetime(2021, 5, 1), endDate=None)
addr_b = AddressBook(emp_id='id_b', first='first_b', last='last_b', email='b@kidoz.com')
payroll_b = Payroll(emp_id='id_b', vacationDays=14)

    
#Employee C

emp_c = Employee(id='id_c', name='C', startDate=datetime(2018, 4, 23), endDate=datetime(2022, 3, 10))
addr_c = AddressBook(emp_id='id_c', first='first_c', last='last_c', email='c@kidoz.com')
payroll_c = Payroll(emp_id='id_c', vacationDays=14)


#Employee D

emp_d = Employee(id='id_d', name='D', startDate=datetime(2017, 7, 1), endDate=None)
addr_d = AddressBook(emp_id='id_d', first='first_d', last='last_d', email='d@kidoz.com')
payroll_d = Payroll(emp_id='id_d', vacationDays=14)
    
    
addresses = [addr_a, addr_b, addr_c, addr_d]
employees = [emp_a, emp_b, emp_c, emp_d]
payroll = [payroll_a, payroll_b, payroll_c, payroll_d]

asyncio.run(grant_vacation(EmailApi(), payroll, addresses, employees))



    
    
